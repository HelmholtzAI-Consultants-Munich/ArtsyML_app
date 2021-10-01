from flask import Blueprint
from flask import render_template
from .. import artsyml_connector
events = Blueprint('events', __name__)

@events.route("/", methods = ['GET', 'POST'])
@events.route("/consultant_team_events", methods = ['GET', 'POST'])
def consultant_team_events():
    artsyml_connector.camera_off()
    artsyml_connector.delete_folder_contects()
    print("events called")
    return render_template('consultant_team_events.html', title = 'Events')


@events.route("/helmhotzai_events", methods = ['GET', 'POST'])
def helmhotzai_events():
    artsyml_connector.camera_off()
    artsyml_connector.delete_folder_contects()
    print("events called")
    return render_template('helmhotzai_events.html', title = 'Events')