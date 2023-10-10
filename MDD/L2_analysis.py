from jiwer import compute_measures
import csv
import json

def check_phoneme(file_path, file_path_store, num_lines_to_read, area):
    # read file csv
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)

        #skip first row
        next(csv_reader)

        line_count = 0
        my_dict = dict()

        for row in csv_reader:
            if line_count < num_lines_to_read:
                line_count += 1

                _area = row[4]
                if area == _area:
                    # jiwer to compute phoneme error
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

def sort_top_10_error(file_path_store):
    with open(file_path_store, "r") as json_file:
        data = json.load(json_file)

    # Sort the JSON data based on values (assuming values are numeric)
    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
    # If you only want the top 10 items, you can slice the sorted list:
    top_10_items = sorted_dict[:10]

    # If you want to convert the keys back to strings:
    string_dict = {str(key): value for key, value in top_10_items}

    # Write the sorted data back to the JSON file
    with open(file_path_store, "w") as json_file:
        json.dump(string_dict, json_file)
    


# check error TIMIT and store
num_lines = 3600-1
area = '4'
path = "data/all_area-1.csv"
path_store = f"results/phoneme_error_l2_{area}.json"

# for area in range(6):
check_phoneme(file_path=path, file_path_store=path_store, num_lines_to_read=num_lines, area=area)
# get top error TIMIT
sort_top_10_error(file_path_store=path_store)
# print(top_10)

