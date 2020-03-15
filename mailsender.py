# Sends an email with given content

import smtplib

def sendMail(receivers, subject, content) :
   sender = "me@example.com"
   message = """From: <{}>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: {}
{}
""".format(sender, '<' + '>,<'.join(receivers) + '>', subject, content)

   try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(sender, receivers, message)         
      print("Successfully sent email")
   except smtplib.SMTPException:
      print ("Error: unable to send email")