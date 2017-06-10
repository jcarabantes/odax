# -*- coding: utf-8 -*-
import time


class ProcessTimer:

    def __init__(self):
        self.current_time = time.time()

    def get_time(self):
        return (time.time() - self.current_time)
