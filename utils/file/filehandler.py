# -*- coding: utf-8 -*-
import sys


class FileHandler:

    def __init__(self):
        pass

    def open(self, path, mode='r'):
        try:
            fh = open(path, mode)
        except IOError as io:
            print io
            sys.exit(1)
        except Exception as e:
            print e
            sys.exit(1)
        else:
            return fh

    def seek_from_line(self, path, l=0):
        """
            Open the password file
            and seek a specific line to start.
            Each thread knows where to stop
        """

        line = ""
        fhandler = self.open(path, 'r')
        content = fhandler.readlines()

        line_offset = []
        offset = 0

        for line in content:
            line_offset.append(offset)
            offset += len(line)

        fhandler.seek(0)
        l = int(l)
        fhandler.seek(line_offset[l])

        return fhandler

    def get_total_lines(self, path):

        ret = 0
        fh = self.open(path)
        for line in fh.readlines():
            ret += 1
        fh.close()

        return ret
