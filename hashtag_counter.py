# COUNT HASHTAG FREQUENCY ON YOUR DATASETS

import pandas as pd
import glob
from collections import Counter

files = glob.glob("your-dataset-name.csv")      # DEFINE HERE YOUR DATASET NAME

for file in files:

    hashtag_list =[]
    df = pd.read_csv(file)
    for index, row in df.iterrows():             # For every tweet in dataset
        hashtags = row["ent_hashtags"]           # The column where hashtags are
        if hashtags == "false":                  # some tweets dosen't have hashtags :)
            pass
        else:
            list = hashtags.split(";")           # if there're mor than one hashtag, must pass to list
            for element in list:
                hashtag_list.append(element)     # append each hashtag to list

    c = Counter(hashtag_list)                    # NOW count the frequency
    frame = pd.DataFrame.from_dict([c])
    frame_2 = frame.transpose()                  # Doing some magic stuff
    frame_2.index.name = 'hashtag'
    su = frame_2.rename(columns={frame_2.columns[0]: 'count'}) # More magic things...
    su.to_csv(f"{file}-count.csv")               # Your output file
