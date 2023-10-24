import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file into a DataFrame
df = pd.read_csv('data/all_area-1.csv')

# Create sets to store distinct phonemes
canonical_phonemes_set = set()
transcript_phonemes_set = set()

# Loop through the DataFrame to extract and add phonemes to the sets
for index, row in df.iterrows():
    canonical_phonemes = set(row['Canonical'].split())
    transcript_phonemes = set(row['Transcript'].split())
    
    canonical_phonemes_set.update(canonical_phonemes)
    transcript_phonemes_set.update(transcript_phonemes)

# Create dictionaries to count phoneme occurrences
canonical_phoneme_counts = {}
transcript_phoneme_counts = {}
    
for phoneme in canonical_phonemes_set:
    canonical_phoneme_counts[phoneme] = 0

for phoneme in transcript_phonemes_set:
    transcript_phoneme_counts[phoneme] = 0

# Loop through the DataFrame to count phoneme occurrences
for index, row in df.iterrows():
    canonical_phonemes = row['Canonical'].split()
    transcript_phonemes = row['Transcript'].split()
    
    for phoneme in canonical_phonemes:
        canonical_phoneme_counts[phoneme] += 1

    for phoneme in transcript_phonemes:
        transcript_phoneme_counts[phoneme] += 1

# Create bar plots
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(canonical_phoneme_counts.keys(), canonical_phoneme_counts.values())
plt.title('Canonical Phoneme Counts')
plt.xlabel('Phoneme')
plt.ylabel('Count')
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
plt.bar(transcript_phoneme_counts.keys(), transcript_phoneme_counts.values())
plt.title('Transcript Phoneme Counts')
plt.xlabel('Phoneme')
plt.ylabel('Count')
plt.xticks(rotation=90)

plt.tight_layout()

# Show the plots
plt.show()
