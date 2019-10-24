#!/usr/bin/env python
#
###########################################
#
# File: craigs_alert.py
# Author: Ra Inta
# Description:
# Created: September 15, 2019
# Last Modified: September 27, 2019 R.I.
#
###########################################

import argparse

import requests
from bs4 import BeautifulSoup

import datetime as dt

# Additional project files
from send_mail import send_mail
from email_creds import email_user, email_passwd
from get_craig_html import query_join, craigs_topic_to_html


# Get optional input parameters
parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="User name")
parser.add_argument("-t", "--add-topic", help="Additional Craigslist topic")
parser.add_argument("-z", "--zip-code", help="Zip code")

args = parser.parse_args()


if not args.username:
    user_name = 'ra'
else:
    user_name = args.username.lower()

if not args.zip_code:
    zip_code = 78749
else:
    zip_code = args.zip_code

print(f"Running daily alerts for {user_name}, with additional topics {args.add_topic}")

# Set today's date
dt_today = dt.date.today()

##################################################
# Generate Craigslist category codes
##################################################

cat_code = {}

cat_code["computer gigs"] = "computer-gigs", "cpg", query_join("is_paid=all", "postedToday=1")
cat_code["software jobs"] = "software-qa-dba-etc", "sof", query_join("postedToday=1")
cat_code["film jobs"] = "tv-film-video-radio", "tfr", query_join("postedToday=1")
cat_code["creative gigs"] = "creative-gigs", "crg", query_join("is_paid=all", "postedToday=1")
cat_code["business"] = "business", "bfa" , query_join("query=desk", "postedToday=1")
cat_code["free stuff"] = "free-stuff", "zip", query_join("postedToday=1", "search_distance=10", f"postal={zip_code}")
cat_code["web jobs"] = "web-html-info-design", "web", query_join("postedToday=1")
cat_code["writing jobs"] = "writing-editing", "wri", query_join("postedToday=1")

# Cars
cat_code["cars"] = "cars-trucks", "cta", query_join("min_price=1200", "max_price=4500", "postedToday=1",
                                                    "search_distance=45", "postal=78749", "-bmw", "-ford",
                                                    "-dodge", "-saab", "-lexus", "-mercedes", "-volvo")

# Send out upcoming Saturday and Sunday garage sales if today is Thursday,
# Friday or Saturday
if dt_today.strftime("%A") in ["Thursday", "Friday", "Saturday"]:
    # Get this coming Saturday and Sunday's dates
    days_to_add = (5 - dt_today.weekday()) % 7
    str_sat = (dt_today + dt.timedelta(days=days_to_add)).strftime("%Y-%m-%d")
    str_sun = (dt_today + dt.timedelta(days=days_to_add + 1)).strftime("%Y-%m-%d")
    cat_code["garage sale (sat)"] = "garage-moving-sales", "gms", query_join("search_distance=5", "postal=78749", f"sale_date={str_sat}")
    cat_code["garage sale (sun)"] = "garage-moving-sales", "gms", query_join("search_distance=5", "postal=78749", f"sale_date={str_sun}")


##################################################


# Get HTML header

html_header = """
<html>
<head>
<title>Craigslist Daily Alert</title>
<style>

h3 {
    color: grey;
    font-size: 16pt !important;
    }

h2.warning {
    color: red;
    font-size: 18pt !important;
    }

p.odd_para:nth-child(odd) {
background: #CCC
    }

tr.odd_row:nth-child(odd) {
background: #CCC
    }

</style>
</head>

"""


def output_full_html(keys, cat_code, dt_today, html_header):
    """"""
    output_full_html = html_header
    output_full_html += "\n<body>\n"
    for key in keys:
        output_full_html += craigs_topic_to_html(key, cat_code)
    output_full_html += "\n<footer>\n"
    #output_full_html += dt_today.strftime("Generated, with love, on %A, %d of %B, %Y. \U0001F63B")
    output_full_html += "\n</footer>\n"
    output_full_html += "\n</body>\n"
    output_full_html += "\n</html>\n"
    return output_full_html


def dump_html_to_file(f_name, html):
    """docstring for dump_html_to_file"""
    with open(f_name, "w") as file_handle:
        file_handle.write(html)


##################################################
# Construct and send the emails
##################################################

search_keys = {}
search_keys['ra'] = cat_code.keys()
search_keys['beth'] = "cars", "garage sale (sat)", "garage sale (sun)"
search_keys['test'] = "free stuff", "cars", "computer gigs"

def get_search_code(user_name, search_keys, cat_code):
    """docstring for get_search_code"""
    return {k: cat_code[k] for k in search_keys[user_name] if k in cat_code}

search_code = {k: cat_code[k] for k in search_keys[user_name] if k in cat_code}

# Keep email addresses as lists at the moment; we may want to combine batch
# emails later
email_addr = {'ra': ["r_inta@hotmail.com"]}

email_addr['beth'] = ["elizabethkoehn@hotmail.com"]

# Generate subject and output HTML
alert_subject = f"Ra's Daily Alerts for {dt_today.strftime('%A')}!"

output_html = output_full_html(search_keys[user_name], search_code, dt_today, html_header)

#dump_html_to_file("test_yet_another_test.html", test_html)

# Send email of HTML format:
try:
    send_mail(email_addr[user_name], subject=alert_subject, body_html=output_html)
    print(f"Sent daily email to {user_name} at {email_addr[user_name]} with the topics {search_keys[user_name]} on {dt_today.strftime('%Y-%m-%d')}")
except Error as e:
    print(f"Warning! Email not sent because of error {e}")


###########################################
# End of craigs_alert.py
###########################################
