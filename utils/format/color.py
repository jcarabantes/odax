# -*- coding: utf-8 -*-


class color:

    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def blue(self, m):
        return "%s%s%s" % (self.OKBLUE, m, self.ENDC)

    def bold(self, m):
        return "%s%s%s" % (self.BOLD, m, self.ENDC)

    def green(self, m):
        return "%s%s%s" % (self.OKGREEN, m, self.ENDC)

    def warning(self, m):
        return "%s%s%s" % (self.WARNING, m, self.ENDC)

    def underline(self, m):
        return "%s%s%s" % (self.UNDERLINE, m, self.ENDC)

    def fail(self, m):
        return "%s%s%s" % (self.FAIL, m, self.ENDC)


