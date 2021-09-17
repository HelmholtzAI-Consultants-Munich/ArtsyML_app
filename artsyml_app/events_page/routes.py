from flask import Blueprint
from flask import render_template
from .._artsyml_connector import artsyml_connector
events = Blueprint('events', __name__)

@events.route("/events", methods = ['GET', 'POST'])
def events_page():
    artsyml_connector.camera_off()
    artsyml_connector.delete_folder_contects()
    print("events called")
    return render_template('events.html', title = 'Events')
