import datetime

VIDEO_CONFIG = {
	"VIDEO_CAP" : "samples/people.mp4",
	"IS_CAM" : True,
	"CAM_APPROX_FPS": 3,
	"HIGH_CAM": False,
	"START_TIME": datetime.datetime(2024, 7, 9, 0, 0, 0, 0)
}


YOLO_CONFIG = {
	"WEIGHTS_PATH" : "YOLOv7-tiny/yolov7-tiny.weights",
	"CONFIG_PATH" : "YOLOv7-tiny/yolov7-tiny.cfg"
}

SHOW_PROCESSING_OUTPUT = True
SHOW_DETECT = True
DATA_RECORD = True
DATA_RECORD_RATE = 5
RE_CHECK = False
RE_START_TIME = datetime.time(0,0,0) 
RE_END_TIME = datetime.time(23,0,0)
SD_CHECK = False
SHOW_VIOLATION_COUNT = False
SHOW_TRACKING_ID = True
SOCIAL_DISTANCE = 50
ABNORMAL_CHECK = True
ABNORMAL_MIN_PEOPLE = 5
ABNORMAL_ENERGY = 1866
ABNORMAL_THRESH = 0.66
MIN_CONF = 0.3
NMS_THRESH = 0.2
FRAME_SIZE = 1080
TRACK_MAX_AGE = 3


