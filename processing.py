import pandas as pd
import numpy as np
import json
import sys

molecular_weights = {
    "TiO2": 79.8658,
    "Al2O3": 101.961,
    "FeO": 71.844,
    "Fe2O3": 159.69,
    "MgO": 40.304,
    "CaO": 56.0774,
    "Na2O": 61.98,
    "K2O": 94.2
}

def process_liq(filepath):
    elements = [
        "wt% SiO2", "wt% TiO2", "wt% Al2O3", "wt% FeOt", "wt% MnO", "wt% MgO",
        "wt% CaO", "wt% Na2O", "wt% K2O", "wt% P2O5"
    ]
    outputs = [
        "T (C)", "P (MPa)", "liq mass (gm)",
        "wt% SiO2", "wt% TiO2", "wt% Al2O3", "wt% FeOt", "wt% MnO", "wt% MgO",
        "wt% CaO", "wt% Na2O", "wt% K2O", "wt% P2O5", "wt% H2O"]
    df_liq = pd.read_csv(filepath + "melts-liquid.csv")
    df_liq["P (MPa)"] = 100 * df_liq["P (kbars)"]
    df_liq["wt% FeOt"] = df_liq["wt% FeO"] + 0.9 * df_liq["wt% Fe2O3"]
    df_liq[elements] = df_liq[elements].apply(lambda x: x * 100 / x.sum(), axis=1)
    df_liq = df_liq[outputs]
    return df_liq

def process_ol(filepath):
    ol_outputs = ["T (C)", "P (MPa)", "ol mass (gm)", "ol Fo", "ol wt% CaO"]
    df_ol = pd.read_csv(filepath + "olivine.csv")

    df_ol["P (MPa)"] = 100 * df_ol["P (kbars)"]

    FeO_wt = df_ol["wt% FeO"]
    MgO_wt = df_ol["wt% MgO"]

    FeO_mp = FeO_wt / molecular_weights["FeO"]
    MgO_mp = MgO_wt / molecular_weights["MgO"]

    Fo = 100 * MgO_mp / (MgO_mp + FeO_mp)

    df_ol["ol Fo"] = Fo
    df_ol["ol wt% CaO"] = df_ol["wt% CaO"]
    df_ol["ol mass (gm)"] = df_ol["mass (gm)"]

    df_ol = df_ol[ol_outputs]
    return df_ol


def process_cpx(filepath):
    aug_outputs = ["T (C)", "P (MPa)", "aug mass (gm)", "aug Wo", "aug Mg#"]
    pig_outputs = ["T (C)", "P (MPa)", "pig mass (gm)", "pig Wo", "pig Mg#"]
    df_cpx = pd.read_csv(filepath + "clinopyroxene.csv")

    df_cpx["P (MPa)"] = 100 * df_cpx["P (kbars)"]

    FeO_wt = df_cpx["wt% FeO"]
    Fe2O3_wt = df_cpx["wt% Fe2O3"]
    MgO_wt = df_cpx["wt% MgO"]
    CaO_wt = df_cpx["wt% CaO"]

    FeO_mp = FeO_wt / molecular_weights["FeO"]
    Fe2O3_mp = Fe2O3_wt / molecular_weights["Fe2O3"]
    MgO_mp = MgO_wt / molecular_weights["MgO"]
    CaO_mp = CaO_wt / molecular_weights["CaO"]

    Wo = 100 * CaO_mp / (CaO_mp + MgO_mp + FeO_mp + 2 * Fe2O3_mp)
    Mg_num = 100 * MgO_mp / (MgO_mp + FeO_mp)

    df_cpx["Wo"] = Wo
    df_cpx["Mg#"] = Mg_num

    df_aug = df_cpx.drop_duplicates(subset="Index", keep="first").copy()
    df_pig = df_cpx[~df_cpx["wt% SiO2"].isin(df_aug["wt% SiO2"])].copy()
    df_aug["aug mass (gm)"] = df_aug["mass (gm)"]
    df_aug["aug Wo"] = df_aug["Wo"]
    df_aug["aug Mg#"] = df_aug["Mg#"]
    df_pig["pig mass (gm)"] = df_pig["mass (gm)"]
    df_pig["pig Wo"] = df_pig["Wo"]
    df_pig["pig Mg#"] = df_pig["Mg#"]
    df_aug = df_aug[aug_outputs]
    df_pig = df_pig[pig_outputs]
    return df_aug, df_pig

