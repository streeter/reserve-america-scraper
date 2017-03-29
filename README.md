Scrape Reserve America
======================

Scrape Reserve America for your favorite campsite

Usage
-----

Run the script with a few environment variables like so:

```sh
> export CAMPGROUND="https://www.reserveamerica.com/camping/big-basin-redwoods-sp/r/campgroundDetails.do?contractCode=CA&parkId=120009"
> export LENGTH=2
> export DATE="04/14/2017"
> ./scraper.py
```

Then the scraper will search the given campsite for the date with the length of stay.

Or, you can set up the script to run under cron, and notify you on macOS using the provided [`cron.sh`](./cron.sh) script. An example is:

```cron
0/15 * * * * CAMPGROUND="https://www.reserveamerica.com/camping/big-basin-redwoods-sp/r/campgroundDetails.do?contractCode=CA&parkId=120009" LENGTH=2 DATE="04/14/2017" /Users/streeter/reserve-america-scraper/cron.sh 2>&1 > /dev/null
```

License
-------

[MIT](./LICENSE)
