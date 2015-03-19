#!python 

'''
  Monitor a given url and notify the website maintainer if the page fails to load 3 times in one minute.
'''

import logging
import time
import urllib2

api_url = 'http://restyourdroid.com/f/ae4564ss'  #  change to the url of your android device
url_to_monitor = 'http://restyourdroid.com' # change to the url you want to monitor


logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO)
failures = 0

while True:
  try:
    response = urllib2.urlopen(url_to_monitor)
    html = response.read()
    if 'Download the app now!' not in html:
      logging.info('Did not find target text in html.')
      failures += 1
    else:
      logging.info('Everything looks ok.')
      if failures>0:
	failures -= 1
  except Exception as exp:
    logging.exception('Received exception while fetching %s' % url_to_monitor)
    failures += 1
  
  if failures>=3:
    logging.info('3 failures in last minute, notifying maintainer...')
    urllib2.urlopen("%s%s" % (api_url, '/notify'), "title=Server down!&text=3 failures in last minute. Please check %s" % url_to_monitor).read()
    time.sleep(300)  # don't send a notification for 5 minutes
  else:
    time.sleep(20)  # check url again in 20 seconds