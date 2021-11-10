"""einen Platz um nicht im Restlichen Code immer rumschreiben zu müssen"""
""" Email PW: 4He3m4t#"""
"""testMaster@bietigheimer-htc.de"""

from email.mime.text import MIMEText
from email.header import Header
import smtplib

def testMail():

    msg = 'Rate mal wo ich die Email geschrieben habe, morgen 9:20Uhr los ?'
    subj = 'Hihi eine Email'
    frm = 'Absender <testMaster@bietigheimer-htc.de>'
    to = ['Alex Wengert <alexander.wengert@haw-hamburg.de',
          'Kranauge, Nils <Nils.Kranauge@haw-hamburg.de>',
          'Gildenstern, Lasse <Lasse.Gildenstern@haw-hamburg.de>'
          'Muhamed, Alshimaa Nabil Awaad Badawy <Alshimaa.Muhamed@haw-hamburg.de>',
          'Kaibour, Siham <Siham.Kaibour@haw-hamburg.de>',
          'Kompch, Maximilian Hans <Maximilian.Kompch@haw-hamburg.de>',
          'Boje, Maximilian <Maximilian.Boje@haw-hamburg.de>']

    toSoftware = ['AW <alexander.wengert@haw-hamburg.de','MB <Maximilian.Boje@haw-hamburg.de>']
    toMe = 'AW <alexander.wengert@haw-hamburg.de'
    toBoje = 'MB <Maximilian.Boje@haw-hamburg.de>'

    # Email zusammenstellen
    mail = MIMEText(msg, 'plain', 'utf-8')
    mail['Subject'] = Header(subj, 'utf-8')
    mail['From'] = frm
    mail['To'] = toBoje

    # Email versenden

    smtp = smtplib.SMTP('web03.dimait.de')
    smtp.starttls()
    smtp.login('testMaster@bietigheimer-htc.de', '4He3m4t#')
    smtp.sendmail(frm, [toBoje], mail.as_string())
    smtp.quit()

