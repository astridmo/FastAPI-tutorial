#!python
# -*- coding: utf-8 -*-

"""
Send attachment (image or PDF. Some code must be changed (the not used lines are commented out).
Send to several receivers.
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import smtplib, ssl
import imghdr
from email.message import EmailMessage
import glob

smtp_server = "smtp.office365.com"
port = 587  # For starttls
#attachment_path = './assets/logo_alwayscargo.png'  #picture
attachment_path = './assets/test_pdf.pdf'

sender_email = "oslo_venner@hotmail.com"  # sender's email address
family = ["testuser4development@gmail.com"]  # List of of all recipients' email addresses
password = "vennene"


# Open the plain text file whose name is in textfile for reading.
with open("textfile.txt") as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())


msg['Subject'] = 'Our family reunion'
msg['From'] = sender_email
msg['To'] = ', '.join(family)
msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

# Open the files in binary mode.  Use imghdr to figure out the
# MIME subtype for each specific image.
for file in glob.glob(attachment_path):
    print(file)
    with open(file, 'rb') as fp:
        # img_data = fp.read()  # for attaching image
        pdf_data = fp.read()  # for attaching pdf
    # msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data))  # for attaching image
    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='example.pdf')  # for attaching PDF


context = ssl.create_default_context()
# Send the email via our own SMTP server.
with smtplib.SMTP(smtp_server, port) as s:
    s.starttls(context=context)
    s.login(sender_email, password)
    s.send_message(msg, sender_email, family)
