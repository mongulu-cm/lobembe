import calendar
import csv
import datetime
from io import StringIO

import zulip
from decouple import config
from github import Github
from loguru import logger
from rich.traceback import install
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from utils import (construct_assigned_issues, construct_issue_message,
                   construct_meeting_message, get_assigned_users, get_names,
                   get_table_ignored_assignees, get_table_open_issues,
                   get_table_zulip_members, get_zulip_id_from_assignee)

install(show_locals=True)

today = datetime.datetime.now()
month = calendar.monthcalendar(today.year, today.month)
last_sunday = max(month[-1][calendar.SUNDAY], month[-2][calendar.SUNDAY])

# Pass the path to your zuliprc file here.
client = zulip.Client(email="reminder-bot@mongulu.zulipchat.com", api_key=config('API_KEY'),
                      site="https://mongulu.zulipchat.com")

token = config("GH_TOKEN")
g = Github(token, verify=False)

account_sid = config("ACCOUNT_SID")
auth_token = config("AUTH_TOKEN")
client = Client(account_sid, auth_token)

if config("REMINDER_TYPE", default="") == "ISSUES" and today.weekday() == 3:

    t1 = get_table_open_issues(g)
    t1.present()
    t2 = get_table_zulip_members(client)
    t2.present()

    names = get_names(t2)
    assignees, ignored_assignees = get_assigned_users(t1, names)

    for assignee in assignees:
        zulip_message = construct_issue_message(list(t1.where(lambda o: assignee in o.Assignees)))

        zulip_id = get_zulip_id_from_assignee(t2, names, assignee)
        request = {"type": "private", "to": [zulip_id], "content": f" {zulip_message}"}
        result = client.send_message(request)
        logger.info(f"👉 {result}")

    if len(ignored_assignees) != 0:
        t3 = get_table_ignored_assignees(ignored_assignees)
        messages = construct_assigned_issues(t3.as_markdown())
        for zulip_message in messages:
            request = {"type": "private", "to": [470841], "content": f"{zulip_message}"}
            result = client.send_message(request)
            logger.info(f"👉 {result}")

else:

    zulip_message, sms_message = construct_meeting_message(today, last_sunday)
    if zulip_message != "":
        zulip_ids = get_table_zulip_members(client).all.user_id
        for zulip_id in zulip_ids:
            request = {"type": "private", "to": [zulip_id], "content": f" {zulip_message} "}
            result = client.send_message(request)
            logger.info(f"👉 {result}")

    if sms_message != "":
        repo = g.get_repo("mongulu-cm/contacts")
        contents = repo.get_contents("members.csv")
        f = StringIO(contents.decoded_content.decode("utf-8"))
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            try:
                client.messages.create(to=f"+33{row[3][1:]}", from_="+16625000434",
                                       body=sms_message)
            except TwilioRestException as exc:
                if exc.status == 400:
                    print(f"message failed to sent to {row[0]} {row[1]} because not registered")
                else:
                    raise

