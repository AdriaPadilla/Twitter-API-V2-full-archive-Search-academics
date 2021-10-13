import pandas as pd
import glob
import collections

files = glob.glob("dataset-*.csv") # DEFINE HERE YOUR DATASET NAME

for file in files:

    file_hashtag_list = []
    file_mention_list = []
    file_anotations_list = []

    filename = file
    print(filename)
    df = pd.read_csv(file)
    lenth = len(df.index)

    for index, row in df.iterrows():
        print(f"working on row {index} of {lenth}")
        date = pd.to_datetime(row["tweet_created_at"], format="%Y-%m-%d %H:%M:%S")
        year = date.year

        try:
            hashtags = row["ent_hashtags"].split(";")
            for hashtag in hashtags:
                h_pair = (hashtag, year)
                file_hashtag_list.append(h_pair)
        except AttributeError:
            pass
        try:
            mentions = row["ent_mentions"].split(";")
            for mention in mentions:
                if mention == "false":
                    pass
                else:
                    m_pair = (mention, year)
                    file_mention_list.append(m_pair)
        except AttributeError:
            pass

        try:
            anotation_elements = row["ent_anotation_elements"].split(";")
            anotation_types = row["ent_anotation_types"].split(";")
        except AttributeError:
            pass

        for anotation, type in zip(anotation_elements, anotation_types):
            if anotation == "false":
                pass
            else:
                pair = (anotation, type, year)
                file_anotations_list.append(pair)

    hashtag_df = pd.DataFrame(file_hashtag_list, columns=["hashtag", "year"])
    hashtag_resume = hashtag_df.groupby(["hashtag","year"]).size().reset_index(name="count")
    hashtag_resume.to_excel(f"{filename}-hashtags.xlsx")

    mention_df = pd.DataFrame(file_mention_list, columns=["mention", "year"])
    mention_resume = mention_df.groupby(["mention","year"]).size().reset_index(name="count")
    mention_resume.to_excel(f"{filename}-mentions.xlsx")

    anotation_df = pd.DataFrame(file_anotations_list, columns=["anotation", "type", "year"])
    anotation_resume = anotation_df.groupby(["anotation","type", "year"]).size().reset_index(name="count")
    anotation_resume.to_excel(f"{filename}anotation.xlsx")
