#!/usr/bin/python2 

'''
  Ask your colleagues to order their pizza
'''

#  add correct urls here:
api_urls = { 'Koen': 'http://restyourdroid.com/f/ae4564ss',    
            'Franco': 'http://restyourdroid.com/f/565dfze',
            'Isabelle': 'http://restyourdroid.com/f/sdva545d'} 

title='Please choose your pizza'
text='Choose before 11am, please pay Franco.'
options= { 'Pizza type': ["Margerita","Hawaiian","BBQ Chicken","Veggie","Meat special","<custom>"], 'size': ["small","medium","large"]}


import json
import random
import time
import urllib
import urllib2

poll_id = random.randint(1,1000000)
api_params = { 'id': poll_id, 'title': title, 'text': text, 'options': json.dumps(options)}
encoded_api_params = urllib.urlencode(api_params)

# initiate poll:
polls_initiated = []
for user in api_urls:
    try:
        response = json.load(urllib2.urlopen("%s/poll_init" % api_urls[user], encoded_api_params))
        if response['success']:
            polls_initiated.append(user)
        else:
            print "Failed to initiate poll for %s" % user
    except Exception as exp:
        print "Failed to initiate poll for %s" % user


# get results:
results = {}
print "Initiated polll, collecting results"
while len(results)<len(polls_initiated):
    for user in polls_initiated:
        if user not in results:
            try:
                response = json.load(urllib2.urlopen("%s/poll_result?id=%s" % (api_urls[user], poll_id)))
                if response['success']:
                    data = response['data']
                    if data['result_available']:
                        if data['poll_ignored']:
                            results[user] = None
                        else:
                            results[user] = data['result']
                        print "\tCollected result for %s of %s users" % (len(results), len(polls_initiated))
                    else:
                        continue
                else:
                    print "Failed to get results for %s" % user
            except Exception as exp:
                print "Failed to get results for %s" % user
    time.sleep(2)

# print results
print "\nOrders"
for user in results:
    result = results[user]
    if result:
        print "\t%s would like a %s %s" % (user, result['size'], result['Pizza type'])
    else:
        print "\t%s does not want a pizza today" % user
