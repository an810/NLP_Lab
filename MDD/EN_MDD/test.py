# from phonetic_extract import en_phonetic_extract
# import pandas as pd
import numpy as np
import librosa
from python_speech_features import fbank
import scipy
import scipy.io.wavfile as wav
# import os
# import glob
# from help import get_pitch_kaldi, get_pitch_NCCF, get_filterbank

#Extract phonetic 
"""
data = pd.read_csv("dev.csv")
for i in range(len(data)):
    print(i)
    print("WAV/" + data['Path'][i] + "phonetic.npy")
    phonetic = en_phonetic_extract("WAV/" + data['Path'][i] + ".wav").squeeze(0).detach().cpu().numpy()
    # print("WAV/" + data['Path'][i] + "phonetic.npy")
    np.save("WAV/" + data['Path'][i] + "phonetic.npy", phonetic)
    # print(phonetic.shape)
# print(data['Path'][0])

"""

#Extract pitch
"""
data = pd.read_csv("test.csv")
path = [
'L2_arctic_WAV/BWC_arctic_a0100']

for i in range(len(data)):
    # print(i)
    # print("WAV/" + data['Path'][i] + "NCCF.npy")
    # print("WAV/" + data['Path'][i] + "KALDI.npy")
    phonetic = np.load("WAV/" + data['Path'][i] + "phonetic.npy")
    KALDI = get_pitch_kaldi("WAV/" + data['Path'][i] + ".wav")
    NCCF = get_pitch_NCCF("WAV/" + data['Path'][i] + ".wav")
    if i%100==0:
        print(i)
    # phonetic = en_phonetic_extract("WAV/" + data['Path'][i] + ".wav").squeeze(0).detach().cpu().numpy()
    # # print("WAV/" + data['Path'][i] + "phonetic.npy")
    if phonetic.shape[0]!=KALDI.shape[1] or phonetic.shape[0]!=NCCF.shape[1]:
        print(data['Path'][i])
        print(phonetic.shape[0])
        print(KALDI.shape[1])
        print(NCCF.shape[1])
    else:
        np.save("WAV/" + data['Path'][i] + "NCCF.npy", NCCF)
        np.save("WAV/" + data['Path'][i] + "KALDI.npy", KALDI)

"""

#Extract acoustic
"""
data = pd.read_csv("dev.csv")
for i in range(len(data)):
    phonetic = np.load("WAV/" + data['Path'][i] + "phonetic.npy")
    FILTERBANK = get_filterbank("WAV/" + data['Path'][i] + ".wav")
    if i%100==0:
        print(i)
    if phonetic.shape[0]!=FILTERBANK.shape[1]:
        print(data['Path'][i])
    else:
        np.save("WAV/" + data['Path'][i] + "FILTERBANK.npy", FILTERBANK)

"""

#Create Vocab Dict
"""
data = pd.read_csv("train.csv")
Transcripts = []
Canonicals = []
for i in range(len(data)):
    Transcripts.extend(data['Transcript'][i].split(" "))
    Canonicals.extend(data['Canonical'][i].split(" "))

Transcripts = set(Transcripts)
Canonicals = set(Canonicals)
Transcript = ['ae', 'm', 'k', 'eh*', 'n', 'aw', 'ao*', 'iy', 'er*', 'z*', 'uw*', 'f', 'p', 'd*', 'ao', 'l*', 'uw', 'hh*', 't', 'ah*', 'y*', 'n*', 'th', 'hh', 'err', 'uh*', 'p*', 'zh', 'k*', 'eh', 'ow*', 'ay', 'w', 'ey', 'aw*', 'l', 'zh*', 'ih', 'v', 'oy', 'aa*', 't*', 'jh', 'b*', 'w*', 'ow', 'ng', 'b', 'ch', 'dh*', 'y', 'er', 'v*', 'ah', 'sh', 'aa', 'g', 'd', 'dh', 'r*', 'ae*', 'ey*', 'uh', 'r', 'g*', 's', 'z', 'jh*']
dic = list([])
for i in range(len(Transcript)):
    dic.append(Transcript[i])
    dic.append(i)

def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct
print(Convert(dic))
"""



"""
#Debug
path = [
'L2_arctic_WAV/HQTV_arctic_a0028',
'L2_arctic_WAV/HQTV_arctic_a0047',
'L2_arctic_WAV/NCC_arctic_a0131',
'L2_arctic_WAV/SVBI_arctic_a0059',
'L2_arctic_WAV/YKWK_arctic_a0027',
'L2_arctic_WAV/YKWK_arctic_a0134',
'L2_arctic_WAV/ZHAA_arctic_a0088',
]
for i in (path):
    phonetic = np.load("WAV/" + i + "phonetic.npy")
    FILTERBANK = get_filterbank("WAV/" + i + ".wav")
    # if i%100==0:
    #     print(i)
    if phonetic.shape[0]!=FILTERBANK.shape[1]:
        # print(data['Path'][i])
        print(phonetic.shape[0])
        print(FILTERBANK.shape[1])
"""
def get_filterbank(path):
    (rate,sig) = wav.read(path)
    filter, energy = fbank(sig,rate, winlen=20, winstep = 0.02, nfilt=80)
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

import glob
import os
import tqdm
data = glob.glob("./WAV/train/*/*/*")
print(len(data))