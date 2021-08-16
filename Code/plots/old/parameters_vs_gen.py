from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pickle_name = Path("plots/param_results_test.pkl")

df = pd.read_pickle(pickle_name)

ax = sns.relplot(
    data=df.loc[df["gene"] == "Density constant"],
    x="generation",
    y="value",
    hue="gene",
    style="reference phenotype",
    kind="line"
)

plt.show()

# print(sns.plotting_context())
# sns.set_theme()
# settings = sns.set_context()
# # settings = sns.plotting_context()
# for key in settings:
#     print(key, settings[key])