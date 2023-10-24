from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
# from datasets import load_dataset
import torch
import librosa
import pandas as pd
# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60")


newmodel = torch.nn.Sequential(*(list(model.children())[:-2]))
newmodel.eval().to('cuda')
# print(newmodel)
def en_phonetic_extract(path):
# print(newmodel)
    with torch.no_grad():
        path = path
        wav, sr = librosa.load(path)
        y_16k = librosa.resample(wav, sr, 16000)
        audio_input = librosa.to_mono(y_16k)
        input_values = processor(audio_input, return_tensors="pt",sampling_rate = 16000, padding="longest").input_values
        input_values = input_values.to('cuda')     
        outputs = newmodel(input_values)
    return outputs.last_hidden_state

# print(en_phonetic_extract("/home/tuht/EN_MDD/WAV/TEST/DR1/FAKS0/sa1.wav"))
