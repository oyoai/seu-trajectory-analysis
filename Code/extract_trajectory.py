import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

def extract_trial_info(filename, folder_name=""):
    name = filename.lower()
    position = "back" if "back" in name else "front" if "front" in name else "unknown"
    if "left" in folder_name.lower() or "left" in name:
        orientation = "left"
    elif "right" in folder_name.lower() or "right" in name:
        orientation = "right"
    elif "flipped" in name:
        orientation = "flipped"
    elif "normal" in name:
        orientation = "normal"
    else:
        orientation = "unknown"
    return position, orientation

def select_bbox(folder, label, scale=0.5):
    sample_file = next(f for f in os.listdir(folder) if f.endswith(".mp4"))
    sample_path = os.path.join(folder, sample_file)
    cap = cv2.VideoCapture(sample_path)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise Exception(f"could not read from {sample_path}")
    resized = cv2.resize(frame, None, fx=scale, fy=scale)
    bbox_scaled = cv2.selectROI(f"select ROI — {label}", resized, fromCenter=False)
    cv2.destroyAllWindows()
    return tuple(int(c / scale) for c in bbox_scaled)

def track_with_csrt(video_path, init_bbox):
    cap = cv2.VideoCapture(video_path)
    ok, first_frame = cap.read()
    if not ok:
        print(f"could not read {video_path}")
        return []
    tracker = cv2.TrackerCSRT_create()
    tracker.init(first_frame, init_bbox)
    trajectory = []
    frame_idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        ok, bbox = tracker.update(frame)
        if ok:
            x, y, w, h = bbox
            cx = int(x + w / 2)
            cy = int(y + h / 2)
        else:
            cx, cy = np.nan, np.nan
        trajectory.append((frame_idx, cx, cy))
        frame_idx += 1
    cap.release()
    return trajectory

def process_folder(video_folder, init_bbox):
    data = []
    for fname in tqdm(os.listdir(video_folder), desc=f"tracking in {video_folder}"):
        if not fname.endswith(".mp4"):
            continue
        video_path = os.path.join(video_folder, fname)
        trial_id = os.path.splitext(fname)[0]
        position, orientation = extract_trial_info(fname, video_folder)
        traj = track_with_csrt(video_path, init_bbox)
        for frame, x, y in traj:
            data.append({
                "trial": trial_id,
                "position": position,
                "orientation": orientation,
                "frame": frame,
                "x": x,
                "y": y
            })
    return pd.DataFrame(data)