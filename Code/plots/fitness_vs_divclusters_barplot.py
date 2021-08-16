from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pickle_name = Path("plots/pickles/individual_20210816.pkl")

df = pd.read_pickle(pickle_name)
df["Generation"] = df["Generation"].astype(int)

# pick only top individuals from each experiment
rank = 10
filtered_df = pd.DataFrame()
for parameter_name in df["DIV"].unique():
    filtered_df = filtered_df.append(df.loc[df["DIV"] == parameter_name].sort_values("Fitness", ascending=False).groupby("Experiment ID").head(rank))
df = filtered_df
print(df)

sns.set_context("paper")
font_size = 9
width = 7.16 / 1
aspect_ratio = 1.9
culture_order = ["Sparse", "Small & sparse", "Small", "Dense"] # "Ultra sparse" left out

# plot fitness vs div
for model_type in df["Model type"].unique():
    min_gen = df["Number of generations"].min() # normalize gens to minimum
    
    if model_type == "CA":
        color_theme = "Greens_d"
    else:
        color_theme = "Blues_d"

    ax = sns.barplot(
        data=df.loc[(df["Model type"] == model_type)],
        order=culture_order,
        x="Culture",
        y="Fitness",
        hue="DIV",
        ci="sd",
        palette=color_theme,
    )

    ax.set_xlabel("Culture and DIV", fontsize=font_size)
    ax.set_ylabel("Fitness", fontsize=font_size)
    ax.tick_params(labelsize=font_size)

    ax.set(
        title=f"{model_type} top {rank}",
        yticks=(0, 0.5, 1),
        )

    ax.get_legend().remove()
    
    fig = ax.get_figure()
    fig.set_size_inches(width, width/aspect_ratio)
    fig.savefig(Path(f"plots/figures/fitness_vs_div_clusters/{model_type}_top-{rank}"), dpi=300)
    plt.close()