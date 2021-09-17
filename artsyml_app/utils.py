import os
import cv2
import time
from flask_mail import Message
from .config import AdditionalConfig
from . import mail
from artsyml import settings
from artsyml import ArtsyML

SNAPSHOT_FILE_ORIGINAL = "original_frame.jpg"
SNAPSHOT_FILE_STYLED = "styled_frame.jpg"




def mail2user(user_email):  
    print("mail2user called, email sender", AdditionalConfig.app_email)
    print("mail2user called, email receiver", user_email)
    subject = "ArtsyML snapshot"
    body = f"Dear ArtsyML user,\n\n"+\
           f"Thank you for using the ArtsyML application. Please find in attachment the snapshot image.\n\n"+\
           f"Best regards,\n"+\
           f"Helmholtz AI,\n"

    msg = Message(subject = subject,
                  sender = AdditionalConfig.app_email,
                  recipients = [user_email], 
                  body = body)
    print("mail2user called, created")    
    for filename in [SNAPSHOT_FILE_ORIGINAL, SNAPSHOT_FILE_STYLED]:
        file_path = os.path.join(os.path.dirname(__file__), 'static/snapshot', filename)
        print(f"{filename}:{file_path}")
        with open(file_path,'rb') as fh:
            msg.attach(
                filename = filename,
                disposition = "attachment",
                content_type = "snapshot/jpg",
                data = fh.read()
            )
    print("mail2user called, attached")               
    mail.send(msg)
    print("mail2user called, sent")    


