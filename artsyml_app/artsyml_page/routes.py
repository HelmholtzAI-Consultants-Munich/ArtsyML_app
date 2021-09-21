from artsyml_app.config import AdditionalConfig
from artsyml_app.artsyml_page.email_form import EmailForm
from flask import Blueprint
from flask import render_template, Response, url_for, flash, redirect, current_app
import os
import time
from ..utils import mail2user, abspath_to_relpath
from .email_form import EmailForm
from .. import artsyml_connector

artsyml = Blueprint('artsyml', __name__)

IMAGE_NAME_PREF = "style_image_"
STYLE_ONOFF = "style_onoff"
CYCLE_ONOFF = "cycle_onoff"
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), '../static/snapshot')
style_files_paths_in_app = {
    name: os.path.relpath(abspath, os.path.join(os.path.dirname(__file__), '../')) 
    for (name, abspath) 
    in artsyml_connector.style_images_abspath.items()
}






#@artsyml.route("/", methods = ['GET', 'POST'])
@artsyml.route("/artsyml", methods = ['GET', 'POST'])
def artsyml_page():
    artsyml_connector.delete_folder_contects()

    artsyml_connector.gen_frame()
    return render_template(
        'artsyml.html',  
        title = 'ArtsyML', 
        style_files_paths = style_files_paths_in_app,
        IMAGE_NAME_PREF = IMAGE_NAME_PREF,
        STYLE_ONOFF = STYLE_ONOFF
    )

@artsyml.route('/video_feed')
def video_feed():
    return Response(artsyml_connector.gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@artsyml.route('/styling_on_off',methods=['GET', 'POST'])
def style_on_off():
    #artsyml_connector.if_styling_cycle = False

    if artsyml_connector.if_styling:
        artsyml_connector.stop_style()
    else:
        artsyml_connector.start_style()
    
    return render_template(
        'artsyml.html', 
        title = 'ArtsyML', 
        style_files_paths = style_files_paths_in_app,
        IMAGE_NAME_PREF = IMAGE_NAME_PREF,
        STYLE_ONOFF = STYLE_ONOFF
    )


@artsyml.route('/styling_cycle_on_off',methods=['GET', 'POST'])
def styling_cycle_on_off():
    if artsyml_connector.if_styling_cycle:
        artsyml_connector.stop_cycle()
    else:
         artsyml_connector.start_cycle()
        
    return render_template(
        'artsyml.html', 
        title = 'ArtsyML', 
        style_files_paths = style_files_paths_in_app,
        IMAGE_NAME_PREF = IMAGE_NAME_PREF,
        STYLE_ONOFF = STYLE_ONOFF
    )


@artsyml.route('/set_style_image/<style_image>',methods=['GET', 'POST'])
def set_style_image(style_image = None):
    artsyml_connector.stop_cycle()
    style_image_commad = style_image.replace(IMAGE_NAME_PREF, "")
    if style_image_commad == STYLE_ONOFF:
        if artsyml_connector.if_styling:
            artsyml_connector.stop_style()
        else:
            artsyml_connector.start_style()
    else:
        artsyml_connector.start_style(style_image_commad)
    return render_template(
        'artsyml.html', 
        title = 'ArtsyML', 
        style_files_paths = style_files_paths_in_app,
        IMAGE_NAME_PREF = IMAGE_NAME_PREF,
        STYLE_ONOFF = STYLE_ONOFF
    )

@artsyml.route('/snapshot', methods = ['GET', 'POST'])
def snapshot():
    """
    The function renders the html of the snapshot after some delay to make sure that
    the snapshot images are stored at SNAPSHOT_DIR. If it takes moe than 5 second 
    a message is shown that the taking snapshot was not successfull.
    """
    try:
        artsyml_connector.take_snapshot()
    except:
        print("Taking a snapshot was unsuccessful!")
        flash(f"""At the moment, taking spanshot is not possible.\n""",'error')    

    form = EmailForm()
    artsyml_connector.camera_off()
    if form.validate_on_submit():
        mail2user(user_email = form.email.data)
        print("email was sent!")
        flash(f"""Dear user,\n 
                  the spanshot was sent to your email address successfully. You will be redirected to the video stream page in few seconds.\n""",'success')

        return redirect(url_for('artsyml.email_success'))
    else:   
        print(form.errors)
        return render_template(
            'artsyml_snapshot.html', 
            title = 'ArtsyML', 
            form = form
        )


@artsyml.route('/email_success', methods = ['GET', 'POST'])
def email_success():
    artsyml_connector.delete_folder_contects()
    return render_template("email_success.html")