import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.interpolate
import json
import os


def plot_cntr(phase, param_phases, df, t_C_range, p_MPa_range):
    # load parameters from config file
    param = param_phases[phase]
    content_col = param["content"]
    mass_col = param["mass"]
    content_name = param["content_name"]
    content_range = param["range"]

    # load temperature and pressure
    xy = df.loc[:, ["T (C)", "P (MPa)"]]
    x = df["T (C)"]
    y = df["P (MPa)"]
    #title = phase + ", " + str(df["bulk wt% SiO2"].iat[0]) + " wt% SiO$_2$, " + str(df["bulk wt% H2O"].iat[0]) + " wt% H$_2$O, " + str(df["Oxide buffer"].iat[0])
    content = df[content_col]
    mass = df[mass_col]
    xi = np.linspace(800, 1400, 600)
    yi = np.linspace(0, 600, 600)
    xi, yi = np.meshgrid(xi, yi)

    ci = scipy.interpolate.griddata(xy, content, (xi, yi))
    mi = scipy.interpolate.griddata(xy, mass, (xi, yi))

    fig, ax = plt.subplots(figsize=(5, 4))
    #ax.set_title(title, fontsize=10)
    plot = ax.scatter(x, y, marker="s", s=50, c=content, cmap="turbo")
    cbar = fig.colorbar(plot, ax=ax)
    plot.set_clim(*content_range)
    cbar.set_label(content_name, fontsize=10)

    c_cont1 = plt.contour(xi, yi, ci, colors=["k"], linewidths=0.2, linestyles="solid", levels=[i for i in range(100)])
    c_cont2 = plt.contour(xi, yi, ci, colors=["k"], linewidths=0.5, linestyles="solid", levels=[10 * i for i in range(100)])
    c_cont2.clabel(fmt="%d", fontsize=8)

    m_cont1 = plt.contour(xi, yi, mi, colors=["w"], linewidths=0.2, linestyles="dashed", levels=[i for i in range(100)])
    m_cont2 = plt.contour(xi, yi, mi, colors=["w"], linewidths=0.5, linestyles="dashed", levels=[10 * i for i in range(100)])
    m_cont2.clabel(fmt="%d", fontsize=8)

    ax.set_xlim(*t_C_range)
    ax.set_ylim(*p_MPa_range)

    ax.set_xlabel("Temperature ($^{\circ}$C)")
    ax.set_ylabel("Pressure (MPa)")
    return fig

def main():
    # load config file
    with open("config.json") as f:
        config = json.load(f)["plot_ptx"]
    filename = config["Summary file"]
    param_phases = config["Phase"]
    phases = list(param_phases.keys())
    t_C_range = config["Temperature range (C)"]
    p_MPa_range = config["Pressure range (MPa)"]

    df = pd.read_csv("summary/" + filename + ".csv")

    for phase in phases:
        fig = plot_cntr(phase, param_phases, df, t_C_range, p_MPa_range)
        if not os.path.exists("cntr/" + filename):
            os.makedirs("cntr/" + filename)
        fig.savefig(
            "cntr/" + filename + "/" + phase + ".tif",
            dpi=300, bbox_inches="tight"
            )

if __name__ == "__main__":
    main()