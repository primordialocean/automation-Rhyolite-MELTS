import json
import sys
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# load a config file
config = json.load(open("config.json", "r"))["search_liquidus"]
ps_MPa = config["ps_MPa"]
p1_xlim = config["p1_xlim"]
p1_ylim = config["p1_ylim"]
p2_xlim = config["p2_xlim"]
plot_phase = config["plot_phase"]

# extract csv files from summary directories
filelist = [file for file in os.listdir("summary") if file.endswith(".csv")]
filelist_wo_extension = [os.path.splitext(file)[0] for file in filelist]

for filename in filelist_wo_extension:
    df = pd.read_csv("summary/" + filename + ".csv")

    pl_ts_C = []
    for p_MPa in ps_MPa:
        df_t = df[df["P (MPa)"] == p_MPa]
        df_t = df_t[["T (C)", "pl mass (gm)"]].dropna(subset=["pl mass (gm)"])
        pl_ts_C.append(df_t["T (C)"].max())

    opx_ts_C = []
    for p_MPa in ps_MPa:
        df_t = df[df["P (MPa)"] == p_MPa]
        df_t = df_t[["T (C)", "opx mass (gm)"]].dropna(subset=["opx mass (gm)"])
        opx_ts_C.append(df_t["T (C)"].max())

    aug_ts_C = []
    for p_MPa in ps_MPa:
        df_t = df[df["P (MPa)"] == p_MPa]
        df_t = df_t[["T (C)", "aug mass (gm)"]].dropna(subset=["aug mass (gm)"])
        aug_ts_C.append(df_t["T (C)"].max())

    # export liquidus temperature to csv files
    output = {
        "P (MPa)": ps_MPa,
        "pl liquidus (C)": pl_ts_C,
        "opx liquidus (C)": opx_ts_C,
        "aug liquidus (C)": aug_ts_C
    }

    pd.DataFrame(output).to_csv("liquidus/" + filename + ".csv")

    fig, ax = plt.subplots(
        1, 2, sharey=True,
        gridspec_kw=dict(width_ratios=(2, 1), wspace=0.1)
        )
    if plot_phase["pl"] == True:
        ax[0].plot(pl_ts_C, ps_MPa, "-o", label="pl")
    if plot_phase["opx"] == True:
        ax[0].plot(opx_ts_C, ps_MPa, "-o", label="opx")
    if plot_phase["aug"] == True:
        ax[0].plot(aug_ts_C, ps_MPa, "-o", label="aug")
    ax[0].set_xlim(*p1_xlim)
    ax[0].set_ylim(*p1_ylim)
    ax[0].legend()
    ax[0].set_xlabel("Temperature ($^\circ$C)")
    ax[0].set_ylabel("Pressure (MPa)")

    diffs = []
    for i, pl_t_C in enumerate(pl_ts_C):
        diff = ((pl_ts_C[i] - opx_ts_C[i]) ** 2) ** 0.5
        diffs.append(diff)

    min_diff = min(diffs)
    solved_P_MPa = ps_MPa[diffs.index(min_diff)]

    ax[1].plot(diffs, ps_MPa, "-o", c="k")
    if min_diff <= 5:
        ax[1].hlines(solved_P_MPa, 0, 50, linewidth=1, linestyle="solid", color="r")
    else:
        pass
    ax[1].vlines(5, 0, 200, linewidth=1, linestyle="dashed", color="k")
    ax[1].set_xlim(*p2_xlim)
    ax[1].set_xlabel(r"$|T_\mathrm{pl}^\mathrm{liquidus} - T_\mathrm{opx}^\mathrm{liquidus}|$")
    fig.savefig("plots/" + filename + ".jpg", dpi=300)
    plt.close()
