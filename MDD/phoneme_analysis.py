from jiwer import compute_measures
import csv
import json

def check_phoneme(file_path, num_lines_to_read, fileName, filter, filterName):
    # read file csv
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # file_path_store = f"results/en/phoneme_error_{fileName}_full.json"
        file_path_store = f"results/vi_top/phoneme_error_{fileName}_full{filterName}.json"

        # skip first row
        next(csv_reader)

        line_count = 0
        my_dict = dict()

        for row in csv_reader:
            if line_count < num_lines_to_read:
                line_count += 1
                
                # jiwer to compute phoneme error
                can = row[2]
                trans = row[3]
                can_split = can.split()
                trans_split = trans.split()

                # filter nucleus or tone
                # canonical = [word for word in can_split if any(t in word for t in filter)]
                # transcript = [word for word in trans_split if any(t in word for t in filter)]

                # filter  
                # canonical = [word for word in can_split if word in filter]
                # transcript = [word for word in trans_split if word in filter]

                # filter without nucleus and tone
                # canonical = [word for word in can_split if not word in filter]
                # transcript = [word for word in trans_split if not word in filter]

                # reference = ' '.join(canonical)
                # hypothesis = ' '.join(transcript)
               
                # if len(reference) == 0 or len(hypothesis) == 0:
                #     continue
                
                # no filter
                reference = row[2]
                hypothesis = row[3]

                result = compute_measures(reference, hypothesis)

                # Check phoneme
                delete_chunks = []
                insert_chunks = []
                substitute_chunks = []

                for chunk in result['ops'][0]:
                    if chunk.type == 'delete':
                        delete_chunks.append(chunk)
                    elif chunk.type == 'insert':
                        insert_chunks.append(chunk)
                    elif chunk.type == 'substitute':
                        substitute_chunks.append(chunk)

                for chunk in delete_chunks:
                    start = chunk.ref_start_idx
                    end = chunk.ref_end_idx
                    ref_word = result['truth'][0][start:end]
                    for i in range(len(ref_word)):
                        if (ref_word[i], '<eps>') in my_dict:
                            my_dict[(ref_word[i], '<eps>')] += 1
                        else:
                            my_dict[(ref_word[i], '<eps>')] = 1

                for chunk in insert_chunks:
                    start = chunk.hyp_start_idx
                    end = chunk.hyp_end_idx
                    hyp_word = result['hypothesis'][0][start:end]
                    for i in range(len(hyp_word)):
                        if ('<eps>', hyp_word[i]) in my_dict:
                            my_dict[('<eps>', hyp_word[i])] += 1
                        else:
                            my_dict[('<eps>', hyp_word[i])] = 1

                for chunk in substitute_chunks:
                    start_ref = chunk.ref_start_idx
                    end_ref = chunk.ref_end_idx
                    start_hyp = chunk.hyp_start_idx
                    end_hyp = chunk.hyp_end_idx
                    ref_word = result['truth'][0][start_ref:end_ref]
                    hyp_word = result['hypothesis'][0][start_hyp:end_hyp]
                    for i in range(min(len(ref_word), len(hyp_word))):
                        if (ref_word[i], hyp_word[i]) in my_dict:
                            my_dict[(ref_word[i], hyp_word[i])] += 1
                        else:
                            my_dict[(ref_word[i], hyp_word[i])] = 1
            else:
                break

        # store phoneme error
        string_dict = {str(key): value for key, value in my_dict.items()}
        with open(file_path_store, "w") as json_file:
            json.dump(string_dict, json_file)
        sort_top_10_error(file_path_store=file_path_store)

    
def len_file(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Use a list comprehension to iterate through the rows and count them
        row_count = sum(1 for row in csv_reader)
        return row_count

def sort_top_10_error(file_path_store):
    with open(file_path_store, "r") as json_file:
        data = json.load(json_file)

    # Sort the JSON data based on values (assuming values are numeric)
    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
    # If you only want the top 10 items, you can slice the sorted list:
    top_10_items = sorted_dict[:30]

    # If you want to convert the keys back to strings:
    string_dict = {str(key): value for key, value in top_10_items}

    # Write the sorted data back to the JSON file
    with open(file_path_store, "w") as json_file:
        json.dump(string_dict, json_file)

# Nucleus and Tone
nucleus = ['a', 'E', 'e', 'i', 'O', 'o', '7', 'u', 'M', 'a_X', '7_X', 'E_X', 'O_X', 'ie', 'uo', 'M7']
tone = ['_1', '_2', '_3', '_4', '_5a', '_5b', '_6a', '_6b']


fileName = ["dev", "L2_arctic_train", "test", "Timit", "train_EN", "all"]
# filterName = "nucleus"
# filterName = "tone"
# filterName = "nucleus_tone"
filterName = ""

# for name in fileName:
#     path = f"EN_MDD/{name}.csv"
#     path_store = f"results/en/phoneme_error_{name}_full.json"
#     num_lines = len_file(csv_file_path=path) - 1
#     # check_phoneme(file_path=path, num_lines_to_read=num_lines, fileName=name)
#     check_phoneme(file_path=path, num_lines_to_read=num_lines, fileName=name, filter=[], filterName=filterName)
#     sort_top_10_error(file_path_store=path_store)

name = "mamnon"
path = f"data/{name}.csv"
path_store = f"results/vi_top/phoneme_error_{name}_full.json"
num_lines = len_file(csv_file_path=path) - 1
check_phoneme(file_path=path, num_lines_to_read=num_lines, fileName=name, filter=[], filterName=filterName)
