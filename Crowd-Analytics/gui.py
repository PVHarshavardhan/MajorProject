import tkinter as tk
from tkinter import filedialog, messagebox
import json
from datetime import datetime

def load_config():
    """Load existing configuration or set defaults."""
    default_config = {
        "VIDEO_CONFIG": {
            "VIDEO_CAP": "",
            "START_TIME": datetime.now().isoformat()
        },
        "YOLO_CONFIG": {
            "WEIGHTS_PATH": "YOLOv7-tiny/yolov7-tiny.weights",
            "CONFIG_PATH": "YOLOv7-tiny/yolov7-tiny.cfg"
        },
        "SHOW_PROCESSING_OUTPUT": True,
        "SHOW_DETECT": True,
        "DATA_RECORD": True,
        "DATA_RECORD_RATE": 5,
        "SHOW_TRACKING_ID": True,
        "FRAME_SIZE": 1080,
        "TRACK_MAX_AGE": 3
    }
    
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = default_config
    
    return config

def save_config(config):
    """Save configuration to file."""
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

def select_video():
    """Open a file dialog to select the video file."""
    video_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4;*.avi"), ("All Files", "*.*")]
    )
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)

def submit_config():
    """Save the configuration and exit the GUI."""
    try:
        config["VIDEO_CONFIG"]["VIDEO_CAP"] = video_entry.get()
        config["VIDEO_CONFIG"]["START_TIME"] = datetime.now().isoformat()  
        config["SHOW_PROCESSING_OUTPUT"] = bool(show_processing_toggle_var.get())
        config["SHOW_DETECT"] = bool(show_detect_toggle_var.get())
        config["DATA_RECORD"] = bool(data_record_toggle_var.get())
        config["SHOW_TRACKING_ID"] = bool(show_tracking_toggle_var.get())
        config["DATA_RECORD_RATE"] = data_record_rate_var.get()
        config["FRAME_SIZE"] = int(frame_size_entry.get())

        save_config(config)
        messagebox.showinfo("Success", "Configuration saved successfully!")
        root.destroy()  
    except ValueError:
        messagebox.showerror("Error", "Frame size must be an integer.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration: {e}")

config = load_config()

root = tk.Tk()
root.title("Crowd Analysis and Movement Tracking for Real-Time CCTV Monitoring")
root.geometry("1000x700")  
root.configure(bg="#fced9f")


tk.Label(root, text="Crowd Analysis and Movement Tracking for Real-Time CCTV Monitoring",
         font=("Helvetica", 18, "bold"), bg="#fced9f").pack(pady=15)


tk.Label(root, text="Select the configuration settings", font=("Helvetica", 14), bg="#fced9f").place(x=20, y=60)



tk.Label(root, text="Select Video File:", font=("Helvetica", 12), bg="#fced9f").place(x=20, y=100)
video_entry = tk.Entry(root, width=80, font=("Helvetica", 10)) 
video_entry.place(x=180, y=100)  
video_entry.insert(0, config["VIDEO_CONFIG"].get("VIDEO_CAP", ""))
tk.Button(
    root, text="Browse", command=select_video, font=("Helvetica", 12), width=12, bg="#f5b562", fg="white"
).place(x=870, y=95) 


tk.Label(root, text="Frame Size:", font=("Helvetica", 12), bg="#fced9f").place(x=20, y=130)
frame_size_entry = tk.Entry(root, width=10)
frame_size_entry.place(x=180, y=130)
frame_size_entry.insert(0, config.get("FRAME_SIZE", 1080))


show_processing_toggle_var = tk.IntVar(value=int(config.get("SHOW_PROCESSING_OUTPUT", True)))
tk.Checkbutton(root, text="Show Processing Output", variable=show_processing_toggle_var, bg="#fced9f").place(x=20, y=190)

show_detect_toggle_var = tk.IntVar(value=int(config.get("SHOW_DETECT", True)))
tk.Checkbutton(root, text="Show Detections", variable=show_detect_toggle_var, bg="#fced9f").place(x=20, y=230)

data_record_toggle_var = tk.IntVar(value=int(config.get("DATA_RECORD", True)))
tk.Checkbutton(root, text="Enable Data Recording", variable=data_record_toggle_var, bg="#fced9f").place(x=20, y=270)

show_tracking_toggle_var = tk.IntVar(value=int(config.get("SHOW_TRACKING_ID", True)))
tk.Checkbutton(root, text="Show Tracking IDs", variable=show_tracking_toggle_var, bg="#fced9f").place(x=20, y=310)


data_record_rate_var = tk.IntVar(value=config.get("DATA_RECORD_RATE", 5))
tk.Label(root, text="Data Record Rate:", font=("Helvetica", 12), bg="#fced9f").place(x=20, y=370)
tk.Scale(root, from_=1, to=30, orient="horizontal", variable=data_record_rate_var, bg="#fced9f").place(x=180, y=360)


tk.Button(root, text="Save Configuration", command=submit_config, bg="green", fg="white", font=("Helvetica", 14)).place(x=800, y=630)


root.mainloop()
