#!/usr/bin/env python

import os

import mechanize
from bs4 import BeautifulSoup

# Configuration
date = os.environ['DATE']
length_of_stay = os.environ['LENGTH']
url = os.environ['CAMPGROUND']

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 '
              'Safari/537.36')

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
    print "On {}, found available sites: {}".format(date, ', '.join(hits))
