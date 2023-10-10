from jiwer import compute_measures
import csv
import json

def check_phoneme(file_path, file_path_store, path_analysis, num_lines_to_read):
    # read file csv
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)

        # skip 3600 rows
        for i in range(3600):
            next(csv_reader)

        line_count = 0
        my_dict = dict()

        for row in csv_reader:
            if line_count < num_lines_to_read:
                line_count += 1

                path = row[1]
                if path.startswith(path_analysis):
                    # jiwer to compute phoneme error
                    reference = row[2]
                    hypothesis = row[3]
                    result = compute_measures(reference, hypothesis)

                    # Check phoneme

                    for op in result['ops']:
                        if op['type' == 'insert']:
                            # Pair '<eps>' with inserted word
                            temp = result['ops'][0]['type' == 'insert']
                            start = temp.hyp_start_idx
                            end = temp.hyp_end_idx
                            hyp_word = result['hypothesis'][0][start:end]
                            for i in range(len(hyp_word)):
                                if ('<eps>', hyp_word[i]) in my_dict:
                                    my_dict[('<eps>', hyp_word[i])] += 1
                                else:
                                    my_dict[('<eps>', hyp_word[i])] = 1      
                        elif op['type' == 'delete']:
                            # Pair deleted word with '<eps>'
                            temp = result['ops'][0]['type' == 'delete']
                            start = temp.ref_start_idx
                            end = temp.ref_end_idx
                            ref_word = result['truth'][0][start:end]
                            for i in range(len(ref_word)):
                                if (ref_word[i], '<eps>') in my_dict:
                                    my_dict[(ref_word[i], '<eps>')] += 1
                                else:
                                    my_dict[(ref_word[i], '<eps>')] = 1
                        elif op['type' == 'substitute']:
                            # Pair original word with substitution word
                            temp = result['ops'][0]['type' == 'substitute']
                            start_ref = temp.ref_start_idx
                            end_ref = temp.ref_end_idx
                            start_hyp = temp.hyp_start_idx
                            end_hyp = temp.hyp_end_idx
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


def get_top_10_error(file_path_store):
    with open(file_path_store, "r") as json_file:
        data = json.load(json_file)

    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)
    top_10_items = sorted_dict[:10]
    return dict(top_10_items)


# check error TIMIT and store
num_lines = 9900 - 3600
path = "data/all_area-1.csv"
train_path = "train"
region = "dr1"
path_analysis = train_path + "/" + region
path_store = f"results/phoneme_error_timit_{train_path}_{region}.json"
check_phoneme(file_path=path, file_path_store=path_store, path_analysis=path_analysis, num_lines_to_read=num_lines,)

# get top error TIMIT
top_10 = get_top_10_error(file_path_store=path_store)
print(top_10)

