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

    def test_geojson_required_fields(self):
        with open('evacuspots.geojson', 'r') as f:
            evacuspots_geojson = json.load(f)
            # assert that the lon and lat are within the valid range for new orleans
            for feature in evacuspots_geojson['features']:
                lon, lat = feature['geometry']['coordinates'][0], feature['geometry']['coordinates'][1]
                self.assertTrue(lon > -91 and lon < -89 , 'Longitude {} is invalid'.format(lon))
                self.assertTrue(lat > 28 and lat < 30.5, 'Latitude {} is invalid'.format(lat))
            # assert that the properties object has the required fields
            required_props = [p for p in self.required_fields if p is not 'longitude' and p is not 'latitude']
            for prop in required_props:
                self.assertTrue(prop in feature['properties'], '{} is required but missing from properties'.format(prop))

if __name__ == '__main__':
    unittest.main()
