#!python
# -*- coding: utf-8 -*-

"""
code to send a mail from python
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import smtplib, ssl

#port = 465  # For SSL to Gmail
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
# port = 1025  # For SSL to local port
# smtp_server = "localhost"
sender_email = "testuser4development@gmail.com"
receiver_email = "forstaafysikk@gmail.com"
# password = input("Type your password and press enter: ")
password = "JaB418W9JVFw"
message = """\
Subject: Hi there

This message is sent from Python."""




# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # This line only works when you connect to gmail
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)  # Authentication error -> you must make
    server.sendmail(sender_email, receiver_email, message)
