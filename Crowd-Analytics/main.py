import os
import sys
import json
import time
import cv2
import csv
import datetime
from video_process import video_process
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort import generate_detections as gdet
from datetime import datetime
import subprocess

def load_config():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as json_file:
                config = json.load(json_file)
            
            # Convert the string back to datetime objects
            config["VIDEO_CONFIG"]["START_TIME"] = datetime.fromisoformat(config["VIDEO_CONFIG"]["START_TIME"])
            config["RE_START_TIME"] = datetime.strptime(config["RE_START_TIME"], "%H:%M:%S").time()
            config["RE_END_TIME"] = datetime.strptime(config["RE_END_TIME"], "%H:%M:%S").time()
            
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return None
    else:
        print("Config file not found, invoking GUI for configuration.")
        return None  

def start_gui():
    # Launch the GUI using subprocess
    subprocess.run(["python", "gui.py"])

# Function to proceed with video processing after settings are loaded
def process_video(config):
    VIDEO_CONFIG = config["VIDEO_CONFIG"]
    YOLO_CONFIG = config["YOLO_CONFIG"]
    SHOW_PROCESSING_OUTPUT = config["SHOW_PROCESSING_OUTPUT"]
    DATA_RECORD_RATE = config["DATA_RECORD_RATE"]
    FRAME_SIZE = config["FRAME_SIZE"]
    TRACK_MAX_AGE = config["TRACK_MAX_AGE"]

    if FRAME_SIZE > 1920:
        print("Frame size is too large!")
        quit()
    elif FRAME_SIZE < 480:
        print("Frame size is too small! You won't see anything")
        quit()

    # Read from video
    IS_CAM = VIDEO_CONFIG["IS_CAM"]
    cap = cv2.VideoCapture(VIDEO_CONFIG["VIDEO_CAP"])

    if not cap.isOpened():
        print(f"Error: Couldn't read video stream from file '{VIDEO_CONFIG['VIDEO_CAP']}'")
        quit()

    # Load YOLOv7-tiny weights and config
    WEIGHTS_PATH = YOLO_CONFIG["WEIGHTS_PATH"]
    CONFIG_PATH = YOLO_CONFIG["CONFIG_PATH"]

    # Load the YOLOv7-tiny pre-trained COCO dataset 
    net = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)
    # Set the preferable backend to CPU since we are not using GPU
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Get the names of all the layers in the network
    ln = net.getLayerNames()
    # Filter out the layer names we don't need for YOLO
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # Tracker parameters
    max_cosine_distance = 0.7
    nn_budget = None

    # Initialize deep sort object
    if IS_CAM: 
        max_age = VIDEO_CONFIG["CAM_APPROX_FPS"] * TRACK_MAX_AGE
    else:
        max_age = DATA_RECORD_RATE * TRACK_MAX_AGE
        if max_age > 50:
            max_age = 50
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric, max_age=max_age)

    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')

    movement_data_file = open('processed_data/movement_data.csv', 'w') 
    crowd_data_file = open('processed_data/crowd_data.csv', 'w')
    movement_data_writer = csv.writer(movement_data_file)
    crowd_data_writer = csv.writer(crowd_data_file)

    if os.path.getsize('processed_data/movement_data.csv') == 0:
        movement_data_writer.writerow(['Track ID', 'Entry time', 'Exit Time', 'Duration','Positions For Tracking'])
    if os.path.getsize('processed_data/crowd_data.csv') == 0:
        crowd_data_writer.writerow(['Time', 'Human Count'])

    START_TIME = time.time()
    start_time_datetime = datetime.fromtimestamp(START_TIME)  # Convert float to datetime
    start_time_datetime = start_time_datetime.strftime('%d/%m/%Y %H:%M:%S')

    try:
        processing_FPS = video_process(cap, FRAME_SIZE, net, ln, encoder, tracker, movement_data_writer, crowd_data_writer)
        print(processing_FPS)
    except ZeroDivisionError:
        print("Error: ZeroDivisionError occurred. The video file may not be properly read.")
        quit()

    cv2.destroyAllWindows()
    movement_data_file.close()
    crowd_data_file.close()

    END_TIME = time.time()
    PROCESS_TIME = END_TIME - START_TIME

    print("Time elapsed: ", PROCESS_TIME)

    if IS_CAM:
        print("Processed FPS: ", processing_FPS)
        VID_FPS = processing_FPS
        DATA_RECORD_FRAME = 1
    else:
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if PROCESS_TIME > 0:
            print("Processed FPS: ", round(total_frames / PROCESS_TIME, 2))
            VID_FPS = cap.get(cv2.CAP_PROP_FPS)
        else:
            VID_FPS = 0
            print("Error: Processing time is zero, cannot calculate FPS.")
        DATA_RECORD_FRAME = int(VID_FPS / DATA_RECORD_RATE) if VID_FPS > 0 else 0
        START_TIME = VIDEO_CONFIG["START_TIME"]
        time_elapsed = round(total_frames / VID_FPS) if VID_FPS > 0 else 0
        END_TIME = START_TIME + datetime.timedelta(seconds=time_elapsed)

    cap.release()

    end_time_formatted = datetime.fromtimestamp(END_TIME)  
    end_time_formatted = end_time_formatted.strftime('%d/%m/%Y %H:%M:%S')
    print(end_time_formatted)

    video_data = {
        "IS_CAM": IS_CAM,
        "DATA_RECORD_FRAME": DATA_RECORD_FRAME,
        "VID_FPS": VID_FPS,
        "PROCESSED_FRAME_SIZE": FRAME_SIZE,
        "TRACK_MAX_AGE": TRACK_MAX_AGE,
        "START_TIME": start_time_datetime,
        "END_TIME": end_time_formatted
    }
    print(video_data)

    def datetime_handler(x):
        if type(x) == datetime.datetime:  
            return x.isoformat()
        raise TypeError("Unknown type")

    with open('processed_data/video_data.json', 'w') as video_data_file:
        json.dump(video_data, video_data_file, default=datetime_handler)

# Main execution starts here
start_gui()

# Proceed with video processing
config = load_config()

if config:
    process_video(config)
else:
    print("Error: Configuration not found.")