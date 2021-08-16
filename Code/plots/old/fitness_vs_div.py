from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pickle_name = Path("plots/individual_results_test.pkl")

df = pd.read_pickle(pickle_name)
df["Generation"] = df["Generation"].astype(int)

sns.set_context("notebook")
width = 7.16
aspect_ratio = 2

# set hue theme
model_palette = {
    "CA" : "#509A29", # green
    "Network" : "#2A74BC" # blue
    }

parameter_palette = {
    "Temporal" : "#A82C40", # red,
    "Spatial" : "#B19B2F", # yellow
    "Overall" : "#1979AD", # blue
}

# plot fitness vs div
for culture in df["Culture"].unique():
    min_gen = df["Number of generations"].min() # normalize gens to minimum
    
    ax = sns.pointplot(
        data=df.loc[(df["Culture"] == culture) & (df["Generation"] <= min_gen)],
        x="DIV",
        y="Overall",
        hue="Model type",
        palette=model_palette
    )


    ax.set(
        title=f"{culture}",
        yticks=(0, 0.5, 1),
        # xticks=(0, n_gens-1)
        # xticks=range(0, n_gens, n_gens//5)
        )
    
    fig = ax.get_figure()
    fig.savefig(Path(f"plots/figures/fitness_vs_div/{culture}"))
    plt.close()


# plot fitness components vs div
df = pd.melt(
    df, 
    id_vars=["DIV", "Culture", "Model type", "Generation"],
    var_name="Fitness type",
    value_vars=["Temporal", "Spatial", "Overall"],
    value_name="Value"
    )

for culture in df["Culture"].unique():
    for model in df["Model type"].unique():

        ax = sns.pointplot(
            data=df.loc[(df["Culture"] == culture) & (df["Model type"] == model) & (df["Generation"] <= min_gen)],
            x="DIV",
            y="Value",
            hue="Fitness type",
            palette=parameter_palette,
        )


        ax.set(
            title=f"{culture} using {model} model",
            yticks=(0, 0.5, 1),
            # xticks=(0, n_gens-1)
            # xticks=range(0, n_gens, n_gens//5)
            )
        
        fig = ax.get_figure()
        fig.savefig(Path(f"plots/figures/fitness_vs_div/{model}_{culture}"))
        plt.close()