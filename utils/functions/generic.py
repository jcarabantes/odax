# -*- coding: utf-8 -*-
import urllib2
import time
from utils.format.color import color
from utils.format.output import Output


def show_banner(current_version):

    Color = color()

    print "      ___  ____  _  _ __  __"
    print "     / _ \|  _ \| || |\ \/ /"
    print "    | | | | | | | || |_\  / "
    print "    | |_| | |_| |__   _/  \ "
    print "     \___/|____/   |_|/_/\_\\"
    print "                        "
    print("    {0}doo {1}ictionary {2}ttack {3}MLRPC Tool").format(
        Color.green(Color.bold("O")),
        Color.green(Color.bold("D")),
        Color.green(Color.bold("A")),
        Color.green(Color.bold("X")))
    print "\n    Author: @javicarabantes"
    print "    Version: {0}".format(Color.bold(current_version))
    print "    Tested on Odoo {0}\n\n".format(Color.bold('v8, v9, v10'))


def show_epilog_examples(name=None):
    return """
Examples:
    Enumerate Databases without banner (-q):
    $ {0} -q --enum-db <host_name/ip> <port>

    Enumerate Versions using TOR:
    $ {0} --enum-version --tor localhost:9050 odoo-server-test.com 8069

    Dictionary attack using 10 threads:
    $ {0} --threads=10 --db db1 -u <path> -p <path> odoo-server-test.com 8069

    Dictionary attack with verbose mode and logging:
    $ {0} -vv --db=db1 --log=<path> --users <path> --pass <path> odoo-server-test.com 8069

    Dictionary attack and continue the attack using TOR:
    $ {0} -c --db db1 --tor=localhost:9050 --users <path> --pass <path> odoo-server-test.com 8069
    """.format(name)


def check_url(host, port, verbose):
    output = Output(verbose)
    c = color()
    attempts = 3
    success = False
    output.out("[+] Connection attempts ({0}):  "
        .format(attempts), force_show=True, backspace=True)
    for i in range(attempts):
        try:
            urllib2.urlopen('http://{0}:{1}'.format(host, port), timeout=2)
            success = True
            break
        except:
            time.sleep(0.5)
            success = False
        finally:
            output.out("{0}".format(c.warning(i+1)), force_show=True, backspace=True)
    print
    return success