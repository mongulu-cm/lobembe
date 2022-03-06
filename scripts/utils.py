def construct_message(today, last_sunday):

    message = "" # message will be empty for saturday/sunday that are not near to meeting date

    if today.day == last_sunday:
        if int(today.hour) == 9:
            message = ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h http://lobembe.mongulu.cm/?q=meet"
        elif int(today.hour) == 13:
            message = ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h http://lobembe.mongulu.cm/?q=meet"
        elif int(today.hour) == 16:
            message = ":alert: Le meeting c'est maintenant http://lobembe.mongulu.cm/?q=meet :alert: "
    elif today.day == last_sunday - 1:
        message = ":alert: Rappel :alert: Le meeting c'est demain à 18h http://lobembe.mongulu.cm/?q=meet"
    elif today.day == last_sunday - 3:
        message = ":alert: Rappel :alert: Le meeting de ce mois c'est :date: ce dimanche de 18 à 19h30 :date"
    elif today.weekday() == 3:
        message = ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche " + str(
            last_sunday) + " de 18 à 19h30 :date"

    return message
