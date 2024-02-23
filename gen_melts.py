import pandas as pd
from itertools import product
import json

def gen_meltsfile(inputs):
    elements = [
        "SiO2", "TiO2", "Al2O3", "FeO", "MnO", "MgO",
        "CaO", "Na2O", "K2O", "P2O5", "H2O"
        ]

    for i in range(len(inputs)):
        # zfillで0埋め．桁数は任意のものを．
        with open("in/input-"+str(i).zfill(8)+".melts", "w") as f:
            f.write("Title: "+str(i)+"\n")
            for element in elements:
                f.write("Initial Composition: " + element + " " \
                        + str(inputs[element][i]) + "\n")
            f.write("Initial Temperature: " \
                    + str(inputs["Initial Temperature (C)"][i]) + "\n")
            f.write("Final Temperature: " \
                    + str(inputs["Final Temperature (C)"][i]) + "\n")
            f.write("Initial Pressure: " \
                    + str(10 * inputs["Initial Pressure (MPa)"][i]) + "\n")
            f.write("Final Pressure: " \
                    + str(10 * inputs["Final Pressure (MPa)"][i]) + "\n")
            f.write("Increment Temperature: " \
                    + str(inputs["Increment Temperature (C)"][i]) + "\n")
            f.write("Increment Pressure: " \
                    + str(10 * inputs["Increment Pressure (MPa)"][i]) + "\n")
            f.write("dp/dt: " + str(inputs["dp/dt"][i]) + "\n")
            f.write("log fo2 Path: " \
                    + str(inputs["log fo2 Path"][i]) + "\n")
            if inputs["Mode"][i] != "Equilibrium":
                f.write("Mode: " + inputs["Mode"][i])
            f.close()


def main():
    # load config.json
    with open("config.json") as f:
        config = json.load(f)
    
    active_normalisation = config["Normalise with H2O"]
    
    df = pd.read_csv("start.csv")
    elements = [
        "SiO2", "TiO2", "Al2O3", "FeO", "MnO", "MgO",
        "CaO", "Na2O", "K2O", "P2O5",
        ]
    bulk = df[elements].dropna()
    h2o = df[["H2O"]].dropna()
    tempc = df[
            [
            "Initial Temperature (C)", "Final Temperature (C)",
            "Increment Temperature (C)"
            ]
        ].dropna()
    pressmpa = df[
            [
            "Initial Pressure (MPa)", "Final Pressure (MPa)",
            "Increment Pressure (MPa)"
            ]
        ].dropna()
    dpdt = df[["dp/dt"]].dropna()
    oxbuffer = df[["log fo2 Path"]].dropna()
    mode = df[["Mode"]].dropna()

    def convert_tuple(df):
        df_tuple = [tuple(x) for x in df.values]
        return df_tuple
    
    h2o = convert_tuple(h2o)
    tempc = convert_tuple(tempc)
    pressmpa = convert_tuple(pressmpa)
    dpdt = convert_tuple(dpdt)
    oxbuffer = convert_tuple(oxbuffer)
    mode = convert_tuple(mode)

    params = pd.DataFrame(
        list(product(mode, oxbuffer, h2o, dpdt, pressmpa, tempc))
        )
    
    params = params[params.columns[::-1]]
    params = pd.concat(
        [params[x].apply(pd.Series) for x in params.columns], axis=1
        )
    params = params.set_axis(
            [
            "Initial Temperature (C)", "Final Temperature (C)",
            "Increment Temperature (C)", "Initial Pressure (MPa)",
            "Final Pressure (MPa)", "Increment Pressure (MPa)", "dp/dt",
            "H2O", "log fo2 Path", "Mode"
            ], axis = 1
        )
    df1 = bulk.loc[bulk.index.repeat(len(params))].reset_index(drop=True)
    df2 = pd.concat([params] * len(bulk), axis=0).reset_index(drop=True)
    inputs = pd.concat([df1, df2], axis=1)

    # normalised starting composition to 100 wt% including H2O content
    if active_normalisation == True:
        coef = (100 - inputs["H2O"]) / inputs[elements].sum(axis=1)
        inputs[elements] = inputs[elements].apply(lambda x: x * coef, axis=0)
    else:
        pass
    
    # export starting condition to input.csv
    inputs.to_csv("input.csv")

    # export melts file
    gen_meltsfile(inputs)

if __name__ == "__main__":
    main()
