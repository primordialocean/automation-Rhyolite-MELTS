import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.interpolate

def plot_2d(df):
    
    xy = df.loc[:, ["T (C)", "P (MPa)"]]
    x = df["T (C)"]
    y = df["P (MPa)"]

    param_phases = {
        "pl": {"content": "pl An", "mass": "pl mass (gm)", "content_name": "Anorthite (mol%)", "range": (30, 100)},
        "aug": {"content": "aug Mg#", "mass": "aug mass (gm)", "content_name": "Mg#", "range": (30, 90)},
        "pig": {"content": "pig Mg#", "mass": "pig mass (gm)", "content_name": "Mg#", "range": (30, 90)},
        "opx": {"content": "opx Mg#", "mass": "opx mass (gm)", "content_name": "Mg#", "range": (30, 90)},
        "ol": {"content": "ol Fo", "mass": "ol mass (gm)", "content_name": "Forstelite (mol%)", "range": (30, 90)}
    }

    for phase in ["pl", "aug", "pig", "opx", "ol"]:
        param = param_phases[phase]
        content_col = param["content"]
        mass_col = param["mass"]
        content_name = param["content_name"]
        content_range = param["range"]

        title = phase + ", " + str(df["bulk wt% SiO2"].iat[0]) + " wt% SiO$_2$, " + str(df["bulk wt% H2O"].iat[0]) + " wt% H$_2$O, " + str(df["Oxide buffer"].iat[0])
        content = df[content_col]
        mass = df[mass_col]
        xi = np.linspace(800, 1400, 600)
        yi = np.linspace(0, 600, 600)
        xi, yi = np.meshgrid(xi, yi)

        ci = scipy.interpolate.griddata(xy, content, (xi, yi))
        mi = scipy.interpolate.griddata(xy, mass, (xi, yi))
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.set_title(title, fontsize=10)
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

        ax.set_xlim(850, 1250)
        ax.set_ylim(0, 600)

        plt.xlabel("Temperature ($^{\circ}$C)")
        plt.ylabel("Pressure (MPa)")

        plt.savefig("cntr/" + phase + ".tif", dpi=300, bbox_inches="tight")

def main():
    df = pd.read_csv("summary/summary_58 wt% SiO2_3.0 wt% H2O.csv")
    plot_2d(df)

if __name__ == "__main__":
    main()