import csv
import requests
from io import StringIO

from decouple import config
from github import Github

from rich.traceback import install

install(show_locals=True)


def send_instant_message():
    headers = {'Priority': '5', 'Title': "Mongulu: meeting reminder"}
    message = "La réunion du collectif c'est maintenant https://meet.jit.si/mongulu"
    response = requests.post('https://ntfy.mongulu.cm/meetings', headers=headers, data=message.encode(encoding='utf-8'))
    response.raise_for_status()


# Currently Github Action does not support TimeZone so call at each last sunday at 6:00 PM will impossible
# This file will be executed manually at the meeting time
send_instant_message()
