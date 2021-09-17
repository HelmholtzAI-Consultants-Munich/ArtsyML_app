import os
from artsyml import settings
from artsyml import ArtsyML
from .config import AdditionalConfig
import cv2
import time
from itertools import cycle


SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), 'static/snapshot')
SNAPSHOT_FILE_ORIGINAL = "original_frame.jpg"
SNAPSHOT_FILE_STYLED = "styled_frame.jpg"

class ArtsymlConnector():

    def __init__(self, artsyml_obj, styling_cycle_seconds):
        self.artsyml_obj = artsyml_obj
        self.if_camera_on = False        
        self.if_styling = False
        self.style_image = 0
        self.style_image_index = 0
        self.if_snaphot = False
        self.if_styling_cycle = False
        self.styling_cycle_seconds = styling_cycle_seconds

    def __str__(self):
        return f"""ArtsymlConnector params\n+
               if_camera_on: {self.if_camera_on}\n+
               if_styling: {self.if_styling}\n+
               if_snaphot: {self.if_snaphot}\n"""

    def camera_on(self):
        self.camera = cv2.VideoCapture(0)
        self.if_camera_on = True
        self.time_camera_on = time.time()

    def camera_off(self):
        self.stop_style()
        try:
            self.camera.release()
        except:
            pass
        self.if_camera_on = False

    def start_style(self, i = 0):
        self.style_image_index = i
        self.if_styling = True
        
    def stop_style(self):
        self.if_styling = False

    def delete_folder_contects(self, folder = SNAPSHOT_DIR):
        print("delete_snapshot_files() called")
        for f in os.listdir(folder):
            f_path = os.path.join(folder, f)
            print("delete f_path")
            os.remove(f_path)

    def take_snapshot(self):
        artsyml_connector.if_snaphot = True
        original_file_path = os.path.join(SNAPSHOT_DIR, SNAPSHOT_FILE_ORIGINAL)
        styled_file_path = os.path.join(SNAPSHOT_DIR, SNAPSHOT_FILE_STYLED)
        cv2.imwrite(original_file_path, self.frame)
        cv2.imwrite(styled_file_path, self.output_frame)
        self.camera_off()   

    def gen_frame(self):
        self.camera_on()     
        _start_time = time.time()
        _prev_capture_time = time.time()
        _style_number = len(self.artsyml_obj.style_images)
        _cycle_time_counter = 0
        style_number_cycle_gen = cycle(range(_style_number))
        print(f"gen_frame called (if_camera_on: {self.if_camera_on})")
        while self.if_camera_on:
            success, self.frame = self.camera.read()

            # mearing the time difference
            _capture_time = time.time()
            _delta_time = _capture_time - _prev_capture_time
            _prev_capture_time = _capture_time    
            _cycle_time_counter += _delta_time

            if self.if_styling:
                # if the the user changes the style image, then style image of
                # ArtsyML object should also be changed.

                # Cycling the syle images
                if self.if_styling_cycle and (self.styling_cycle_seconds <= _cycle_time_counter):
                    print("_cycle_time_counter", _cycle_time_counter)
                    _cycle_time_counter = 0
                    self.style_image_index = next(style_number_cycle_gen)

                if self.style_image_index != self.artsyml_obj.style_image_index:
                    self.artsyml_obj.set_style_image_by_index(self.style_image_index)

                self.output_frame = self.artsyml_obj.apply_style(frame = self.frame)
            else:
                self.output_frame = self.frame
            if self.if_snaphot:
                self.if_snaphot = False
                break
            ret, buffer = cv2.imencode('.jpg', self.output_frame)
            frame2 = buffer.tobytes()

            yield (b'--frame2\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n') 



artsyml_obj = ArtsyML()
style_files_paths = AdditionalConfig.style_images
artsyml_obj.read_style_images(style_files_paths)
artsyml_connector = ArtsymlConnector(artsyml_obj, AdditionalConfig.styling_cycle_seconds)

