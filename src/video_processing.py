import pandas as pd
import os
from skimage.color import rgb2hsv
import numpy as np
import cv2

import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.detectors import ContentDetector


def get_dataframe(year, superdata, otherdata, datapath):
    df = pd.read_csv(
        ("%s/dataframe.csv" % (datapath)), index_col=0, keep_default_na=False
    )
    df = df[
        [
            os.path.exists(os.path.join(datapath, otherdata, str(i) + ".mp4"))
            for i in df.index
        ]
    ]
    df["filepath"] = [
        os.path.join(datapath, otherdata, str(i) + ".mp4") for i in df.index
    ]
    return df


def hsv_image(img):
    if img.ndim > 2:
        hsv_img = rgb2hsv(img)
        hue_img = hsv_img[:, :, 0]
        saturation_img = hsv_img[:, :, 1]
        value_img = hsv_img[:, :, 2]
    else:
        hue_img = np.zeros(img.shape)
        saturation_img = np.zeros(img.shape)
        value_img = img
    return hue_img, saturation_img, value_img


def averaged(img):
    return np.mean(img, axis=(0, 1))


def jumpcuts(video):
    video_manager = VideoManager([video])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list(video_manager.get_base_timecode())
    return len(scene_list)


def video_features(video, info):
    rawvideofeatures = pd.DataFrame()
    cap = cv2.VideoCapture(video)
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_count = 0
    while frame_count < num_frames:
        ret, frame = cap.read()
        if frame_count % 60 == 0:
            info = pd.Series()
            info.name = frame_count
            hue_img, saturation_img, value_img = hsv_image(frame)
            info["mean hue"] = averaged(hue_img)
            info["mean saturation"] = averaged(saturation_img)
            info["mean brightness"] = averaged(value_img)
            rawvideofeatures = rawvideofeatures.append(info)
        frame_count += 1
    cap.release()
    cv2.destroyAllWindows()
    videofeatures = info
    videofeatures.append(rawvideofeatures.mean())
    videofeatures["Number of Jump Cuts"] = jumpcuts(video)
    return videofeatures


def dataframe_processor(year, superdata, otherdata, datapath):
    rawdataframe = get_dataframe(year, superdata, otherdata, datapath)
    videodata = pd.DataFrame()
    info = pd.Series()
    for i in rawdataframe["filepath"]:
        print(i)
        info = pd.Series()
        info.name = i
        info = video_features(i, info)
        videodata = videodata.append(info)
    videodata.to_csv("%s/nonsuper_dataframe.csv" % (datapath))
    return videodata
