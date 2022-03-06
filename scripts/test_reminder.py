import unittest
import datetime
from utils import construct_message


class TestConstructMessage(unittest.TestCase):

    def test_thrusday(self):
        last_sunday = 27

        for day in [3, 10, 17]:
            today = datetime.date(2022, 2, day)
            self.assertEqual(construct_message(today, last_sunday),
                             ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche 27 de 18 à 19h30 "
                             ":date")

        today = datetime.date(2022, 2, 24)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting de ce mois c'est :date: ce dimanche de 18 à 19h30 :date")

    def test_saturday(self):
        last_sunday = 27
        today = datetime.date(2022, 2, 26)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting c'est demain à 18h http://lobembe.mongulu.cm/?q=meet")

        for day in [5, 12, 19]:
            today = datetime.date(2022, 2, day)
            self.assertEqual(construct_message(today, last_sunday), "")

    def test_sunday(self):
        last_sunday = 27

        today = datetime.datetime(2022, 2, 27, 9, 00, 30)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h "
                         "http://lobembe.mongulu.cm/?q=meet")

        today = datetime.datetime(2022, 2, 27, 13, 00, 30)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting c'est tout à l'heure à 18h "
                         "http://lobembe.mongulu.cm/?q=meet")

        today = datetime.datetime(2022, 2, 27, 16, 45, 30)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Le meeting c'est maintenant http://lobembe.mongulu.cm/?q=meet :alert: ")

        for day in [6, 13, 20]:
            today = datetime.date(2022, 2, day)
            self.assertEqual(construct_message(today, last_sunday), "")


if __name__ == '__main__':
    unittest.main()
