#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

# Import smtplib for the actual sending function
import smtplib, ssl
port = 587  # For starttls

# Import the email modules we'll need
from email.message import EmailMessage
smtp_server = "smtp.office365.com"
sender_email = "oslo_venner@hotmail.com"
receiver_email = "testuser4development@gmail.com"
password = "vennene"

# Open the plain text file whose name is in textfile for reading.
with open("textfile.txt") as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# msg = """Det er veldig rart at det ikke alltid fungerer...."""

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'The contents of {"textfile.txt"}'
msg['From'] = sender_email
msg['To'] = receiver_email

context = ssl.create_default_context()

# Send the message via our own SMTP server.
s = smtplib.SMTP(smtp_server, port)
s.starttls(context=context)
s.login(sender_email, password)
s.send_message(msg, sender_email, receiver_email)
s.quit()