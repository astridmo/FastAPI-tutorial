#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

# Import smtplib for the actual sending function
import smtplib, ssl
port = 1025

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
with open("textfile.txt") as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'The contents of {"textfile.txt"}'
msg['From'] = "test4development@gmail.com"
msg['To'] = "forstaafysikk@gmail.com"

context = ssl.create_default_context()

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost', port)
s.starttls(context=context)
s.send_message(msg)
s.quit()