Scrape Reserve America
======================

Scrape Reserve America for your favorite campsite

Usage
-----

Run the script with a few environment variables like so:

```sh
> pip install -r requirements.txt
> export CAMPGROUND="https://www.reserveamerica.com/camping/big-basin-redwoods-sp/r/campgroundDetails.do?contractCode=CA&parkId=120009"
> export LENGTH=2
> export DATE="04/14/2017"
> ./scraper.py
```

Then the scraper will search the given campsite for the date with the length of stay.

Or, you can set up the script to run under cron, and notify you on macOS using the provided [`cron.sh`](./cron.sh) script.

Note that the `cron.sh` wants you to run it inside of a python virtual environment by running with the env var `RESERVE_AMERICA_VENV_BASE` set to the path of your virtual environment.

An example is:

```cron
*/15 * * * * RESERVE_AMERICA_VENV_BASE='path/to/your/virtualenv' CAMPGROUND="https://www.reserveamerica.com/camping/big-basin-redwoods-sp/r/campgroundDetails.do?contractCode=CA&parkId=120009" LENGTH=2 DATE="04/14/2017" ~/reserve-america-scraper/cron.sh 2>&1 > /dev/null
```

Also, make sure that you have `terminal-notifier` installed. That's easy to do with Homebrew:

```sh
> brew install terminal-notifier
```

Twilio
------
When a reservation is found, you can use Twilio to send you an SMS. Just export the following env vars:
```sh
# Your Account SID from twilio.com/console
export TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Your Auth Token from twilio.com/console
export TWILIO_AUTH_TOKEN="your_auth_token"
# Your twilio phone number
export TWILIO_FROM_NUMBER="your_twilio_phone_number"
# Your personal phone number
export TWILIO_TO_NUMBER="your_personal_phone_number"
```

License
-------

[MIT](./LICENSE)
