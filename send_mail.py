#!/usr/bin/env python
#
###########################################
#
# File: send_mail.py
# Author: Ra Inta
# Description:
# Created: September 13, 2019
# Last Modified: September 13, 2019
#
###########################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_creds import email_user, email_passwd

to_list = ["r_inta@hotmail.com"]
cc_list = []

subject = "Ra's Daily Alerts!"

body_text = """
This really is a test.
How the hell are you?
Great to see you man!

Ra
"""

body_html= """\
<html>
  <head></head>
  <body>
  <h1>This is the cool shit man</h1>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

def send_mail(to_list, subject="Ra's Daily Alerts!",
              body_text="Test message",
              body_html="",
              cc_list=[],
              from_addr=email_user, email_user=email_user,
              email_passwd=email_passwd,
              smtpserver="smtp.live.com:587"):
    """A function to send email, in MIME multi-part (plain-text and HTML).

    For example: to send to myself:
    send_mail(to_list, subject, body_text=body_text, body_html=body_html)
    """

    # Construct the message header
    message = MIMEMultipart('alternative')
    message['From'] = from_addr
    message['To'] = ','.join(to_list)
    message['Cc'] = ','.join(cc_list)
    message['Subject'] = subject

    # Append the body text
    message.attach(MIMEText(body_text, 'plain'))
    message.attach(MIMEText(body_html, 'html'))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(email_user, email_passwd)
    problems = server.sendmail(from_addr, to_list, message.as_string())
    server.quit()


###########################################
# End of send_mail.py
###########################################
