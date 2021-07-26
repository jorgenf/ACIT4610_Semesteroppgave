from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pickle_name = Path("plots/results.pkl")

df = pd.read_pickle(pickle_name)

ax = sns.pointplot(
    x="DIV",
    y="fitness",
    data=df,
    hue="reference culture",
)

plt.show()