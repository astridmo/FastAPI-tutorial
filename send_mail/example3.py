#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

# Import smtplib for the actual sending function
import smtplib, ssl

# And imghdr to find the types of our images
import imghdr

# Here are the email package modules we'll need
from email.message import EmailMessage
from PIL import Image
import glob
image_list = []
for filename in glob.glob('./assets/logo_alwayscargo.png'): #assuming gif
    im=Image.open(filename)
    image_list.append(im)
    print(image_list)

sender_email = "oslo_venner@hotmail.com"
family = ["testuser4development@gmail.com"]
smtp_server = "smtp.office365.com"
password = "vennene"
port = 587  # For starttls

# Create the container email message.
msg = EmailMessage()
msg['Subject'] = 'Our family reunion'
# me == the sender's email address
# family = the list of all recipients' email addresses
msg['From'] = sender_email
msg['To'] = ', '.join(family)
msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

# Open the files in binary mode.  Use imghdr to figure out the
# MIME subtype for each specific image.
for file in glob.glob('./assets/logo_alwayscargo.png'):
    print(file)
    with open(file, 'rb') as fp:
        img_data = fp.read()
    msg.add_attachment(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))

context = ssl.create_default_context()
# Send the email via our own SMTP server.
with smtplib.SMTP(smtp_server, port) as s:
    s.starttls(context=context)
    s.login(sender_email, password)
    s.send_message(msg, sender_email, family)
