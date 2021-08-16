from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pickle_name = Path("plots/individual_results_test.pkl")

df = pd.read_pickle(pickle_name)

# plot esthetics
sns.set_context("notebook")
width = 7.16
aspect_ratio = 2

# set hue theme
model_palette = {
    "CA" : "#509A29", # green
    "Network" : "#2A74BC" # blue
    }

df = pd.melt(
    df, 
    id_vars=["Generation", "Rank", "Culture", "DIV", "Number of generations", "Model type", "Population size"],
    var_name="Fitness type",
    value_vars=["Temporal", "Spatial", "Overall"],
    value_name="Fitness"
    )

total_n_plots = len(df["Culture"].unique()) * len(df["DIV"].unique()) * 2
n_plots = 0
for culture in df["Culture"].unique():
    for div in df["DIV"].unique():

        n_gens=df["Number of generations"].loc[
            (df["DIV"] == div) &
            (df["Culture"] == culture)
            ].unique()[0]

        n_inds=df["Population size"].loc[
            (df["DIV"] == div) &
            (df["Culture"] == culture)
            ].unique()[0]
        
        for rank in [10, n_inds]:
            n_plots += 1
            print(f"Creating plot {n_plots}/{total_n_plots}", end="\r")
            ax = sns.relplot(
                data=df.loc[
                    (df["Rank"] <= rank) &
                    (df["DIV"] == div) &
                    (df["Culture"] == culture)
                    ],
                # data=df,
                x="Generation",
                y="Fitness",
                # style="Reference culture",
                # hue="Fitness type",
                hue="Model type",
                style="Fitness type",
                kind="line",
                height=(width/aspect_ratio),
                palette=model_palette,
            )

            ax.set(
                title=f"{culture} {div} DIV  top {rank}",
                # title=f"Top {rank} phenotypes",
                yticks=(0, 0.5, 1),
                xticks=(0, n_gens-1)
                # xticks=range(0, n_gens, n_gens//5)
                )
            
            ax.savefig(Path(f"plots/figures/fitness_vs_gen/{culture}-{div}_top-{rank}"))
            plt.close()

# plt.show()
print("\nDone")