#!python
# -*- coding: utf-8 -*-

"""
code to send a mail from python
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#port = 465  # For SSL to Gmail
port = 587  # For starttls
smtp_server = "smtp.office365.com"
# port = 1025  # For SSL to local port
# smtp_server = "localhost"
sender_email = "oslo_venner@hotmail.com"
receiver_email = "testuser4development@gmail.com"
# password = input("Type your password and press enter: ")
password = "vennene"


# message = """\
# Subject: Hi there
#
# This message is sent from Python."""

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)


# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # This line only works when you connect to gmail
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
