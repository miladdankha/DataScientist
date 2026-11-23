import unittest

import pandas as pd

from logic import PROFESSIONAL, population, ranking


class PopulationAndRanking(unittest.TestCase):
    def test_denominator_and_multiple_choices(self):
        data = pd.DataFrame({
            "ResponseId": list("abcdef"),
            "Country": ["France", "France", "France", None, "Canada", "France"],
            "CodeMain": [PROFESSIONAL] * 5 + ["I create code occasionally"],
            "LanguagesHaveWorkedWith": ["SQL;SQL;Python", None, "Other, please specify", "SQL", "C", "Go"],
        }, dtype="string").set_index("ResponseId")
        french = population(data, "France")
        self.assertEqual(list(french.index), list("abc"))
        self.assertEqual(list(population(data, "Outside France").index), ["e"])
        table, n = ranking(french, "Languages", "Past-year use")
        self.assertEqual(n, 2)
        self.assertEqual(table["Technology"].tolist(), ["Python", "SQL"])
        self.assertEqual(table["Share (%)"].tolist(), [50, 50])
        empty, n = ranking(french.iloc[:0], "Languages", "Past-year use")
        self.assertTrue(empty.empty)
        self.assertEqual(n, 0)
