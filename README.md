# automation-Rhyolite-MELTS

![Static Badge](https://img.shields.io/badge/Rhyolite--MELTS--2.0-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Ubuntu-20.04_LTS-blue?style=flat-square&logo=Ubuntu)
![Static Badge](https://img.shields.io/badge/Python-3.8-blue?style=flat-square&logo=python)
![Static Badge](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Earth_science-Volcanology-blue?style=flat-square)

[日本語版README](README-ja.md)

## Overview
`automation-Rhyolite-MELTS` is a repository for automation of Rhyolite-MELTS (Gualda et al., 2012) calculation.

## Rerequistes
This repository has been developed under following enviornments:
- Ubuntu 20.04 LTS on VMware 17.5.0
- Python 3.8.10

Only the environments listed above have been confirmed to work.

Here is a list of softwares that are required to run this program:
- `scrot`
- `python3-tk`
- `python3-dev`
- `libpng12-0`

The repository relies on the following third-party libraries:
- `numpy` carries out numerical calculations.
- `pandas` loads input files.
- `matplotlib` visualises the calculation results.
- `opencv-python`
- `pyautogui`

## Installation
- Rhyolite-MELTS (`Melts-rhyolite-public`) can be downloadable at the [developer's website](https://melts.ofm-research.org/unix.html). The downloaded file should be saved in the `automation-rhyolite-melts` directory.

- (Optional) create virtual environment.
```bash
python -m venv ${the name of a new virtual environment}
```
- Installation of `libpng12-0` requires additional repository.
```bash
sudo add-apt-repository ppa:linuxuprising/libpng12
sudo apt update
sudo apt install libpng12-0
```

- Install third-party python libraries.
```bash
pip install --user ${the name of third-party libraries}
```

- Grant execute permission to Melts-rhyolite-public.
```bash
sudo chmod +x Melts-rhyolite-public
```

- Test operation of `Melts-rhyolite-public`.
```bash
./Melts-rhyolite-public

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
rhyolite-MELTS (-0.2, --0, -2.0) pMELTS (5.6.1) - (Jul 31 2015 - 14:52:41)
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
---> Reading environment variables...
<><> There are three releases of rhyolite-MELTS and a version of pMELTS included in this package:
     (*) rhyolite-MELTS v. -0.2 (original version, with corrections) - old H2O model, no mixed fluids.
     (*) rhyolite-MELTS v, --0 (mixed fluid version that perserves the ternary minimum) - old H2O model.
     (*) rhyolite-MELTS v. -2.0 (mixed fluid version optimal for mafic and alkalic melts) - new H2O model.
     (*) pMELTS v. 5.6.1 (original version, with corrections) - - old H2O model, no mixed fluids.
<><> Visit the website melts.ofm-research.org for information on which version to use for your application.
---> Default calculation mode is rhyolite-MELTS (v. -0.2).  Change this? (y or n): y
     Set calculation mode to rhyolite-MELTS (public release v --0)? (y or n): n
     Set calculation mode to rhyolite-MELTS (public release v -2.0)? (y or n): y
---> ************************************************************
---> Calculation mode is rhyolite-MELTS (public release v -2.0).
---> ************************************************************
---> Initializing data structures using selected calculation mode...
---> Building interface...
---> ...Call to initialize_colors ()...
---> ...Call to initialize_strings ()...
---> ...Create main window...
---> ...Create menu bar...
---> ...Create work window...
---> ...Call to create_managed ()...
---> ...Call to create_unmanaged ()...
---> ...Manage children...
---> ...Manage parent...
---> ...Realize parent...
---> Ready for user input...
```

## Usage
`python ${filename}.py` or `python3 ${filename}.py` command are used to run `.py` programs.

- Input the values of starting composition and run condition (e.g. pressure, temperature, fO2 buffer) into `start.csv`.
- Configure `config.json`.
- Check that the `in` and `out` directories are empty.
- Run `gen_melts.py` to generate `input-$(number).melts` and `input.csv` files.
- Run `auto_melts.py`.
- Run `convert_results.py` to convert `.tbl` files to `.csv`.
- Run `processing.py` to export summary files of calculation results in the `summary` directry.
- Run `plot_liquidus.py` to plot liquidus lines. (under development)

## About `start.csv`
- `Sample`: Input sample name or number.
- `SiO2`, `TiO2`, `Al2O3`, `Fe2O3`, `FeO`, `MnO`, `MgO`, `CaO`, `Na2O`, `K2O`, `P2O5`, `H2O`: Input starting composition as wt%. The starting composition is automatically normalised as 100 wt%.
- `Initial Temperature (C)`, `Final Temperature (C)`, `Increment Temperature (C)`: Input initial/final temperature and intervals as degree Celsius.
- `Initial Pressure (MPa)`, `Final Pressure (MPa)`, `Increment Pressure (MPa)`: Input initial/final pressure and intervals as MPa.
- `dp/dt`: Slope of pressure vs temperature as bar/K.
- `log fo2 Path`: Set fO2 buffer from `MH`, `NNO`, `FMQ`, `WM` and `IW`, or dFMQ style (e.g. `+1FMQ`). The settable range of dFMQ is from `-9FMQ` to `+3FMQ`.
- `Mode`: Select from `Equilibrium` (equilibrium crystallisation) or `Fractionate Solids` (fractional crystallisation).

## About `config.json`
- `"gen_melts"`: Setting of `"gen_melts.py"`
  - `"Normalise with H2O"`: Select whether to include H2O content (`true` or `false`) when normalising to 100 wt%.

- `"processing"`: Setting of `"processing.py"`
  - `"l_SiO2_wt"`, `"l_H2O_wt"`, `"l_oxbuffer"`: Set starting content of SiO2, H2O, and fO2 buffer as list.
  - `"Mode"`: Select from `Equilibrium` (equilibrium crystallisation) or `Fractionate Solids` (fractional crystallisation).

- `"plot_liquidus"`: Setting of `"plot_liquidus.py"`
  - `"plot_phase"`: Select the mineral phase to be plotted as `true` and the phase not to be plotted as `false`.
  - `p1_xlim`: Set a range of x-axis of P-T-X plot as `[min, max]`.
  - `p1_ylim`: Set a range of y-axis of P-T_X plot as `[min, max]`.
  - `p2_xlim`: Set a range of x-axis of P-Σresidual plot as `[min, max]`.

## Notes
- This program is recommended to run on virtual machines (e.g. VMware) to prevent unexpected malfunction.
- If the program hang-up during running, type the command of `Ctrl+C` into the bash window.
- If you want to resume calculation, delete the calculated `input-${number}.melts` and run `auto_melts.py`.

## References
- Ghiorso, M., Sack, R., 1995. Chemical mass transfer in magmatic processes IV. A revised and internally consistent thermodynamic model for the interpolation and extrapolation of liquid-solid equilibria in magmatic systems at elevated temperatures and pressures. Contributions to Mineralogy and Petrology, 119, 197-212. https://doi.org/10.1007/BF00307281
- Gualda, G., Ghiorso, M., Lemons, R., Carley, T., 2012. Rhyolite-MELTS: A modified calibration of MELTS optimized for silica-rich, fluid-bearing magmatic systems. Journal of Petrology, 53, 875-890. https://doi.org/10.1093/petrology/egr080
- Ghiorso M., Gualda, G., 2015. An H2O-CO2 mixed fluid saturation model compatible with rhyolite-MELTS. Contributions to Mineralogy and Petrology, 165, 53. https://doi.org/10.1007/s00410-015-1141-8

## License
The repository is **not confidential** and available under the [MIT license](https://opensource.org/license/mit/).