'''
Run: python validator.py
'''
from library.geojson import validation, codec
import urllib2
import sys

def main():
  if len(sys.argv) == 1:
    port = 8000 # default port
  elif len(sys.argv) == 2:
    port  = int(sys.argv[1])
  else:
    raise Exception(
        'At most one argument (i.e., port number) is accepted by validator.py'
    )

  filters = [
    'max_bath=2',
    'max_bed=2',
    'max_price=200000',
    'min_bath=2',
    'min_bed=2',
    'min_price=100000',
  ]
  url = 'http://127.0.0.1:{}/listings?{}'.format(port, '&'.join(filters))
  body = urllib2.urlopen(url).read()
  result = codec.loads(body)
  check_result = validation.is_valid(result)
  assert check_result['valid'] == 'yes'
  print(check_result)

if __name__ == "__main__":
    main()
