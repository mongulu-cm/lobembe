from rich.traceback import install
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

install(show_locals=True)

import csv
from io import StringIO

from decouple import config
from github import Github
from twilio.twiml.voice_response import Say, VoiceResponse

token = config("GH_TOKEN")
account_sid = config("ACCOUNT_SID")
auth_token = config("AUTH_TOKEN")

client = Client(account_sid, auth_token)
g = Github(token, verify=False)
repo = g.get_repo("mongulu-cm/contacts")
contents = repo.get_contents("members.csv")
f = StringIO(contents.decoded_content.decode("utf-8"))
reader = csv.reader(f, delimiter=',')
next(reader)


def send_voice_message():

    response = VoiceResponse()
    response.say("La réunion du collectif c'est maintenant", voice='woman', language='fr-FR')

    for row in reader:
        try:
            client.calls.create(to=f"+33{row[3][1:]}", from_="+16625000434", twiml=response)
        except TwilioRestException as exc:
            if exc.status == 400:
                print(f"voice message failed to sent to {row[0]} {row[1]} because not registered")
            else:
                raise


# Currently Github Action does not support TimeZone so call at each last sunday at 6:00 PM will impossible
# This file will be executed manually at the meeting time
send_voice_message()
