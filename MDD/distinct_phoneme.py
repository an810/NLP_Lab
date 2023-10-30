import json


def distinct_phoneme(file_path_store, output_file_path):
    with open(file_path_store, "r") as json_file:
            data = json.load(json_file)

    # Extract the unique phonemes
    unique_phonemes = set()

    for key in data.keys():
        original_phoneme, incorrect_phoneme = eval(key)
        unique_phonemes.add(original_phoneme)
        unique_phonemes.add(incorrect_phoneme)

    # Convert the set of unique phonemes to a sorted list if needed
    sorted_unique_phonemes = sorted(unique_phonemes)

    # Print or use the list of unique phonemes
    # print(sorted_unique_phonemes)

    with open(output_file_path, 'w') as json_file:
        json.dump(sorted_unique_phonemes, json_file, indent=4)


fileName = ["dev", "L2_arctic_train", "test", "Timit", "train_EN", "all"]
# filter = "tone"
# filter = "nucleus"
# filter = "nucleus_tone"
filter = ""

for file_name in fileName:
    # file_path_store = f"results/phoneme_error_{file_name}_full_{filter}.json"
    # output_file_path = f"confusion_matrix_data/phoneme_error_{file_name}_{filter}.json"
    file_path_store = f"results/en/phoneme_error_{file_name}_full{filter}.json"
    output_file_path = f"confusion_matrix_data/en/phoneme_error_{file_name}{filter}.json"
    distinct_phoneme(file_path_store=file_path_store, output_file_path=output_file_path)

# file_name = "all"
# file_path_store = f"results/en/phoneme_error_{file_name}_full{filter}.json"
# output_file_path = f"confusion_matrix_data/en/phoneme_error_{file_name}{filter}.json"
# distinct_phoneme(file_path_store=file_path_store, output_file_path=output_file_path)