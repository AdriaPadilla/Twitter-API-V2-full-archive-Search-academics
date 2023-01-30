import pandas as pd
import glob
from itertools import combinations
from tqdm import tqdm
import time
from datetime import datetime

files_to_process = glob.glob("a-*/*.csv") # DEFINE THE NAME OF THE DATASET THAT WILL BE PROCESSED

def graph(frame, file_name):
    print(f"loading file {file_name}")
    df = pd.read_csv(frame, sep="\t", quotechar='"', lineterminator="\n")
    print(df)
    user_hashtag_list = []
    cohashtag_list = []
    coanotation_list = []
    coanotation_nodes_list = []
    user_mentions_list = []

    index = df.index
    rows_to_process = len(index)

    for index, row in tqdm(df.iterrows(), total=rows_to_process, desc="Processing..."):
        tweet_time = row["tweet_created_at"]

       # print(f"working on row {index} from {rows_to_process}")

        # Hashtags / Users network

        username = row["username"]
        target = row["ent_hashtags"]
        diferent_targets = target.split(";")

        for hashtag in diferent_targets:
            if hashtag == "false":
                pass
            else:
                node_source = username
                node_target = "#" + hashtag

                user_hash_network_df = pd.DataFrame({
                    "source": node_source,
                    "target": node_target,
                    "Timeset": tweet_time
                }, index=[0])
                user_hashtag_list.append(user_hash_network_df)

        # Co-hashtag graph

        n = len(diferent_targets)
        if n > 1:
            comb_list = combinations(diferent_targets, 2)
            for element in list(comb_list):
                hashtag_source = element[0]
                hashtag_target = element[1]

                cohash_network_df = pd.DataFrame({
                    "source": hashtag_source,
                    "target": hashtag_target,
                    "Timeset": tweet_time,
                }, index=[0])
                cohashtag_list.append(cohash_network_df)

        else:
            pass

        # COANOTATIONS graph
        anotation_type = row["ent_anotation_types"]
        if anotation_type == False:
            pass
        else:
            anotation_type = row["ent_anotation_types"].split(";")

            n = len(anotation_type)
            if n > 1:
                anotation_name = row["ent_anotation_elements"].split(";")

                # COANPTATIONS NODES TABLE
                for type, name in zip(anotation_type, anotation_name):
                    nodes_frame = pd.DataFrame({
                        "Id": name,
                        "Label": name,
                        "category": type,
                    }, index=[0])
                    coanotation_nodes_list.append(nodes_frame)

                # COANOTATION EDGES
                types_combinations = combinations(anotation_type, 2)
                name_combinations = combinations(anotation_name, 2)

                for type, name in zip(types_combinations, name_combinations):
                    co_anotation_df = pd.DataFrame({
                        "source": name[0],
                        "target": name[1],
                        "source_type": type[0],
                        "target_type": type[1],
                        "Timeset": tweet_time
                    }, index=[0])
                    coanotation_list.append(co_anotation_df)
            else:
                pass

        # USERS / ANOTATION GRAPH

            # TO-DO

        # MENTION GRAPH

        mentions = row["ent_mentions"]
        different_mentions = mentions.split(";")

        for mention in different_mentions:
            if mention == "false":
                pass
            else:
                mentions_frame = pd.DataFrame({
                    "source": username,
                    "target": mention,
                    "Timeset": tweet_time,
                }, index=[0])
                user_mentions_list.append(mentions_frame)

    #### BUILD FINAL DATASETS

    print("Exporting Network Files")

    # USER-HASHTAG GRAPH
    try:
        user_hash_graph = pd.concat(user_hashtag_list)
        user_hash_graph.to_csv(f"{file_name}-user_hashtag_graph.csv", index=False)
    except ValueError:
        pass
    # COHASHTAGS GRAPH
    try:
        cohashtags_network = pd.concat(cohashtag_list)
        cohashtags_network.to_csv(f"{file_name}-cohashtag_graph_adjacency_list.csv", index=False)
    except ValueError:
        pass
    # COANOTATION GRAPH
    try:
        coanotation_network = pd.concat(coanotation_list)
        coanotation_network.to_csv(f"{file_name}-coanotation_edges_list.csv", index=False)
    except ValueError:
        pass
    # COANOTATION NODES TABLE
    try:
        coanotation_nodes = pd.concat(coanotation_nodes_list)
        coanotation_nodes.drop_duplicates()
        coanotation_nodes.to_csv(f"{file_name}-coanotation_nodes_list.csv", index=False)
    except ValueError:
        pass
    # MENTIONS LIST GRAPH
    try:
        mention_graph = pd.concat(user_mentions_list)
        mention_graph.to_csv(f"{file_name}-mention-graph.csv", index=False)
    except ValueError:
        pass

# EXECUTION
for file in files_to_process:
    file_name = file.split(".")[0]
    graph(file, file_name)
