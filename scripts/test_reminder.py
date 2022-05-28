import datetime

import pytest
import zulip
from decouple import config
from github import Github
from pytest_hoverfly import hoverfly

from utils import (construct_assigned_issues, construct_issue_message,
                   construct_meeting_message, get_assigned_users, get_names,
                   get_table_ignored_assignees, get_table_open_issues,
                   get_table_zulip_members, get_zulip_id_from_assignee,
                   retrieve_assigned_issues)


def test_thrusday():
    last_sunday = 27

    for day in [3, 10, 17]:
        today = datetime.date(2022, 2, day)
        assert construct_meeting_message(today, last_sunday) == \
                         ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche 27 de 18 à 19h30 :date:"

    today = datetime.date(2022, 2, 24)
    assert construct_meeting_message(today, last_sunday) == \
                     ":alert: Rappel :alert: Le meeting de ce mois c'est :date: ce dimanche de 18 à 19h30 :date:"

def test_saturday():
    last_sunday = 27
    today = datetime.date(2022, 2, 26)
    assert construct_meeting_message(today, last_sunday) \
           == ":alert: Rappel :alert: Le meeting c'est demain à 18h http://lobembe.mongulu.cm/?q=meet"

    for day in [5, 12, 19]:
        today = datetime.date(2022, 2, day)
        assert construct_meeting_message(today, last_sunday) == ""

def test_sunday():
    last_sunday = 27

    today = datetime.datetime(2022, 2, 27, 9, 00, 30)
    assert construct_meeting_message(today, last_sunday) == \
                     ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h http://lobembe.mongulu.cm/?q=meet"

    today = datetime.datetime(2022, 2, 27, 13, 00, 30)
    assert construct_meeting_message(today, last_sunday) == \
                     ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h http://lobembe.mongulu.cm/?q=meet"

    today = datetime.datetime(2022, 2, 27, 16, 45, 30)
    assert construct_meeting_message(today, last_sunday) == \
                     ":alert: Le meeting c'est maintenant http://lobembe.mongulu.cm/?q=meet :alert: "

    for day in [6, 13, 20]:
        today = datetime.date(2022, 2, day)
        assert construct_meeting_message(today, last_sunday) == ""


@pytest.fixture()
def github_client():
    token = config("GH_TOKEN")
    return Github(token,verify=False)

@pytest.fixture()
@hoverfly('reminder_issues')
def zulip_client():
    return zulip.Client(email="reminder-bot@mongulu.zulipchat.com", api_key=config('API_KEY'),
                        site="http://mongulu.zulipchat.com", insecure=True)


@hoverfly('not_empty_issues')
def test_not_empty_issues(github_client):

    # Getting the repo based on the info from command line
    repo = github_client.get_repo("mongulu-cm/lobembe")
    issues = repo.get_issues(state="open")
    # Calling the funtions
    issues = retrieve_assigned_issues(issues)
    assert  issues == [
        {'Title': 'Alternative à monocle ( car il supporte juste les merge)', 'Assignees': ['billmetangmo'],
          'CreatedAt': '15-11-2021', 'Url': 'https://github.com/mongulu-cm/lobembe/issues/3',
          'AssignedAt': '08-01-2022'}
                      ]

@hoverfly('empty_issues')
def test_empty_issues(github_client):
    repo = github_client.get_repo("mongulu-cm/monocle")
    issues = repo.get_issues(state="open")
    issues = retrieve_assigned_issues(issues)
    assert  issues == []


def test_fuzzy_matching():
    names =['Flomin Tchawe', 'TCHAPTCHET NOUDJET CHRISTIAN IGOR', 'Ghislain Takam',
            'Pascaline', 'Fabiola', 'Dimitri7', 'Boris', 'Patrick Djiela', 'Dimitri.T',
            'Tchepga Patrick', 'EMAKO AUBERT', 'behanzin777', 'ngnnpgn']

    from thefuzz import process
    assert process.extractOne("fabiolatagne97", names)[0] == "Fabiola" and \
            process.extractOne("fabiolatagne97", names)[1] == 90
    assert process.extractOne("christian970", names)[0] == "TCHAPTCHET NOUDJET CHRISTIAN IGOR" and \
            process.extractOne("christian970", names)[1] == 68
    assert process.extractOne("ngnnpgn", names)[0] == "ngnnpgn" and \
            process.extractOne("ngnnpgn", names)[1] == 100
    assert process.extractOne("billmetangmo", names)[0] == "TCHAPTCHET NOUDJET CHRISTIAN IGOR" and \
           process.extractOne("billmetangmo", names)[1] == 45


@hoverfly('reminder_issues')
def test_issues_messages(github_client,zulip_client):

    t1 = get_table_open_issues(github_client)
    t2 = get_table_zulip_members(zulip_client)
    names = get_names(t2)
    _, ignored_assignees = get_assigned_users(t1, names)

    assignees = ["billmetangmo"]
    assert get_zulip_id_from_assignee(t2, names, assignees[0]) == 485816 # celui de christian

    # car mon nom sur zulip était pas bon
    ignored_assignees = [{'assignnee (github)': 'billmetangmo',
                          'correspondance (zulip)': ('TCHAPTCHET NOUDJET CHRISTIAN IGOR', 45)}]
    t3 = get_table_ignored_assignees(ignored_assignees)
    messages = construct_assigned_issues(t3.as_markdown())
    assert messages[1] == '| assignnee (github) | correspondance (zulip) |\n|---|---|\n| billmetangmo | (\'TCHAPTCHET NOUDJET CHRISTIAN IGOR\', 45) |\n'

    message = construct_issue_message(list(t1.where(lambda o: assignees[0] in o.Assignees)))

    assert message == ":warning: Tu as actuellement 1 issue(s) en cours: \n \n" + \
    "* [Alternative à monocle ( car il supporte juste les merge)](https://github.com/mongulu-cm/lobembe/issues/3)"+ \
    " qui t'est assigné depuis le :date: **08-01-2022** \n"+ \
    "\n Essaie de trouver du temps pour ça :pray: :pray:"

    # pytest test_reminder.py -k test_reminder_issues -s