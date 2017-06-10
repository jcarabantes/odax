# -*- coding: utf-8 -*-
import sys
import logging


class Output:

    def __init__(self, is_verbose=False):
        self.is_verbose = is_verbose

    def out(self, message, force_show=False, backspace=False):
        """
            Prints only if verbose has been set to true.
            force_show even if no verbose was set
            backspace is used just to show FAIL or SUCCESS after an action
                ABC ........ FAIL (there are two output.out)
        """
        logging.info(message)

        if(self.is_verbose or force_show):

            sys.stdout.write("{0}".format(message))
            if (not backspace):
                sys.stdout.write("\n".format(message))
            if (backspace):
                sys.stdout.write('\b')
            sys.stdout.flush()

    def error(self, message):
        self.out("{0}".format(message), True, False)