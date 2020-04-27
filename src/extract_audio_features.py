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
                transcript = 'Fail'
            else:
                transcript = tries['alternative'][0]['transcript']
    return transcript


def get_text_rates(dur, text):
    if text != 'Fail':
        wordrate = len(text.split()) / dur
        charrate = len(text) / dur
    else:
        wordrate = np.nan
        charrate = np.nan
    return (wordrate, charrate)


def feature_extract(mp3_file, wordrate, charrate, sb=1.0, n_mfcc=20):
    
    x, sr = librosa.load(mp3_file)
    
    spec_features = [librosa.feature.spectral_centroid, librosa.feature.spectral_bandwidth,
                 librosa.feature.spectral_contrast, librosa.feature.spectral_flatness,
                 librosa.feature.spectral_rolloff]
    
    raw_feats = list()
    # Add spectral features
    for f in spec_features:
        # Get raw features from function call
        raw_feat_f = f(x)
        # Add each feature one-by-one
        for row in raw_feat_f:
            raw_feats.append(row)
            
    # MFCCs
    f = librosa.feature.mfcc
    raw_feat = f(x, sr, n_mfcc=n_mfcc)
    for row in raw_feat:
        raw_feats.append(row)
        
    # Zero crossing rate
    f = librosa.feature.zero_crossing_rate
    raw_feat = f(x)
    for row in raw_feat:
        raw_feats.append(row)
        
    # Chromagram    
    f = librosa.feature.chroma_stft
    raw_feat = f(x, sr)
    for row in raw_feat:
        raw_feats.append(row)
    
    # Tonnetz
    f = librosa.feature.tonnetz
    raw_feat = f(x, sr)
    for row in raw_feat:
        raw_feats.append(row)
        
    '''
    f = librosa.feature.fourier_tempogram
    raw_feat = f(x, sr)
    for row in raw_feat:
        raw_feats.append(row)
    '''  
    
    transposed = list(map(list, zip(*raw_feats)))
    audio_feats = pd.DataFrame(transposed)
    
    feats1d = audio_feats.values.flatten()
    
    return np.concatenate((np.array([sb, wordrate, charrate]), feats1d))


########################

def extract(videodir, audiodir, cleandatadir, outdir):
    
    data = pd.read_csv(cleandatadir, index_col=0)
    
    for v in os.listdir(videopath):
        path = os.path.join(videopath, v)
        video = VideoFileClip(path)
        audio = video.audio
        audioname = v[:-4] + '.mp3'
        audiofn = os.path.join(audiodir, audioname)
        audio.write_audiofile(audiofn)
    
    texts = list()
    for a in os.listdir(audiodir):
        file = os.path.join(audiodir, a)
        texts.append(transcribe(file))
    data['Text'] = texts
    
    words_per_sec = list()
    chars_per_sec = list()
    for i in range(len(data)):
        row = data.iloc[i]
        wps, cps = get_text_rates(row['Duration (s)'], row['Text'])
        words_per_sec.append(wps)
        chars_per_sec.append(cps)
    data['WordsPerSec'] = words_per_sec
    data['CharsPerSec'] = chars_per_sec
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    data['WordsPerSec'] = imp.fit_transform(data['WordsPerSec'].values.reshape(-1, 1))
    data['CharsPerSec'] = imp.fit_transform(data['CharsPerSec'].values.reshape(-1, 1))
    
    df = data[['WordsPerSec', 'CharsPerSec']]
    features = list()
    sb = 1.0
    for i in range(len(df)):
        a = os.listdir(audiodir)[i]
        audio = os.path.join(audiodir, a)
        wr = df['WordsPerSec'][i]
        cr = df['CharsPerSec'][i]
        feat_array = feature_extract(audio, wr, cr, sb)
        features.append(feat_array)
        
    out = pd.DataFrame(features)
    out.to_csv(outdir)
    
    
    
