#!/bin/bash

[ -z "$RESERVE_AMERICA_VENV_BASE" ] && echo "Need to set RESERVE_AMERICA_VENV_BASE" && exit 1;

PATH="/usr/local/bin:${PATH}"
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TERMINAL_NOTIFIER=`which terminal-notifier`
NOTIF_ARGS="-sender com.google.Chrome -open $CAMPGROUND"

sites=`source $RESERVE_AMERICA_VENV_BASE/bin/activate && $BASE_DIR/scraper.py`

if [ -z "$sites" ] ; then
    if [ -e $TERMINAL_NOTIFIER ]; then
        # No sites available
        $TERMINAL_NOTIFIER $NOTIF_ARGS \
            -title "No Sites Available" \
            -message "No sites are yet available." \
            -timeout 5
    fi
else
    # We've got a site available
    if [ -e $TERMINAL_NOTIFIER ]; then
        # Send to the Nofication Center
        $TERMINAL_NOTIFIER $NOTIF_ARGS \
            -title "Campsites Are Available" \
            -message "$sites"
    fi
fi
