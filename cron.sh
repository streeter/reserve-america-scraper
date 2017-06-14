#!/bin/bash

# Check for an interactive shell
if [ -z "$PS1" ]; then
    INTERACTIVE=0
else
    INTERACTIVE=1
fi

PATH="/usr/local/bin:${PATH}"
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TERMINAL_NOTIFIER=`which terminal-notifier`
NOTIF_ARGS="-sender com.google.Chrome -open $CAMPGROUND"

if [ -z "$RESERVE_AMERICA_VENV_BASE" ]; then
    [ "${INTERACTIVE}" -eq "1" ] && echo "Not running in a virtualenv, this is not recommended! Set up your virtualenv use it by setting RESERVE_AMERICA_VENV_BASE"
    sites=`$BASE_DIR/scraper.py`
else
    sites=`source $RESERVE_AMERICA_VENV_BASE/bin/activate && $BASE_DIR/scraper.py`
fi

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
