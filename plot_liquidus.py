import json
import sys
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def search_liquidus(phase_name, ps_MPa, df):
    column_name = phase_name + " mass (gm)"
    ts_C = []
    for p_MPa in ps_MPa:
        df_tmp = df[df["P (MPa)"] == p_MPa]
        df_tmp = df_tmp[["T (C)", column_name]].dropna(subset=[column_name])
        ts_C.append(df_tmp["T (C)"].max())
    return ts_C

def get_diff(ts_C_1, ts_C_2):
    diffs = []
    for i, t_C in enumerate(ts_C_1):
        diff = ((ts_C_1[i] - ts_C_2[i]) ** 2) ** 0.5
        diffs.append(diff)
    return diffs

# load a config file
config = json.load(open("config.json", "r"))["plot_liquidus"]
p1_xlim = config["p1_xlim"]
p1_ylim = config["p1_ylim"]
phase1 = config["Phase1"]
phase2 = config["Phase2"]
ps_range = config["Pressure range (MPa)"]

# extract csv files from summary directories
filelist = [file for file in os.listdir("summary") if file.endswith(".csv")]
filelist_wo_extension = [os.path.splitext(file)[0] for file in filelist]

ps_MPa = np.arange(*ps_range, 1)

for filename in filelist_wo_extension:
    df = pd.read_csv("summary/" + filename + ".csv")
    ts_C_1 = search_liquidus(phase1, ps_MPa, df)
    ts_C_2 = search_liquidus(phase2, ps_MPa, df)
    
    diffs = get_diff(ts_C_1, ts_C_2)
    try:
        solved_P_MPa = ps_MPa[diffs.index(np.nanmin(diffs))]
    except:
        solved_P_Ma = 0
    print(solved_P_MPa)

    # export liquidus temperature to csv files
    output = {
        "P (MPa)": ps_MPa,
        phase1 + " liquidus (C)": ts_C_1,
        phase2 + "opx liquidus (C)": ts_C_2,
        "Residual": diffs
    }

    pd.DataFrame(output).to_csv("liquidus/" + filename + ".csv")

    fig, ax = plt.subplots(
        1, 2, sharey=True,
        gridspec_kw=dict(width_ratios=(2, 1), wspace=0.2)
        )
    ax[0].plot(ts_C_1, ps_MPa, "-", label=phase1)
    ax[0].plot(ts_C_2, ps_MPa, "-", label=phase2)
    ax[0].set_xlim(*p1_xlim)
    ax[0].set_ylim(*p1_ylim)
    ax[0].legend()
    ax[0].set_xlabel("Temperature ($^\circ$C)")
    ax[0].set_ylabel("Pressure (MPa)")

    ax[1].plot(diffs, ps_MPa, "-o", c="k")
    #ax[1].hlines(solved_P_MPa, 0, 50, linewidth=1, linestyle="solid", color="r")
    ax[1].axhline(y=solved_P_MPa, linewidth=1, linestyle="solid", color="r")
    ax[1].vlines(10, 0, 200, linewidth=1, linestyle="dashed", color="k")
    ax[1].set_xlim(1,)
    ax[1].set_xscale("log")
    ax[1].set_xlabel(r"$|T_\mathrm{pl}^\mathrm{liquidus} - T_\mathrm{opx}^\mathrm{liquidus}|$")
    fig.savefig("plots/" + filename + ".jpg", dpi=300)
    plt.close()
