from jiwer import  compute_measures

reference =  "ih t s ih l iy g    l t uw p ow s t d ey t  ah ch eh k"
hypothesis = "ih t s ih l iy g ih l t ah p ow s   d ey dh ih ch eh k"

result = compute_measures(reference, hypothesis)

print(result)

my_dict = dict()


delete_chunks = []
insert_chunks = []
substitute_chunks = []

for chunk in result['ops']:
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

for op in result['ops']:
    if op.type == 'insert':
        # Pair '<eps>' with inserted word
        temp = result['ops'][0]['type'=='insert']
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

print(my_dict)
