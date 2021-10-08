import os
import time
from flask_mail import Message
from flask import current_app
from .config import AdditionalConfig
from . import mail

SNAPSHOT_FILE_ORIGINAL = "original_frame.jpg"
SNAPSHOT_FILE_STYLED = "styled_frame.jpg"

def abspath_to_relpath(abspath):
    return os.path.relpath(abspath, current_app.root_path)

def mail2user(user_email):  
    print("mail2user called, email receiver:", user_email)
    subject = "ArtsyML snapshot"
    body = f"Dear ArtsyML user,\n\n"+\
           f"Thank you for using the ArtsyML application. Please find the snapshot image attached.\n"+\
           f"Feel free to use the pictures for your own purposes, but please note that the rendered version may only be used without modifications on a non-commercial basis\n\n"+\
           f"Best regards,\n"+\
           f"Helmholtz AI,\n"

    msg = Message(subject = subject,
                  sender = AdditionalConfig.app_email,
                  recipients = [user_email], 
                  body = body)
    print("mail2user called, created")    
    for filename in [SNAPSHOT_FILE_ORIGINAL, SNAPSHOT_FILE_STYLED]:
        file_path = os.path.join(os.path.dirname(__file__), 'static/snapshot', filename)
        print(f"'{filename}': attaching.")

        with open(file_path,'rb') as fh:
            msg.attach(
                filename = filename,
                disposition = "attachment",
                content_type = "snapshot/jpg",
                data = fh.read()
            )
        print(f"'{filename}': attached.")

    mail.send(msg)
    print("mail2user called, sent")    


