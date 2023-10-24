from metric import merge_2dict, confusion_matrix, Accuracy, Correct_Rate
import pandas as pd
import json

# labels_no_tone = ["tS", "h", "x", "m", "7", "n",  "o", "f", "kp", "a_X", "e", "r", "i", "t_h", "w", "l", "O", "v", "p", "M", "u",  "M7", "z", "S", "uo", "7_X", "t", "ts_", "d", "a", "E_X", "b", "s", "j", "E", "k", "N", "J", "O_X", "G", "wp", "ie", "Nm", "dZ", "_1", "_2","_3", "_4", "_5a", "_5b", "_6a", "_6b"]

# labels_no_tone = ["tS",  "h", "x", "m", "7", "n",  "o", "f", "kp", "a_X", "e", "r", "i", "t_h", "w", "l", "O", "v", "p", "M", "u", "M7", "z", "S", "uo", "7_X", "t", "ts_", "d", "a", "E_X", "b", "s", "j", "E", "k", "N", "J", "O_X", "G", "wp", "ie", "Nm", "dZ"]

# labels_no_tone = ["_1", "_2", "_3", "_4", "_5a", "_5b", "_6a", "_6b"]

# tone = []
# labels_no_tone = ['a', 'E', 'e', 'i', 'O', 'o', '7', 'u', 'M', 'a_X', '7_X', 'E_X', 'O_X', 'ie', 'uo', 'M7', '_1', '_2', '_3', '_4', '_5a', '_5b', '_6a', '_6b']

file_name = "test_fix"
json_file_path = f"results/distinct_phoneme_error_{file_name}.json"
with open(json_file_path, 'r') as json_file:
        labels_no_tone = json.load(json_file)

# # b = ["_1", "_2", "_3", "_4", "_5a", "_5b", "_6a", "_6b"]

# # keys = {}
# # for i in range(len(a)):
# #     for j in range(len(b)):
# #         key = a[i], b[j]
# #         keys[key] = 0
# #     # keys.append(key)
    

# # print(keys)

APL = pd.read_csv("data/test_fix.csv")
# APL = pd.read_csv("MHA_KALDI_FIX_LM.csv")
res = {}

for i in range(len(APL)):
    res = merge_2dict(res, confusion_matrix(APL['Canonical'][i], APL['Transcript'][i]), )



res = (dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
# print(res)
import matplotlib.pyplot as plt
import numpy as np

# Example labels and predictions

# Calculate the confusion matrix
confusion_matrix = np.zeros((len(labels_no_tone), len(labels_no_tone)))  # Replace 3 with the number of classes in your case

for label in labels_no_tone:
    for prediction in labels_no_tone:
# for label, prediction in zip(labels, labels):
        k = str(label), str(prediction)
        # print(res[k])
        if (label == prediction):
            confusion_matrix[labels_no_tone.index(label), labels_no_tone.index(prediction)] = 70
        else:
            try:   
                print(res[k])
                confusion_matrix[labels_no_tone.index(label), labels_no_tone.index(prediction)] = res[k]
            except:
                confusion_matrix[labels_no_tone.index(label), labels_no_tone.index(prediction)] = 0

# Define class labels
class_labels = labels_no_tone


# Plot the confusion matrix
plt.figure(figsize=(10, 8))
plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar(label='Counts')

tick_marks = np.arange(len(class_labels))
plt.xticks(tick_marks, class_labels, rotation=45)
plt.yticks(tick_marks, class_labels)


plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.show()
# print(res[0])
# print(res['_1', '_2'])
# print(res['_5a', '_1'])
# print(res['_1', '_5a'])
# print(res['_2', '_1'])
# print(res['_5a', '_2'])
# print(res['_1', '<eps>'])
# print(res['_1', '_6a'])
# print(res['_3', '_2'])
# print(res['j', '<eps>'])
# print(res['n', '<eps>'])


#worst APL -> PAPL
# ('_1', '_2'): 113, ('_5a', '_1'): 111, ('_1', '_5a'): 110, ('_2', '_1'): 97, ('_5a', '_2'): 74, ('_1', '<eps>'): 73, ('_1', '_6a'): 60, ('_3', '_2'): 58, ('j', '<eps>'): 53, ('n', '<eps>'): 51
                # 16                47                  34                  30                28                   56                 12                14                  49                  43

# confuse phoneme (not tone) 
# ('j', '<eps>'): 53, ('n', '<eps>'): 51, ('S', 's'): 50, ('k', '<eps>'): 36, ('a', '<eps>'): 35, ('m', '<eps>'): 35, ('w', '<eps>'): 34, ('wp', '<eps>'): 33, ('t', '<eps>'): 31, ('a_X', 'a'): 26, ('7', '<eps>'): 24, ('h', '<eps>'): 22



#worst PAPL
#{('_1', '<eps>'): 56, ('j', '<eps>'): 49, ('_5a', '_1'): 47, ('n', '<eps>'): 43, ('_2', '<eps>'): 38, ('_2', '_5a'): 37, ('_1', '_5a'): 34, ('_5a', '<eps>'): 32, ('wp', '<eps>'): 30, ('_2', '_1'): 30

# confuse phoneme (not tone) 
# #('j', '<eps>'): 49, ('n', '<eps>'): 43, ('wp', '<eps>'): 30, ('<eps>', '_1'): 29, ('m', '<eps>'): 28, ('a_X', 'a'): 27, ('k', '<eps>'): 27, ('a', '<eps>'): 26, ('t', '<eps>'): 25, ('S', 's'): 25, ('t', 'k'): 22, ('w', '<eps>'): 22, ('tS', 'ts_'): 22, ('r', 'z'): 21


