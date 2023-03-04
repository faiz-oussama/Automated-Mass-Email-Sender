
from email.message import EmailMessage
import smtplib
import ssl

sender = input("Enter you e-mail adress :")
password = input("Enter your password :")
subject = "test"
receivers = []

question = input("Do you know the exact number of receivers ? (Y/N) :")
if (question == "Y"):
    number_of_receivers = int(input("Enter the number of receivers : "))
    for i in range(0,number_of_receivers):
        adress = input("E-mail : ")
        receivers.append(adress)

else:
    while True:
        adress = input("E-mail (or type exit to finish): ")
        if(adress == "exit"):
            break
        receivers.append(adress)
    

body = """hhhhhhhhhhhhhhhhh"""

email = EmailMessage()
email['from'] = sender 
email['to'] = receivers
email['subject'] = subject
email.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as smtp:
    smtp.login(sender,password)
    for i in range(len(receivers)):
        smtp.sendmail(sender,receivers[i],email.as_string())

