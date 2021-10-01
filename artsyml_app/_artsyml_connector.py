import os
from artsyml import ArtsyML
from .config import AdditionalConfig
import cv2
import numpy as np
import time
from itertools import cycle

SNAPSHOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/snapshot'))
SNAPSHOT_FILE_ORIGINAL = "original_frame.jpg"
SNAPSHOT_FILE_STYLED = "styled_frame.jpg"
HELMHOLTZAI_WATERMARK = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/img/Helmholtz_AI_logo.png'))

class ArtsymlConnector():

    def __init__(self):
        self.__artsyml_objs = {}
        self.__style_images_abspath = {}
        self.__if_camera_on = False        
        self.__if_styling = False
        self.__if_snapshot = False
        self.__if_styling_cycle = False
        self.__active_artsyml_obj_name = None
        self.styling_cycle_seconds = AdditionalConfig.styling_cycle_seconds
        self.logo = cv2.imread(HELMHOLTZAI_WATERMARK)

    @property
    def style_images_abspath(self):
        return self.__style_images_abspath

    @property
    def if_camera_on(self):
        return self.__if_camera_on

    @property
    def if_styling(self):
        return self.__if_styling

    @property
    def if_snapshot(self):
        return self.__if_snasphot

    @property
    def if_styling_cycle(self):
        return self.__if_styling_cycle 

    def add_style(self, image_file, name):
        self.__artsyml_objs[name] = ArtsyML(image_file)

        self.__style_images_abspath = {
            name: atrsyml_obj.style_image_abspath 
            for (name, atrsyml_obj) 
            in self.__artsyml_objs.items() 
        }


    def add_styles_from_app_config(self):
        for (name, file) in AdditionalConfig.style_images.items():
            self.add_style(file, name)

    def change_style_by_name(self, name):
        self.__active_artsyml_obj = self.__artsyml_objs[name]
        self.__active_artsyml_obj_name = name
        print(f"style changed to -> {name}")

    def __str__(self):
        return f"""ArtsymlConnector status\n+
               style_images_abspath: {self.__style_images_abspath}\n+               
               if_camera_on: {self.__if_camera_on}\n+
               if_styling: {self.__if_styling}\n+
               if_snaphot: {self.__if_snapshot}\n"""


    def camera_on(self):
        # to make sure that we do not request to turn on a camera which already has been turned on
        self.camera_off()
        self.camera = cv2.VideoCapture(0)
        self.__if_camera_on = True
        self.__if_snapshot = False
        self.time_camera_on = time.time()

    def camera_off(self):
        self.stop_style()
        try:
            self.camera.release()
        except:
            pass
        self.__if_camera_on = False

    def start_style(self, style_name = None):
        if style_name == None:
            style_name = list(self.__artsyml_objs.keys())[0]
        self.change_style_by_name(style_name)
        self.__if_styling = True
        
    def stop_style(self):
        self.__if_styling = False

    def start_cycle(self):
        self.__if_styling = True    
        self.__if_styling_cycle = True

    def stop_cycle(self):
        self.__if_styling_cycle = False

    def delete_folder_contects(self, folder = SNAPSHOT_DIR):
        if not os.path.exists(folder):
            os.makedirs(folder)
        for f in os.listdir(folder):
            f_path = os.path.join(folder, f)
            os.remove(f_path)
    
    def _apply_watermark(self):
        self.watermarked_img = self.output_frame.copy()
        where_not_zero = np.where(self.logo[:,:]!=(0,0,0))
        self.watermarked_img[where_not_zero[0], where_not_zero[1]] = self.logo[where_not_zero[0],where_not_zero[1]]
        
    def take_snapshot(self):
        self.__if_snapshot = True
        original_file_path = os.path.join(SNAPSHOT_DIR, SNAPSHOT_FILE_ORIGINAL)
        styled_file_path = os.path.join(SNAPSHOT_DIR, SNAPSHOT_FILE_STYLED)

        self._apply_watermark()
        cv2.imwrite(original_file_path, self.frame)
        cv2.imwrite(styled_file_path, self.watermarked_img)
        self.camera_off()   

    def gen_frame(self):
        self.camera_on()     
        _start_time = time.time()
        _prev_capture_time = time.time()
        _cycle_time_counter = 0
        _last_style = self.__active_artsyml_obj_name
        style_number_cycle_gen = cycle(self.__artsyml_objs)
        while self.__if_camera_on:
            success, self.frame = self.camera.read()

            # mearing the time difference
            _capture_time = time.time()
            _delta_time = _capture_time - _prev_capture_time
            _prev_capture_time = _capture_time    
            _cycle_time_counter += _delta_time

            if self.__if_styling:
                # if the the user changes the style image, then style image of
                # ArtsyML object should also be changed.

                # Cycling the syle images
                if (self.__if_styling_cycle and (self.styling_cycle_seconds <= _cycle_time_counter)) or self.__active_artsyml_obj_name == None:
                    _cycle_time_counter = 0
                    _cycle_style_name = next(style_number_cycle_gen)
                    self.__active_artsyml_obj_name = _cycle_style_name


                if _last_style != self.__active_artsyml_obj_name:
                    self.change_style_by_name(self.__active_artsyml_obj_name)

                self.output_frame = self.__active_artsyml_obj.apply_style(frame = self.frame)
                _last_style = self.__active_artsyml_obj_name
            else:
                self.output_frame = self.frame
            
            print(f"success: {success} ,delta_time: {_delta_time}")
            if self.__if_snapshot:
                print("self.__if_snapshot", self.__if_snapshot)
                self.__if_snapshot = False
                self.camera_off()
                break
            ret, buffer = cv2.imencode('.jpg', self.output_frame)
            frame2 = buffer.tobytes()

            yield (b'--frame2\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n') 



