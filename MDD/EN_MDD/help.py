from tkinter import N
import librosa
# import pandas as pd
import numpy as np
import pandas as pd
import torchaudio
import torchaudio.functional as F
import numpy as np
from python_speech_features import fbank
# from python_speech_features import logfbank
import scipy.io.wavfile as wav

def get_pitch_kaldi(path):
    SPEECH_WAVEFORM, SAMPLE_RATE = torchaudio.load(path)
    t = librosa.get_duration(filename = path)
    pitch_feature = F.compute_kaldi_pitch(SPEECH_WAVEFORM, 16000, frame_length = 0, frame_shift = 20)
    pitch, nfcc = pitch_feature[..., 0], pitch_feature[..., 1]
    data = pitch.cpu().detach().numpy()
    # print(data.shape)
    # print((t/0.02-(t/0.02)//1))
    if (t/0.02-(t/0.02)//1 <=0.246) or (t/0.02-(t/0.02)//1 >0.99):
        data = np.delete(data,obj = [len(data[0])-1,len(data[0])-2],axis = 1)
    else:
        data = np.delete(data,obj = len(data[0])-1, axis = 1) 
    return data


def get_pitch_NCCF(path):
    SPEECH_WAVEFORM, SAMPLE_RATE = torchaudio.load(path)
    t = librosa.get_duration(filename = path)
    pitch = F.detect_pitch_frequency(SPEECH_WAVEFORM, 16000, frame_time=0.02, win_length=3)
    # pitch, nfcc = pitch_feature[..., 0], pitch_feature[..., 1]
    data = pitch.cpu().detach().numpy()
    # print(data.shape)
    # print((t/0.02-(t/0.02)//1))
    if (0.000001<t/0.02-(t/0.02)//1 <=0.246) or (t/0.02-(t/0.02)//1 >0.99999999999999999):
        data = np.delete(data,obj = [len(data[0])-1],axis = 1)
    # else:
    #     data = np.delete(data,obj = len(data[0])-1, axis = 1) 
    return data


def get_filterbank(path):
    (rate,sig) = wav.read(path)
    filter, energy = fbank(sig,rate, winlen=0.02, winstep = 0.02, nfilt=80)
    filter = filter.reshape(80, -1)
    energy = energy.reshape(1,-1)
    data = np.concatenate((filter,energy))
    t = librosa.get_duration(filename = path)
    # print((t/0.02-(t/0.02)//1))
    if 0.000001<t/0.02-(t/0.02)//1 <=0.246:
        data = np.delete(data,obj = [len(data[0])-1,len(data[0])-2,len(data[0])-3],axis = 1)
    else:
        data = np.delete(data,obj = [len(data[0])-1,len(data[0])-2],axis = 1)
    return data

