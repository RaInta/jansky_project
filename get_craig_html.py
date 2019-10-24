#!/usr/bin/env python

###########################################
# File: get_craig_html.py
# Author: Ra Inta
# Description: Inspirational suggestions for 'Exercises for Web Scraping'
#
# Created: August 28, 2019
# Last Modified: August 28, 2019, R.I.
###########################################


import requests
from bs4 import BeautifulSoup

import datetime as dt

# Additional project files
from send_mail import send_mail
from email_creds import email_user, email_passwd


def query_join(*query_list):
    """Takes a bunch of separate string arguments and binds them into
    a query format, i.e. appended with a '&' between each (unless it's
    a single query)."""
    return "&".join(query_list)


def get_craigs_full_uri(topic, cat_code, full_browse=False, query_string="", location="austin"):
    """Takes a Craigslist category code and coverts it to a full URI.
    The cat_code structure is a dictionary defined by topic names as
    keys. Each value is a three-element tuple, including the long- and
    abbreviated-search term, plus the specific query for that topic.

    Note there is a switch between the default browsing address and that
    for the 'posted daily' address. The former has a '/d/' and full name
    for the category, plus a TLI (three-letter initialism) whilst the latter
    is prepended by '/search/' then the TLI only, plus a 'postedToday=1' flag."""

    url_base = f"https://{location}.craigslist.org"
    # Over-ride dictionary version of query if explicitly specified
    if query_string:
        cat_code[topic] = query_string
    if full_browse:
        return url_base + "/d/" + cat_code[topic][0] + "/search/" + cat_code[topic][1]
    else:
        return url_base + "/search/" + cat_code[topic][1] + "?" + cat_code[topic][2]


#def craigs_topic_to_html(topic, cat_code):
#    """docstring for craigs_topic_to_html"""
#    url_topic = get_craigs_full_uri(topic, cat_code)
#    craigs = requests.get(url_topic)
#    if craigs.status_code == 200:
#        craigs_soup = BeautifulSoup(craigs.text, "html.parser")
#        topic_title = craigs_soup.title.string.title()
#        # Craigslist links thankfully have a specific CSS class attribute:
#        topic_url_list = craigs_soup.find_all("a", class_="result-title hdrlnk")
#        # Generate some pretty-printed HTML
#        title_pretty = "<h3>" + topic_title + "</h3>\n"
#        topic_url_pretty = [f"<p class='odd_para'>{str(x)}</p>\n" for x in topic_url_list]
#        html_body = title_pretty
#        html_body += "\n".join(topic_url_pretty)
#        html_body += "\n<hr>\n"
#        if not len(topic_url_list):
#            html_body = ""
#        return html_body
#    else:
#        out_str = f"Warning! Connection to Craigslist topic {topic} was refused with error code {craigs.status_code}"
#        print(out_str)
#        return "<h2 class='warning'>" + out_str + "</h2>\n"


def craigs_topic_to_html(topic, cat_code):
    """docstring for craigs_topic_to_html"""
    url_topic = get_craigs_full_uri(topic, cat_code)
    url_browse = get_craigs_full_uri(topic, cat_code, full_browse=True)
    craigs = requests.get(url_topic)
    if craigs.status_code == 200:
        craigs_soup = BeautifulSoup(craigs.text, "html.parser")
        topic_title = craigs_soup.title.string.title()
        # Craigslist links thankfully have a specific CSS class attribute:
        topic_url_list = craigs_soup.find_all("a", class_="result-title hdrlnk")
        # The price information is often found in two locations, but only
        # (and somewhat at best) reliably as a child of 'result-meta'
        potential_prices = [x.find("span", class_="result-price") for x in craigs_soup.find_all("span", class_="result-meta")]
        price_list = [x.string if x is not None else '' for x in potential_prices]
        # Generate some pretty-printed HTML
        title_pretty = "<h3>" + topic_title + "</h3>\n"
        topic_url_pretty = [f"\t<td>{str(x)}</td>\n\t<td>{y}</td>\n" for x, y in zip(topic_url_list, price_list)]
        # Create HTML body
        html_body = title_pretty
        html_body += "\n<table>\n<tbody>\n<tr class='odd_row'>"
        html_body += "\n</tr>\n<tr class='odd_row'>".join(topic_url_pretty)
        html_body += f"</tr>\n</table>\n<p><b><a href='{url_browse}'>Browse all {topic}</a></b></p>"
        html_body += "\n<hr>\n"
        if not len(topic_url_list):
            html_body = ""
        return html_body
    else:
        out_str = f"Warning! Connection to Craigslist topic {topic} was refused with error code {craigs.status_code}"
        print(out_str)
        return "<h2 class='warning'>" + out_str + "</h2>\n"


###########################################
# End of get_craig_html.py
###########################################
