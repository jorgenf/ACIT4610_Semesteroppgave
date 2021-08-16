from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# plot esthetics
sns.set_context("notebook")
width = 7.16
aspect_ratio = 2

# set hue theme
model_palette = {
    "CA" : "#509A29", # green
    "Network" : "#2A74BC" # blue
    }

rank = 10 # plot top x individuals

pickle_name = Path("plots/pickles/param_20210816.pkl")

df = pd.read_pickle(pickle_name)
df["Generation"] = df["Generation"].astype(int)

gene_functions = {
        "Firing threshold" : lambda x : (x * 5) + 0.1,
        "Random fire probability" : lambda x : x * 0.15,
        "Refractory period" : lambda x : round(x * 10),
        "Inhibition percentage" : lambda x : x * 0.5,
        "Leak constant" : lambda x : x * 0.2,
        "Integration constant" : lambda x : x * 0.5,
    }

def normalize_gene(row):
    for key in gene_functions:
        if row["Model parameter"] == key: 
            return gene_functions[key](row["Gene value"])
    
    if row["Model parameter"] == "Density constant" and row["Model type"] == "CA":
        return round(row["Gene value"] * 5) + 1
    elif row["Model parameter"] == "Density constant" and row["Model type"] == "Network":
        return round(row["Gene value"] * 4) + 0.1
    else:
        print(f"Error: '{key}' not found")

# pick only top individuals from each experiment
filtered_df = pd.DataFrame()
for parameter_name in df["Model parameter"].unique():
    filtered_df = filtered_df.append(df.loc[df["Model parameter"] == parameter_name].sort_values("Fitness", ascending=False).groupby("Experiment ID").head(rank))
    # print(df.loc[df["Model parameter"] == parameter_name].sort_values("Fitness", ascending=False).groupby("Experiment ID").head(rank))
df = filtered_df

# translate gene to parameter value
df["Parameter value"] = df.apply(normalize_gene, axis=1)

print(df)

# self.firing_threshold = (individual.genotype[0] * 5) + 0.1

# self.random_fire_prob = individual.genotype[1] * 0.15
# self.refractory_period = round(individual.genotype[2] * 10)
# self.inhibition_percentage = individual.genotype[3] * 0.5
# self.leak_constant = individual.genotype[4] * 0.2
# self.integ_constant = individual.genotype[5] * 0.5
# if self.model == "ca":
#     self.density_constant = round(individual.genotype[6] * 5) + 1
# elif self.model == "network":
#     self.density_constant = (individual.genotype[6] * 4) + 0.1
# else:
#     raise Exception("Invalid model chosen.")


sns.set_context("notebook")
width = 7.16
aspect_ratio = 2


# plot parameters vs div
total_n_plots = \
    len(df["Model type"].unique()) * len(df["Culture"].unique()) * 1 \
    + len(df["Model parameter"].unique()) * len(df["Culture"].unique()) * 1
n_plots = 0

def parameter_limits(model_parameter):
    if model_parameter == "Density constant":
        return (0, 6)
    else:
        return (gene_functions[model_parameter](0), gene_functions[model_parameter](1))

# plot normalized parameters vs div
for model_parameter in df["Model parameter"].unique():

    param_min, param_max = parameter_limits(model_parameter)

    for culture in df["Culture"].unique():

        n_gens=df["Number of generations"].loc[
            (df["Model parameter"] == model_parameter) &
            (df["Culture"] == culture)
            ].unique()[0]

        n_inds=df["Population size"].loc[
            (df["Model parameter"] == model_parameter) &
            (df["Culture"] == culture)
            ].unique()[0]

        n_plots += 1
        print(f"Creating plot {n_plots}/{total_n_plots}", end="\r")
        
        div_order = df["DIV"].loc[
                (df["Model parameter"] == model_parameter) &
                (df["Culture"] == culture)
                ].unique()
        div_order.sort()

        ax = sns.pointplot(
            data=df.loc[
                (df["Model parameter"] == model_parameter) &
                (df["Culture"] == culture)
                ],
            x="DIV",
            y="Parameter value",
            hue="Model type",
            order=div_order,
            palette=model_palette,
            capsize=0.2,
            ci="sd",
            dodge=True,
            join=False,
        )

        # ax = sns.barplot(
        #     data=df.loc[
        #         (df["Model parameter"] == model_parameter) &
        #         (df["Culture"] == culture) #&
        #         ],
        #     x="DIV",
        #     y="Parameter value",
        #     hue="Model type",
        #     palette=model_palette,
        # )
        
        ax.set(
            title=f"{model_parameter} {culture} top-{rank}",
            yticks=(param_min, param_max),
            )
        
        fig = ax.get_figure()
        fig.savefig(Path(f"plots/figures/parameter_vs_div/{model_parameter}_{culture}_top-{rank}"))
        plt.close()

print("\nDone")