#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from google_sheets_access import append_value
import usage_telegram


def cb_new_data(data_type, value):
    tm = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
    append_value(data_type, tm, value)


usage_telegram.NEW_USAGE_CB = cb_new_data


if __name__ == "__main__":
    usage_telegram.main()
