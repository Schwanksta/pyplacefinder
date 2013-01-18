import urllib
import json

VERSION = (0, 1, 1, "pre")
def get_version():
  version = '%s.%s' % (VERSION[0], VERSION[1])
  if VERSION[2]:
    version = '%s.%s' % (version, VERSION[2])
  if VERSION[3:]:
    version = '%s.%s' % (version, VERSION[3])
  return version


class PlaceFinderException(Exception):
  pass

class PlaceFinder(object):
  def __init__(self, appid=""):
    self.appid = appid
  
  def geocode(self, **params):
    results = self.query(params)
    return results
  
  def reverseGeocode(self, **params):
    params['gflags'] = 'r'
    return self.geocode(**params)
  
  def query(self, params):
    params['appid'] = self.appid
    params['flags'] = "j"
    
    url = "http://where.yahooapis.com/geocode?%s" % urllib.urlencode(params)
    connection = urllib.urlopen(url)
    
    try:
      data = json.loads(connection.read())
      if int(data['ResultSet']['Error']) > 0:
        raise PlaceFinderException(data['ResultSet']['ErrorMessage'])
      else:
        if len(data['ResultSet']['Results']) > 0:
          result_list = []
          for result in data['ResultSet']['Results']:
            result[u'quality_type'] = QUALITY_TYPES.get(result['quality'], '')
            result[u'quality_description'] = QUALITY_DESCRIPTIONS.get(result['quality'], '')
            result_list.append(result)
          return result_list
        else:
          return None
    except:
      raise PlaceFinderException
    finally:
      connection.close()


# A crosswalk between quality codes and their more informative descriptions
# http://developer.yahoo.com/geo/placefinder/guide/responses.html#address-quality
QUALITY_TYPES = {
  99: 'Point',
  90: 'Point',
  87: 'Point',
  86: 'Point',
  85: 'Point',
  84: 'Point',
  82: 'Point',
  80: 'Point',
  75: 'Line',
  74: 'Line',
  72: 'Line',
  71: 'Line',
  70: 'Line',
  64: 'Area', 
  63: 'Area',
  62: 'Area',
  60: 'Area',
  59: 'Area',
  50: 'Area',
  49: 'Area',
  40: 'Area',
  39: 'Area',
  30: 'Area',
  29: 'Area',
  20: 'Area',
  19: 'Area',
  10: 'Area',
   9: 'Area',
   0: 'Area'
}
QUALITY_DESCRIPTIONS = {
  99: 'Coordinate',
  90: 'POI',
  87: 'Address match with street match',
  86: 'Address mismatch with street match',
  85: 'Address match with street mismatch',
  84: 'Address mismatch with street mismatch',
  82: 'Intersection with street match',
  80: 'Intersection with street mismatch',
  75: 'Postal unit/segment (Zip+4 in US)',
  74: 'Postal unit/segment, street ignored (Zip+4 in US)',
  72: 'Street match',
  71: 'Street match, address ignored',
  70: 'Street mismatch',
  64: 'Postal zone/sector, street ignored (Zip+2 in US)',
  63: 'AOI',
  62: 'Airport',
  60: 'Postal district (Zip Code in US)',
  59: 'Postal district, street ignored (Zip Code in US)',
  50: 'Level4 (Neighborhood)',
  49: 'Level4, street ignored (Neighborhood)',
  40: 'Level3 (City/Town/Locality)',
  39: 'Level3, level4 ignored (City/Town/Locality)',
  30: 'Level2 (County)',
  29: 'Level2, level3 ignored (County)',
  20: 'Level1 (State/Province)',
  19: 'Level1, level2 ignored (State/Province)',
  10: 'Level0 (Country)',
   9: 'Level0, level1 ignored (Country)',
   0: 'Not an address'
}
