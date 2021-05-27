import pandas as pd
from itertools import permutations

def graph(df):
    user_hashtag_list = []
    cohashtag_list = []
    coanotation_list = []
    coanotation_nodes_list = []

    print("creating networks")
    for index, row in df.iterrows():

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
                }, index=[0])
                user_hashtag_list.append(user_hash_network_df)

        # Co-hashtag graph

        n = len(diferent_targets)
        if n > 1:
            perm = permutations(diferent_targets, 2)
            for element in list(perm):
                hashtag_source = element[0]
                hashtag_target = element[1]

                cohash_network_df = pd.DataFrame({
                    "source": hashtag_source,
                    "target": hashtag_target,
                }, index=[0])
                cohashtag_list.append(cohash_network_df)

        else:
            pass

        # CCOANOTATIONS graph
        anotation_type = row["ent_anotation_types"].split(";")
        anotation_name = row["ent_anotation_elements"].split(";")

        n = len(anotation_type)
        if n > 1:

            # COANPTATIONS NODES TABLE
            for type, name in zip(anotation_type, anotation_name):
                nodes_frame = pd.DataFrame({
                    "Id": name,
                    "Label": name,
                    "category": type,
                }, index=[0])
                coanotation_nodes_list.append(nodes_frame)

            # COANOTATION EDGES
            types_perm = permutations(anotation_type, 2)
            name_perm = permutations(anotation_name, 2)

            for type, name in zip(types_perm, name_perm):
                co_anotation_df = pd.DataFrame({
                    "source": name[0],
                    "target": name[1],
                    "source_type": type[0],
                    "target_type": type[1],
                }, index=[0])
                coanotation_list.append(co_anotation_df)

    #### BUILD FINAL DATASETS

    print("Exporting Network Files")

    # USER-HASHTAG GRAPH
    user_hash_graph = pd.concat(user_hashtag_list)
    user_hash_graph.to_csv("user_hashtag_graph.csv", index=False, header=False)

    # COHASHTAGS GRAPH
    cohashtags_network = pd.concat(cohashtag_list)
    cohashtags_network.to_csv("cohashtag_graph_adjacency_list.csv", index=False, header=False)

    # COANOTATION GRAPH
    coanotation_network = pd.concat(coanotation_list)
    coanotation_network.to_csv("coanotation_edges_list.csv", index=False)

    # COANOTATION NODES TABLE
    coanotation_nodes = pd.concat(coanotation_nodes_list)
    coanotation_nodes.drop_duplicates()
    coanotation_nodes.to_csv("coanotation_nodes_list.csv", index=False)