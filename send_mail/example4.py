#!python
# -*- coding: utf-8 -*-

"""
Does not work
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import smtplib, ssl

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

smtp_server = "smtp.office365.com"
port = 587  # For starttls

sender_email = "oslo_venner@hotmail.com"  # sender's email address
receiver_email = "testuser4development@gmail.com"
password = "vennene"

# Create the base text message.
msg = EmailMessage()
msg['Subject'] = "Ayons asperges pour le déjeuner"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content("""\
Salut!

Cela ressemble à un excellent recipie[1] déjeuner.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Pepé
""")

# Add the html version.  This converts the message into a multipart/alternative
# container, with the original text message as the first part and the new html
# message as the second part.
asparagus_cid = make_msgid()
msg.add_alternative("""\
<html>
  <head></head>
  <body>
    <p>Salut!</p>
    <p>Cela ressemble à un excellent
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recipie
        </a> déjeuner.
    </p>
    <img src="cid:{asparagus_cid}" />
  </body>
</html>
""".format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
# note that we needed to peel the <> off the msgid for use in the html.

# Now add the related image to the html part.
with open("./assets/globe.jpg", 'rb') as img:
    msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                     cid=asparagus_cid)

# Make a local copy of what we are going to send.
with open('outgoing.msg', 'wb') as f:
    f.write(bytes(msg))

context = ssl.create_default_context()
# Send the message via local SMTP server.
with smtplib.SMTP(smtp_server, port) as s:
    s.starttls(context=context)
    s.login(sender_email, password)
    s.send_message(msg, sender_email, receiver_email)