def process_opx(filepath):
    opx_outputs = ["T (C)", "P (MPa)", "opx mass (gm)", "opx Wo", "opx Mg#"]
    df_opx = pd.read_csv(filepath + "orthopyroxene.csv")

    df_opx["P (MPa)"] = 100 * df_opx["P (kbars)"]

    FeO_wt = df_opx["wt% FeO"]
    Fe2O3_wt = df_opx["wt% Fe2O3"]
    MgO_wt = df_opx["wt% MgO"]
    CaO_wt = df_opx["wt% CaO"]

    FeO_mp = FeO_wt / molecular_weights["FeO"]
    Fe2O3_mp = Fe2O3_wt / molecular_weights["Fe2O3"]
    MgO_mp = MgO_wt / molecular_weights["MgO"]
    CaO_mp = CaO_wt / molecular_weights["CaO"]

    Wo = 100 * CaO_mp / (CaO_mp + MgO_mp + FeO_mp + 2 * Fe2O3_mp)
    Mg_num = 100 * MgO_mp / (MgO_mp + FeO_mp)

    df_opx["opx Wo"] = Wo
    df_opx["opx Mg#"] = Mg_num
    df_opx["opx mass (gm)"] = df_opx["mass (gm)"]

    df_opx = df_opx[opx_outputs]
    return df_opx

def process_amp(filepath):
    amp_outputs = ["T (C)", "P (MPa)", "amp mass (gm)"]
    df_amp = pd.read_csv(filepath + "amphibole.csv")

    df_amp["P (MPa)"] = 100 * df_amp["P (kbars)"]
    df_amp["amp mass (gm)"] = df_amp["mass (gm)"]

    df_amp = df_amp[amp_outputs]
    return df_amp

def process_hbl(filepath):
    hbl_outputs = ["T (C)", "P (MPa)", "hbl mass (gm)"]
    df_hbl = pd.read_csv(filepath + "hornblende.csv")

    df_hbl["P (MPa)"] = 100 * df_hbl["P (kbars)"]
    df_hbl["hbl mass (gm)"] = df_hbl["mass (gm)"]

    df_hbl = df_hbl[hbl_outputs]
    return df_hbl

def process_bt(filepath):
    bt_outputs = ["T (C)", "P (MPa)", "bt mass (gm)"]
    df_bt = pd.read_csv(filepath + "biotite.csv")

    df_bt["P (MPa)"] = 100 * df_bt["P (kbars)"]
    df_bt["bt mass (gm)"] = df_bt["mass (gm)"]

    df_bt = df_bt[bt_outputs]
    return df_bt

def process_fld(filepath):
    global molecular_weights
    pl_outputs = ["T (C)", "P (MPa)", "pl mass (gm)", "pl An", "pl Or"]
    kfs_outputs = ["T (C)", "P (MPa)", "kfs mass (gm)", "kfs An", "kfs Or"]

    df_fld = pd.read_csv(filepath + "feldspar.csv")
    df_fld["P (MPa)"] = 100 * df_fld["P (kbars)"]

    CaO_wt = df_fld["wt% CaO"]
    Na2O_wt = df_fld["wt% Na2O"]
    K2O_wt = df_fld["wt% K2O"]

    CaO_mp = CaO_wt / molecular_weights["CaO"]
    Na2O_mp = Na2O_wt / molecular_weights["Na2O"]
    K2O_mp = K2O_wt / molecular_weights["K2O"]

    An = 100 * CaO_mp / (CaO_mp + 2 * Na2O_mp + 2 * K2O_mp)
    Or = 100 * 2 * K2O_mp / (CaO_mp + 2 * Na2O_mp + 2 * K2O_mp)
    df_fld["An"] = An
    df_fld["Or"] = Or
    
    df_pl = df_fld.drop_duplicates(subset="Index", keep="first").copy()
    df_kfs = df_fld[~df_fld["wt% SiO2"].isin(df_pl["wt% SiO2"])].copy()
    df_pl["pl mass (gm)"] = df_pl["mass (gm)"]
    df_pl["pl An"] = df_pl["An"]
    df_pl["pl Or"] = df_pl["Or"]
    df_pl = df_pl[pl_outputs]
    df_kfs["kfs mass (gm)"] = df_kfs["mass (gm)"]
    df_kfs["kfs An"] = df_kfs["An"]
    df_kfs["kfs Or"] = df_kfs["Or"]
    df_kfs = df_kfs[kfs_outputs]
    return df_pl, df_kfs

