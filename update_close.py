#!/usr/bin/env python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import finnhub
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pytz import timezone
from datetime import datetime
from datetime import timedelta
import time
import sys

# Setup client
finnhub_client = finnhub.Client(api_key="c0o9qlv48v6qah6s2b00")

def reset_client():
    global finnhub_client
    finnhub_client = finnhub.Client(api_key="c0o9qlv48v6qah6s2b00")


def maybe_run(func, *args, **kwargs):

    # try max 10 times
    for attempt in range(10):
        try:
            # run the function
            res = func(*args, **kwargs)
        except:
            # wait a minute, refresh the client and try again
            print("Unexpected error:", sys.exc_info()[0])
            time.sleep(60)
            reset_client()
        else:
            # break on success
            break

    # all attempts failed
    else:
        return None

    return res

def update_close():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("investment portfolio").sheet1

    rows = sheet.get_all_values()

    for i in range(len(rows)):
        row = rows[i]
        if row[0].isupper() and row[0][0] != 'V' and len(row[0]) != 5:
            res = maybe_run(finnhub_client.quote, row)
            if not res:
                continue

            close = res['c']
            sheet.update_cell(i + 1, 8, '$' + str(close))

if __name__ == "__main__":
    update_close()




