import unittest
import datetime
from utils import construct_message


class TestConstructMessage(unittest.TestCase):

    def test_thrusday(self):
        last_sunday = 27

        today = datetime.date(2022, 2, 3)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche 27 de 18 à 19h30 :date")

        today = datetime.date(2022, 2, 10)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche 27 de 18 à 19h30 :date")

        today = datetime.date(2022, 2, 17)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting de ce mois c'est :date:  dimanche 27 de 18 à 19h30 :date")

        today = datetime.date(2022, 2, 24)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting de ce mois c'est :date: ce dimanche de 18 à 19h30 :date")


    def test_saturday(self):
        last_sunday = 27
        today = datetime.date(2022, 2, 26)
        self.assertEqual(construct_message(today, last_sunday),
                         ":alert: Rappel :alert: Le meeting c'est demain à 18h http://lobembe.mongulu.cm/?q=meet")

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


if __name__ == '__main__':
    unittest.main()
