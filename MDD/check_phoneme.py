import difflib
import csv
import json


# read file csv with skip row
# def read_csv(file_path, skip, ):
#     # Open the CSV file for reading
#     with open(file_path, mode='r', newline='') as file:
#         csv_reader = csv.reader(file)

#         # Skip the first 10 lines (rows)
#         for _ in range(10):
#             next(csv_reader)

#         # Read and process the next 10 lines
#         for _ in range(10):
#             row = next(csv_reader, None)
#             if row is not None:
#                 # Process each row (e.g., print the row)
#                 print(row[2])


def check_phoneme(file_path, file_path_store, num_lines_to_read):
    # read file csv
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)

        # skip first row
        next(csv_reader)

        line_count = 0
        my_dict = dict()

        for row in csv_reader:
            if line_count < num_lines_to_read:
                line_count += 1

                # convert str to word
                words1 = row[2].split()
                words2 = row[3].split()

                # use SequenceMatcher
                matcher = difflib.SequenceMatcher(None, words1, words2)
                opcodes = matcher.get_opcodes()

                # Check phoneme
                for tag, i1, i2, j1, j2 in opcodes:
                    old = ' '.join(words1[i1:i2])
                    new = ' '.join(words2[j1:j2])

                    if tag == 'equal':
                        continue
                    if tag == 'delete':
                        new = '<eps>'
                    if tag == 'insert':
                        old = '<eps>'

                    if (old, new) in my_dict:
                        my_dict[(old, new)] += 1
                    else:
                        my_dict[(old, new)] = 1
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


# check error L2 and store
num_lines = 3600 - 1
path = "data/all_area-1.csv"
path_store = "results/phoneme_error_L2.json"
check_phoneme(file_path=path, file_path_store=path_store, num_lines_to_read=num_lines)

# get top error L2
top_10 = get_top_10_error(file_path_store=path_store)
print(top_10)

