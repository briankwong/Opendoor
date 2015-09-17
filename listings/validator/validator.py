'''
Run: python validator.py
'''
from library.geojson import validation, codec
import urllib2
import sys

def main():
  if len(sys.argv) != 2:
    raise Exception('Please provide the URL to query')

  url = sys.argv[1]
  body = urllib2.urlopen(url).read()
  result = codec.loads(body)
  check_result = validation.is_valid(result)
  assert check_result['valid'] == 'yes'
  print(check_result)

if __name__ == "__main__":
    main()
