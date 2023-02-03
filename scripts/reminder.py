import calendar
import csv
import datetime
from io import StringIO

import zulip
import requests
from decouple import config
from github import Github
from loguru import logger
from rich.traceback import install

from utils import (construct_assigned_issues, construct_issue_message,
                   construct_meeting_message, get_assigned_users, get_names,
                   get_table_ignored_assignees, get_table_open_issues,
                   get_table_zulip_members, get_zulip_id_from_assignee)

install(show_locals=True)

today = datetime.datetime.now()
month = calendar.monthcalendar(today.year, today.month)
last_sunday = max(month[-1][calendar.SUNDAY], month[-2][calendar.SUNDAY])

# Pass the path to your zuliprc file here.
zulip_client = zulip.Client(email="reminder-bot@mongulu.zulipchat.com", api_key=config('API_KEY'),
                            site="https://mongulu.zulipchat.com")

token = config("GH_TOKEN")
g = Github(token, verify=False)

if config("REMINDER_TYPE", default="") == "ISSUES" and today.weekday() == 3:

    t1 = get_table_open_issues(g)
    t1.present()
    t2 = get_table_zulip_members(zulip_client)
    t2.present()

    names = get_names(t2)
    assignees, ignored_assignees = get_assigned_users(t1, names)

    for assignee in assignees:
        zulip_message = construct_issue_message(list(t1.where(lambda o: assignee in o.Assignees)))

        zulip_id = get_zulip_id_from_assignee(t2, names, assignee)
        request = {"type": "private", "to": [zulip_id], "content": f" {zulip_message}"}
        result = zulip_client.send_message(request)
        logger.info(f"👉 {result}")

    if len(ignored_assignees) != 0:
        t3 = get_table_ignored_assignees(ignored_assignees)
        messages = construct_assigned_issues(t3.as_markdown())
        for zulip_message in messages:
            request = {"type": "private", "to": [470841], "content": f"{zulip_message}"}
            result = zulip_client.send_message(request)
            logger.info(f"👉 {result}")

if config("REMINDER_TYPE", default="") != "ISSUES" and today.weekday() != 3:

    zulip_message, sms_message = construct_meeting_message(today, last_sunday)
    if zulip_message != "":
        zulip_ids = get_table_zulip_members(zulip_client).all.user_id
        for zulip_id in zulip_ids:
            request = {"type": "private", "to": [zulip_id], "content": f" {zulip_message} "}
            result = zulip_client.send_message(request)  # zulip automatically send also an email to the users
            logger.info(f"👉 {result}")

    if sms_message != "":
        headers = {'Priority': '3', 'Title': "Mongulu: meeting reminder"}
        response = requests.post('https://ntfy.mongulu.cm/meetings', headers=headers,
                                 data=sms_message.encode(encoding='utf-8'))
        response.raise_for_status()
        logger.info(f"👉  message successfully sent: {sms_message}")
