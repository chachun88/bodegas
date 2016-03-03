#!/usr/bin/python
# -*- coding: UTF-8 -*-


import schedule
import time


def job():
    print "aaa"

schedule.every(10).seconds.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
