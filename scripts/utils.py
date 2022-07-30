import itertools

from littletable import Table
from thefuzz import process


def retrieve_assigned_issues(issues):
    """The funtion retrives the data of issues and returns an array"""

    assigned_issues = []

    for i in issues:
        if len(i.assignees) == 0:
            continue

        for j in i.get_events():
            if j.assignee is not None:
                assigned_date = j.created_at
                break

        issue = {"Title": i.title, "Assignees": [name.login for name in i.assignees],
                 "CreatedAt": i.created_at.strftime("%d-%m-%G"), "Url": i.html_url,
                 "AssignedAt": assigned_date.strftime("%d-%m-%G")}

        assigned_issues.append(issue)

    return assigned_issues


def construct_meeting_message(today, last_sunday):
    zulip_message = ""  # message will be empty for saturday/sunday that are not near to meeting date
    sms_message = ""

    if today.day == last_sunday:
        if int(today.hour) in {9, 13}:
            zulip_message = ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h http://lobembe.mongulu.cm/?q=meet"
            sms_message = zulip_message
        elif int(today.hour) == 16:
            zulip_message = ":alert: Le meeting c'est maintenant http://lobembe.mongulu.cm/?q=meet :alert: "
    elif today.day == last_sunday - 1:
        zulip_message = ":alert: Rappel :alert: Le meeting c'est demain à 18h http://lobembe.mongulu.cm/?q=meet"
        sms_message = zulip_message
    elif today.day == last_sunday - 3:
        zulip_message = ":alert: Rappel :alert: Le meeting de ce mois c'est :date: ce dimanche de 18 à 19h30 :date:"
    elif today.weekday() == 3:
        zulip_message = ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche " + str(
            last_sunday) + " de 18 à 19h30 :date:"

    return zulip_message, sms_message


def construct_issue_message(issues):
    message = f":warning: Tu as actuellement {len(issues)} issue(s) en cours: \n \n"
    for issue in issues:
        message = f"{message}* [{issue.Title}]({issue.Url}) qui t'est assigné depuis le :date: **{issue.AssignedAt}** \n"

    return message + "\n Essaie de trouver du temps pour ça :pray: :pray:"


def construct_assigned_issues(table):
    return ["Les utilisateurs suivant n'ont pas reçu de rappel car la correspodance a échoué", table,
            ":bangbang:  **IL FAUT DEMANDER AUX UTILISATEURS DE CHANGER LEUR NOM ZULIP**"]


def get_table_open_issues(github_client):
    issues = []
    org = github_client.get_organization("mongulu-cm")
    for repo in org.get_repos():
        repo_issues = retrieve_assigned_issues(repo.get_issues(state="open"))
        issues.append(repo_issues)

    flatten_issues = list(itertools.chain(*issues))
    t1 = Table("open_issues")
    t1.insert_many(flatten_issues)
    return t1


def get_table_zulip_members(zulip_client):
    result = zulip_client.get_members()
    return Table("zulip_users").insert_many(result["members"]) \
        .where(is_bot=False) \
        .select("full_name user_id")


def get_assigned_users(t1, names):
    import itertools
    assignees = set(list(itertools.chain(*list(t1.all.Assignees))))
    ignored_assignees = [{"assignnee": x, "correspondance": process.extractOne(x, names)}
                         for x in assignees if process.extractOne(x, names)[1] < 68]
    for x in ignored_assignees:
        assignees.remove(x['assignnee'])

    return assignees, ignored_assignees


def get_names(t2):
    return list(t2.all.full_name)


def get_table_ignored_assignees(ignored_assignees):
    return Table("igonred_assigned").insert_many(ignored_assignees)


def get_zulip_id_from_assignee(t2, names, assignee):
    return t2.where(full_name=process.extractOne(assignee, names)[0])[0].user_id


def send_sms(client, message, number):
    client.messages.create(to=number, from_="+16625000434",
                           body=message)
