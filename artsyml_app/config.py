# -*- coding: utf-8 -*-
import json
import os

with open('config.json') as config_file: #'/etc/config.json'
	config = json.load(config_file)

class BuiltinConfig:
    SECRET_KEY = config.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    MAIL_SERVER = 'mailout.helmholtz-muenchen.de'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config.get('MAIL_USERNAME')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')

class AdditionalConfig:
    app_email = config.get('MAIL_USERNAME')
    style_images = config.get('style_images')
    styling_cycle_seconds = config.get('styling_cycle_seconds')
    """
    snapshot_dir = os.path.abspath
    original_frame_snapshot_filename = config.get('original_frame_snapshot_filename')
    styled_frame_snapshot_filename = config.get('styled_frame_snapshot_filename')
    """
    
