from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import time
import math

import Code.Data as Data


sim_length = 1800
sim_start = 0
#  Model Type (Wagenaar, CA or Network)
model_type = "Network"
# where to find data
culture_name = "network_small_6-2"
evo_folder_name = "network_dim10_pop60_gen80_dur60_res40_mut0.1_par0.5_ret0.05_6-2-10_20210808021425"
file_name = "0.txt"
#  Wagenaar Switch
if model_type == "Wagenaar":
	file_name = culture_name + ".spk.txt"
#  Path magic
pickle_name = Path("plots/pickles/20210818")
experiment_folder = Path("E:/Library/Documents/OneDrive - OsloMet/SSCI ICES paper/NEW NEW RESULTS - Now with more results")
culture_folder = Path(experiment_folder, culture_name, "BEST")
single_runs_folder = Path(culture_folder, evo_folder_name, "single_runs")
# where to save plots
savepath = Path("plots/figures/raster_ASDR")

# esthetics
sns.set_context("paper")
width = 7.16
height = 2.5
aspect_ratio = 10
font_size = 10
dpi = 500
raster_width = 0.5

# set color theme
model_palette = {
	#  "CA": "#509A29",  # green
	"CA": "#509A29",  # green
	"Network": "#2A74BC",  # blue
	"Wagenaar": "#c76a18"   #orange
}

savepath.mkdir(parents=True, exist_ok=True)
#  df = pd.read_pickle(Path(f"{pickle_name}/individual_data.pkl"))
#  df = pd.read_pickle(Path(f"{pickle_name}/pheno_data.pkl"))

spikes_file = None
#  Wagenaar Switch
if model_type == "Wagenaar":
	spikes_file = Data.get_spikes_file(Path("../../Resources", file_name), recording_start=sim_start, recording_len=sim_length, fullpath=True)
else:
	spikes_file = Data.get_spikes_file(Path(single_runs_folder, file_name), recording_start=sim_start,
	                                   recording_len=sim_length, fullpath=True)
spike_rate = Data.get_spikerate(spikes_file, sim_length, sim_start)

#   Check if input is in the correct format
spikes_file = np.array(
   [(row[0], row[1]) for row in spikes_file],
   dtype=[("t", "float64"), ("electrode", "int64")])
#   Sort spikes by electrode
A_spikes_per_array = [[] for _ in range(60)]
for row in spikes_file:
   A_spikes_per_array[row[1]].append(row[0])
   

#   Initialize plot
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex="all", sharey="row", figsize=(width, height))

#   Make raster plots
ax1.eventplot(
   A_spikes_per_array,
   linewidths=raster_width, color=model_palette[model_type]
)
#  ax1.set_xlabel("Minutes", fontsize=font_size)
#  ax1.set_ylabel("Electrode", fontsize=font_size)
ax1.set_position([0, 0, 0, 0])

#  Make lineplot
line_x = np.arange(sim_start, sim_length)
line_y = spike_rate
ax2.plot(
	line_x,
	line_y,
	color=model_palette[model_type], lw=0.2
)
ax2.set_xlabel("Minutes", fontsize=font_size)
#  ax2.set_ylabel("Spikes / M", fontsize=font_size)
ax2.set_position([1, 1, 1, 1])
#  fig.tight_layout()

#   Make histograms
#ax2.hist(spikes_file["t"], bins=sim_length)
#ax2.set_xlabel("Seconds")
#ax2.set_ylabel("Spikes per second")

#  ax1_y_limit = ax1.get_ylim()
#  ax2_y_limit = ax2.get_ylim()
#  ax2_y_limit = (math.ceil(ax2_y_limit[0]), math.floor(ax2_y_limit[1]))
ax2_y_limit = (spike_rate.min(), spike_rate.max())

formatter = ticker.FuncFormatter(lambda s, x: time.strftime('%M', time.gmtime(s)))
ax1.xaxis.set_major_locator(plt.FixedLocator((sim_start, sim_length), sim_length))
ax2.xaxis.set_major_locator(plt.FixedLocator((sim_start, sim_length), sim_length))
ax1.xaxis.set_major_formatter(formatter)
ax2.xaxis.set_major_formatter(formatter)
ax1.yaxis.set_major_locator(plt.FixedLocator((0, 60), 60))
ax2.yaxis.set_major_locator(plt.FixedLocator((ax2_y_limit[0], ax2_y_limit[1]), ax2_y_limit[1]))

#fig.set_figheight(6)
#fig.set_figwidth(7.16)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
fig.savefig(Path(savepath, culture_name), dpi=dpi)
plt.close()

np.set_printoptions(threshold=np.inf)
#  print("SPIKE FILE\n{}\n".format(len(spikes_file)))
#  print("SPIKE RATE\n{}\n".format(spike_rate.max()))
#  print("SPIKES PER ARRAY\n{}\n".format(len(A_spikes_per_array)))
#  print(ax1_y_limit)
#  print(ax2_y_limit)

'''
total_n_plots = len(df["Culture"].unique()) * len(df["DIV"].unique()) * 2
n_plots = 0
for culture in df["Culture"].unique():
	for div in df["DIV"].loc[df["Culture"] == culture].unique():
		for ID in df["Experiment ID"].loc[df["DIV"] == div].unique():
			pass
'''

print("\nDone")
