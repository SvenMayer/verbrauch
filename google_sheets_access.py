#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:24:42 2022

@author: sven
"""
# # auth.py
# from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

import mycredentials


SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
]
credentials = service_account.Credentials.from_service_account_file(
    mycredentials.credentials_file, scopes=SCOPES)
service = spreadsheet_service = build('sheets', 'v4', credentials=credentials)


def append_value(sheet, tm, val):
    global service

    range_ = "{:s}!A1:B1000".format(sheet)

    # How the input data should be interpreted.
    value_input_option = "USER_ENTERED"

    # How the input data should be inserted.
    insert_data_option = "INSERT_ROWS"

    value_range_body = {
        "values": [[tm, val]]
    }

    request = service.spreadsheets().values().append(
        spreadsheetId=mycredentials.spreadsheet_id,
        range=range_,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body)
    response = request.execute()

