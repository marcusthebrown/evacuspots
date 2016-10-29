import json
import unittest
import urllib2

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

    def test_evacuspots_exist_on_city_gis(self):
        response = urllib2.urlopen('http://gis.nola.gov:6080/arcgis/rest/services/PublicSafety/Evacuspots/MapServer/0/query?where=1%3D1&outFields=*&f=geojson')
        city_evacuspots = json.loads(response.read())
        city_evacuspot_names = [es['properties']['FACNAME'] for es in city_evacuspots['features']]
        for evacuspot in self.evacuspots:
            self.assertTrue(evacuspot['name'] in city_evacuspot_names, '{} is not in the city\'s gis dataset'.format(evacuspot['name']))

if __name__ == '__main__':
    unittest.main()
