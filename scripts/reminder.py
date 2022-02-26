import datetime
import calendar
import zulip
import os
from utils import construct_message

today = datetime.datetime.now()
month = calendar.monthcalendar(today.year, today.month)
last_sunday = max(month[-1][calendar.SUNDAY], month[-2][calendar.SUNDAY])

# Pass the path to your zuliprc file here.
client = zulip.Client(email="reminder-bot@mongulu.zulipchat.com", api_key=os.environ['API_KEY'],
                      site="https://mongulu.zulipchat.com")

# Send a stream message
request = {
    "type": "stream",
    "to": "general",
    "topic": "meeting",
    "content": " {} \
     \n \
     \n *NB: Pour ceux qui ont oublié. En décembre 2021, on avait décidé que les réunions seraient désormais fixes. \
      Ce sera à chaque fois le dernier dimanche du mois de 18h à 19h30* ".format(construct_message(today, last_sunday))
}

result = client.send_message(request)
print(result)