def process_qtz(filepath):
    qtz_outputs = ["T (C)", "P (MPa)", "qtz mass (gm)"]
    df_qtz = pd.read_csv(filepath + "quartz.csv")

    df_qtz["P (MPa)"] = 100 * df_qtz["P (kbars)"]
    df_qtz["qtz mass (gm)"] = df_qtz["mass (gm)"]

    df_qtz = df_qtz[qtz_outputs]
    return df_qtz

def process_ox(filepath):
    ox_outputs = ["T (C)", "P (MPa)", "ox mass (gm)", "ox Usp"]
    df_ox = pd.read_csv(filepath + "spinel.csv")

    df_ox["P (MPa)"] = 100 * df_ox["P (kbars)"]

    TiO2_wt = df_ox["wt% TiO2"]
    Al2O3_wt = df_ox["wt% Al2O3"]
    FeOt_wt = df_ox["wt% FeO"] + 0.9 * df_ox["wt% Fe2O3"]
    MgO_wt = df_ox["wt% MgO"]

    TiO2_mp = TiO2_wt / molecular_weights["TiO2"]
    Al2O3_mp = Al2O3_wt / molecular_weights["Al2O3"]
    FeOt_mp = FeOt_wt / molecular_weights["FeO"]
    MgO_mp = MgO_wt / molecular_weights["MgO"]
    factor = 3/ (TiO2_mp + 2 * Al2O3_mp + FeOt_mp + MgO_mp)

    Ti = factor * TiO2_mp
    Al = factor * 2 * Al2O3_mp
    Fe = factor * FeOt_mp
    Mg = factor * MgO_mp

    # Fe3+
    Fe_ferric = 8 - (Ti * 4 + Al * 3 + (Fe + Mg) * 2)
    # Fe2+
    Fe_ferrous = Fe - Fe_ferric
    X_Fe_ferric = Fe_ferric / (Fe_ferric + Al)
    X_Fe_ferrous = Fe_ferrous / (Fe_ferrous + Mg)
    Usp = 100 * (Ti * X_Fe_ferrous) / (0.5 * Fe_ferric * X_Fe_ferric + Ti * X_Fe_ferrous)

    df_ox["ox Usp"] = Usp
    df_ox["ox mass (gm)"] = df_ox["mass (gm)"]

    df_ox = df_ox[ox_outputs]
    return df_ox

def process_ap(filepath):
    ap_outputs = ["T (C)", "P (MPa)", "ap mass (gm)"]
    df_ap = pd.read_csv(filepath + "apatite.csv")

    df_ap["P (MPa)"] = 100 * df_ap["P (kbars)"]
    df_ap["ap mass (gm)"] = df_ap["mass (gm)"]

    df_ap = df_ap[ap_outputs]
    return df_ap

