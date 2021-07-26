from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pickle_name = Path("plots/results.pkl")

df = pd.read_pickle(pickle_name)

ax = sns.relplot(
    data=df,
    x="generation",
    y="fitness",
    hue="reference culture",
    style="model type",
    kind="line"
)

plt.show()