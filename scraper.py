#!/usr/bin/env python

import os
import sys

try:
    import mechanize
    from bs4 import BeautifulSoup
    from twilio.rest import Client
except ImportError:
    print('Unable to import necessary packages!')
    sys.exit(-1)

# Configuration
date = os.environ['DATE']
length_of_stay = os.environ['LENGTH']
url = os.environ['CAMPGROUND']
# Optional Twilio configuration
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_from_number = os.environ.get('TWILIO_FROM_NUMBER')
twilio_to_number = os.environ.get('TWILIO_TO_NUMBER')
has_twilio = twilio_account_sid and twilio_auth_token and twilio_from_number and twilio_to_number

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 '
              'Safari/537.36')

def send_sms(message):
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        to=twilio_to_number,
        from_=twilio_from_number,
        body=message)

def onHit(date, hits):
    message = "On {}, found available sites: {}".format(date, ', '.join(hits))
    if has_twilio:
        message = "{}. {}".format(message, url)
        send_sms(message)
    else:
        print message

def run():
    hits = []

    # Create browser
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', USER_AGENT)]
    br.open(url)

    # Fill out form
    br.select_form(nr=0)
    br.form.set_all_readonly(False)  # allow changing the .value of all controls
    br.form["campingDate"] = date
    br.form["lengthOfStay"] = length_of_stay
    response = br.submit()

    # Scrape result
    soup = BeautifulSoup(response, "html.parser")
    table = soup.findAll("table", {"id": "shoppingitems"})

    if table:
        rows = table[0].findAll("tr", {"class": "br"})

        for row in rows:
            cells = row.findAll("td")
            l = len(cells)
            label = cells[0].findAll("div", {"class": "siteListLabel"})[0].text
            is_ada = bool(cells[3].findAll("img", {"title": "Accessible"}))
            is_group = bool('GROUP' in cells[2].text)
            status = cells[l - 1].text
            if not is_group and not is_ada and status.startswith('available'):
                hits.append(label)

    if hits:
        onHit(date, hits)

run()
