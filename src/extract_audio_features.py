import numpy as np
import pandas as pd
import os
import ast
import librosa

from moviepy.editor import *
import speech_recognition as sr
from os import path
from pydub import AudioSegment
from sklearn.impute import SimpleImputer


def transcribe(mp3):

    sound = AudioSegment.from_mp3(mp3)
    sound.export("placehold.wav", format="wav")
    wave_file = "placehold.wav"

    god = sr.Recognizer()
    with sr.AudioFile(wave_file) as spoken:
        audio = god.record(spoken)
        tries = god.recognize_google(audio, show_all=True)
        if len(tries) == 0:
            transcript = "Fail"
        else:
            transcript = tries["alternative"][0]["transcript"]
    return transcript


def get_text_rates(dur, text):
    if text != "Fail":
        wordrate = len(text.split()) / dur
        charrate = len(text) / dur
    else:
        wordrate = np.nan
        charrate = np.nan
    return (wordrate, charrate)


def feature_extract(mp3_file, sb, wr, cr, n_mfcc=20):
    
    x, sr = librosa.load(mp3_file)
    
    spec_features = [librosa.feature.spectral_centroid, librosa.feature.spectral_bandwidth,
                 librosa.feature.spectral_contrast, librosa.feature.spectral_flatness,
                 librosa.feature.spectral_rolloff]
    
    raw_feats = [mp3_file, sb, wr, cr]
    # Add spectral features
    for f in spec_features:
        # Get raw features from function call
        raw_feat_f = f(x)
        # Add each feature one-by-one
        for row in raw_feat_f:
            avg = np.mean(row)
            raw_feats.append(avg)
            dev = np.std(row)
            raw_feats.append(dev)
            
    # MFCCs
    f = librosa.feature.mfcc
    raw_feat = f(x, sr, n_mfcc=n_mfcc)
    for row in raw_feat:
        avg = np.mean(row)
        raw_feats.append(avg)
        dev = np.std(row)
        raw_feats.append(dev)
        
    # Zero crossing rate
    f = librosa.feature.zero_crossing_rate
    raw_feat = f(x)
    for row in raw_feat:
        avg = np.mean(row)
        raw_feats.append(avg)
        dev = np.std(row)
        raw_feats.append(dev)
        
    # Chromagram    
    f = librosa.feature.chroma_stft
    raw_feat = f(x, sr)
    for row in raw_feat:
        avg = np.mean(row)
        raw_feats.append(avg)
        dev = np.std(row)
        raw_feats.append(dev)
    
    # Tonnetz
    f = librosa.feature.tonnetz
    raw_feat = f(x, sr)
    for row in raw_feat:
        avg = np.mean(row)
        raw_feats.append(avg)
        dev = np.std(row)
        raw_feats.append(dev)
        
    '''
    f = librosa.feature.fourier_tempogram
    raw_feat = f(x, sr)
    for row in raw_feat:
        raw_feats.append(row)
    '''  

    return raw_feats


########################


def extract(datapath, videodir, audiodir):

    feature_filename = "%s audio features.csv" % (videodir)
    feature_filename = os.path.join(datapath, feature_filename)
    data = pd.read_csv(feature_filename, index_col=0)

    directory = os.path.join(datapath, videodir)
    curraudiodir = os.path.join(directory, audiodir)
    if not os.path.exists(curraudiodir):
        os.mkdir(curraudiodir)
    for v in os.listdir(directory):
        vpath = os.path.join(directory, v)
        if os.path.isfile(vpath):
            video = VideoFileClip(vpath)
            audio = video.audio
            audioname = v[:-4] + ".mp3"
            audiofn = os.path.join(curraudiodir, audioname)
            audio.write_audiofile(audiofn)
    texts = list()
    for a in os.listdir(curraudiodir):
        file = os.path.join(curraudiodir, a)
        text = transcribe(file)
        texts.append(text)
    data["Text"] = texts

    words_per_sec = list()
    chars_per_sec = list()
    for i in range(len(data)):
        row = data.iloc[i]
        wps, cps = get_text_rates(row["commercial length (seconds)"], row["Text"])
        words_per_sec.append(wps)
        chars_per_sec.append(cps)
    data["WordsPerSec"] = words_per_sec
    data["CharsPerSec"] = chars_per_sec
    imp = SimpleImputer(missing_values=np.nan, strategy="mean")
    data["WordsPerSec"] = imp.fit_transform(data["WordsPerSec"].values.reshape(-1, 1))
    data["CharsPerSec"] = imp.fit_transform(data["CharsPerSec"].values.reshape(-1, 1))

    df = data[["WordsPerSec", "CharsPerSec"]]
    features = list()
    sb = 1.0
    for i in range(len(df)):
        a = os.listdir(curraudiodir)[i]
        audio = os.path.join(curraudiodir, a)
        wr = df["WordsPerSec"][i]
        cr = df["CharsPerSec"][i]
        sb = df["issuperbowl"][i]
        feat_array = feature_extract(audio, sb, wr, cr)
        features.append(feat_array)
    out = pd.DataFrame(features)
    
    out.to_csv(feature_filename)
