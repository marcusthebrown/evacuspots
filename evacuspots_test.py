import json
import unittest

class TestEvacuspotJson(unittest.TestCase):
    required_fields = [
        'address', 'latitude', 'longitude', 'name', 'neighborhood', 'special_needs_location', 'spot_number', 'zip'
    ]

    def setUp(self):
        f = open("evacuspots.json")
        self.evacuspots = json.load(f)
        f.close()

    def test_required_fields(self):
        for evacuspot in self.evacuspots:
            for field in self.required_fields:
                self.assertTrue(field in evacuspot, 'Missing field {}'.format(field))

    def test_unique_spot_number(self):
        ids = dict()
        for evacuspot in self.evacuspots:
            spot_number = evacuspot['spot_number']
            self.assertFalse(spot_number in ids, "Spot {} is not unique".format(spot_number))
            ids[spot_number] = True

if __name__ == '__main__':
    unittest.main()