def merge_results(df, SiO2_wt, H2O_wt, oxbuffer, mode):
    df_filtered = df[(df["SiO2"] == SiO2_wt) & (df["H2O"] == H2O_wt) & (df["log fo2 Path"] == oxbuffer) & (df["Mode"] == mode)]

    indexes = df_filtered["Unnamed: 0"].to_list()

    dirnames = ["input-" + str(i).zfill(8) for i in indexes]

    dfs = []
    for dirname in dirnames:
        filepath = "./out/" + dirname + "/"

        try:
            df_liq = process_liq(filepath)
        except FileNotFoundError:
            continue
        
        try:
            df_ol = process_ol(filepath)
        except FileNotFoundError:
            df_ol = df_liq[["T (C)", "P (MPa)"]].copy()
            df_ol.loc[:, "ol mass (gm)"] = np.nan
            df_ol.loc[:, "ol Fo"] = np.nan
            df_ol.loc[:, "ol wt% CaO"] = np.nan
        
        try:
            df_opx = process_opx(filepath)
        except FileNotFoundError:
            df_opx = df_liq[["T (C)", "P (MPa)"]].copy()
            df_opx.loc[:, "opx mass (gm)"] = np.nan
            df_opx.loc[:, "opx Wo"] = np.nan
            df_opx.loc[:, "opx Mg#"] = np.nan

        try:
            df_aug, df_pig = process_cpx(filepath)
        except FileNotFoundError:
            # augite
            df_aug = df_liq[["T (C)", "P (MPa)"]].copy()
            df_aug.loc[:, "aug mass (gm)"] = np.nan
            df_aug.loc[:, "aug Wo"] = np.nan
            df_aug.loc[:, "aug Mg#"] = np.nan
            # pigeonite
            df_pig = df_liq[["T (C)", "P (MPa)"]].copy()
            df_pig.loc[:, "aug mass (gm)"] = np.nan
            df_pig.loc[:, "aug Wo"] = np.nan
            df_pig.loc[:, "aug Mg#"] = np.nan

        try:
            df_amp = process_amp(filepath)
        except FileNotFoundError:
            df_amp = df_liq[["T (C)", "P (MPa)"]].copy()
            df_amp.loc[:, "amp mass (gm)"] = np.nan

        try:
            df_hbl = process_amp(filepath)
        except FileNotFoundError:
            df_hbl = df_liq[["T (C)", "P (MPa)"]].copy()
            df_hbl.loc[:, "hbl mass (gm)"] = np.nan

        try:
            df_bt = process_amp(filepath)
        except FileNotFoundError:
            df_bt = df_liq[["T (C)", "P (MPa)"]].copy()
            df_bt.loc[:, "bt mass (gm)"] = np.nan

        try:
            df_pl, df_kfs = process_fld(filepath)
        except FileNotFoundError:
            # plagioclase
            df_pl = df_liq[["T (C)", "P (MPa)"]].copy()
            df_pl.loc[:, "pl mass (gm)"] = np.nan
            df_pl.loc[:, "pl An"] = np.nan
            df_pl.loc[:, "pl Or"] = np.nan
            # K-feldspar
            df_kfs = df_liq[["T (C)", "P (MPa)"]].copy()
            df_kfs.loc[:, "kfs mass (gm)"] = np.nan
            df_kfs.loc[:, "kfs An"] = np.nan
            df_kfs.loc[:, "kfs Or"] = np.nan

        try:
            df_qtz = process_amp(filepath)
        except FileNotFoundError:
            df_qtz = df_liq[["T (C)", "P (MPa)"]].copy()
            df_qtz.loc[:, "qtz mass (gm)"] = np.nan

        try:
            df_ox = process_ox(filepath)
        except FileNotFoundError:
            df_ox = df_liq[["T (C)", "P (MPa)"]].copy()
            df_ox.loc[:, "ox mass (gm)"] = np.nan
            df_ox.loc[:, "ox Usp"] = np.nan

        try:
            df_ap = process_amp(filepath)
        except FileNotFoundError:
            df_ap = df_liq[["T (C)", "P (MPa)"]].copy()
            df_ap.loc[:, "ap mass (gm)"] = np.nan

        df = pd.merge(df_liq, df_pl, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_ol, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_opx, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_aug, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_pig, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_amp, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_hbl, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_bt, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_pl, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_kfs, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_qtz, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_ox, how="left", on =["T (C)", "P (MPa)"])
        df = pd.merge(df, df_ap, how="left", on =["T (C)", "P (MPa)"])
        df.insert(0, "Input", dirname)
        dfs.append(df)
        del df
    
    result = pd.concat(dfs)
    result.insert(1, "bulk wt% SiO2", SiO2_wt)
    result.insert(2, "bulk wt% H2O", H2O_wt)
    result.insert(3, "Oxide buffer", oxbuffer)
    result.insert(4, "Mode", mode)
    result.to_csv("summary/summary_" + str(SiO2_wt) + " wt% SiO2_" + str(H2O_wt) + " wt% H2O_" + oxbuffer + ".csv", index = False)

def main():
    # load a config file
    config = json.load(open("config.json", "r"))["processing"]
    inputfile = config["inputfile"]
    l_H2O_wt = config["l_H2O_wt"]
    l_SiO2_wt = config["l_SiO2_wt"]
    l_oxbuffer = config["l_oxbuffer"]
    mode = config["mode"]

    #sys.exit()
    
    df = pd.read_csv(inputfile)
    for SiO2_wt in l_SiO2_wt:
        for oxbuffer in l_oxbuffer:
            for H2O_wt in l_H2O_wt:
                merge_results(df, SiO2_wt, H2O_wt, oxbuffer, mode)

if __name__ == "__main__":
    main()
