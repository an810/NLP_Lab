from metric import merge_2dict, confusion_matrix, Accuracy, Correct_Rate
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import metric

def plot_cm(file_name, filter):
    json_file_path = f"confusion_matrix_data/en/phoneme_error_{file_name}{filter}.json"
    with open(json_file_path, 'r') as json_file:
            labels = json.load(json_file)

    APL = pd.read_csv(f"EN_MDD/{file_name}.csv")

    res = {}

    for i in range(len(APL)):
        res = merge_2dict(res, metric.confusion_matrix(APL['Canonical'][i], APL['Transcript'][i]), )

    res = (dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))

    # Example labels and predictions

    # Calculate the confusion matrix
    metric.confusion_matrix = np.zeros((len(labels), len(labels)))  # Replace 3 with the number of classes in your case

    for label in labels:
        for prediction in labels:
    # for label, prediction in zip(labels, labels):
            k = str(label), str(prediction)
            # print(res[k])
            if (label == prediction):
                metric.confusion_matrix[labels.index(label), labels.index(prediction)] = 8000
            else:
                try:   
                    print(res[k])
                    metric.confusion_matrix[labels.index(label), labels.index(prediction)] = res[k]
                except:
                    metric.confusion_matrix[labels.index(label), labels.index(prediction)] = 0
    
    # metric.confusion_matrix[labels.index('z'), labels.index('s')] = 5000
    # metric.confusion_matrix[labels.index('dh'), labels.index('d')] = 5000
    # metric.confusion_matrix[labels.index('ih'), labels.index('iy')] = 4000

    # metric.confusion_matrix[labels.index('S'), labels.index('s')] = 50
    # metric.confusion_matrix[labels.index('r'), labels.index('z')] = 50
    # metric.confusion_matrix[labels.index('n'), labels.index('l')] = 50

    # Define class labels
    class_labels = labels


    # Plot the confusion matrix
    plt.figure(figsize=(10, 8))
    plt.imshow(metric.confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f'Confusion Matrix {file_name} {filter}')
    plt.colorbar(label='Counts')

    tick_marks = np.arange(len(class_labels))
    plt.xticks(tick_marks, class_labels, rotation=45)
    plt.yticks(tick_marks, class_labels)


    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.show()


# file_name = "test_fix"
# file_name = "dev"
# file_name = "test"
# file_name = "train"
# file_name = "merge"

# filter = "tone"
# filter = "nucleus"
# filter = "nucleus_tone"
filter = ""

# fileName = "dev"
# fileName = "L2_arctic_train"
# fileName = "test"
# fileName = "Timit"
# fileName = "train_EN"
fileName = "all"

plot_cm(file_name=fileName, filter=filter)