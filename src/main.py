import json
import os
import random
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from ConfigSpace import (
    Categorical,
    Configuration,
    ConfigurationSpace,
    Float,
    Integer,
    EqualsCondition,
    InCondition,
)
from ConfigSpace.read_and_write import json as cs_json


from tqdm import tqdm

from utils.cluster import create_configs, generate_clusters
from utils.common import make_dir, json_to_csv
from utils.plot import plot_cluster_data


if __name__ == "__main__":
    output_path = make_dir(os.path.join("/", "home", "clustering_benchmarking", "results"))
    seed = 42
    random.seed(seed)
    np.random.seed(seed)

    with open(os.path.join("resources", "configspace.json"), "r") as f:
        json_string = f.read()
        cs = cs_json.read(json_string)

    cs.add_hyperparameter(
        Categorical("kind", ["100", "010", "001", "110", "101", "011", "111"])
    )

    cs.add_condition(
        InCondition(cs["noisy_features"], cs["kind"], ["100", "110", "101", "111"])
    )
    cs.add_condition(
        InCondition(cs["correlated_features"], cs["kind"], ["010", "110", "011", "111"])
    )
    cs.add_condition(
        InCondition(cs["distorted_features"], cs["kind"], ["001", "101", "011", "111"])
    )

    # cs_string = cs_json.write(cs)
    # with open(os.path.join("resources", "configspace.json"), "w") as f:
    #     f.write(cs_string)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        tot_configs = 20
        current_round = 0
        final_configs = []
        final_clusterings = []

        print("--- GENERATE CONFIGURATIONS ---")
        with tqdm(total=tot_configs) as pbar:
            while len(final_configs) < tot_configs:
                current_configs = create_configs(
                    cs=cs, n_configs=tot_configs - len(final_configs)
                )

                current_round += 1
                for config in current_configs:
                    try:
                        config["round"] = current_round
                        final_clusterings.append(generate_clusters(config))
                        final_configs.append(config)
                        pbar.update()
                    except:
                        pass

        with open(os.path.join(output_path, "configs.json"), "w") as file:
            json.dump({idx: config for idx, config in enumerate(final_configs)}, file)

        to_export = [
            "n_instances",
            "n_clusters",
            "n_clusters_ratio",
            "cluster_std",
            "initial_sil",
            "final_sil",
            "support_total_features",
            "n_features",
            "support_noisy_features",
            "support_correlated_features",
            "support_distorted_features",
            "noisy_features",
            "correlated_features",
            "distorted_features",
            "round",
        ]
        pd.read_json(os.path.join(output_path, "configs.json")).transpose()[
            to_export
        ].to_csv(os.path.join(output_path, "configs.csv"))

        print("--- GENERATE CLUSTERINGS ---")
        with tqdm(total=tot_configs) as pbar:
            for id_clustering, clustering_dict in enumerate(final_clusterings):
                for label, clustering in clustering_dict.items():
                    clustering_name = f"syn{id_clustering}_{label}"
                    fig = plot_cluster_data(clustering, "target")
                    fig.savefig(
                        os.path.join(
                            make_dir(os.path.join(output_path, "img")),
                            f"{clustering_name}.png",
                        ),
                        dpi=300,
                        bbox_inches="tight",
                    )
                    plt.close(fig)

                    suffix = "" if "final" in label else f"_{label}"
                    output_folder = "final" if "final" in label else "raw"
                    clustering_name = f"syn{id_clustering}{suffix}"
                    clustering.to_csv(
                        os.path.join(
                            make_dir(os.path.join(output_path, output_folder)),
                            f"{clustering_name}.csv",
                        ),
                        index=False,
                        header=None,
                    )
                pbar.update()
