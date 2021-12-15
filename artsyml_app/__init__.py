#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_mail import Mail
from .config import BuiltinConfig, AdditionalConfig
from flask_bcrypt import Bcrypt
from ._artsyml_connector import ArtsymlConnector
# added C-hack
#from artsyml import ArtsyML

bcrypt = Bcrypt()

mail = Mail()

artsyml_connector = ArtsymlConnector()
artsyml_connector.add_styles_from_app_config()

def create_app(config_class = BuiltinConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)    
    bcrypt.init_app(app)
    mail.init_app(app)


    from .artsyml_page.routes import artsyml
    from .events_page.routes import events

    app.register_blueprint(artsyml)
    app.register_blueprint(events)

    return app

