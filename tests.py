import unittest
import pyplacefinder
from pprint import pprint
from private_settings import APP_ID


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.client = pyplacefinder.PlaceFinder(APP_ID)


class GeocoderTest(BaseTest):
    
    def test_location(self):
        self.result = self.client.geocode(
            location='220 W. 1st Street, Los Angeles, CA, 90012'
        )
        self.assertEquals(len(self.result), 1)
        self.assertEquals(type(self.result), type([]))
        self.result = self.client.geocode(location='Winnetka')
        self.assertEquals(len(self.result), 2)
    
    def test_state_bias(self):
        self.result = self.client.geocode(city='Winnetka', state='CA')
        self.assertEquals(len(self.result), 1)
    
    def test_country_bias(self):
        self.result = self.client.geocode(city='Toledo', country='SPAIN')
        self.assertEquals(len(self.result), 1)

if __name__ == '__main__':
    unittest.main()
