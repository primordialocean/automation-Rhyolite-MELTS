# automation-Rhyolite-MELTS

![Static Badge](https://img.shields.io/badge/Rhyolite--MELTS-1.2.0-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Ubuntu-20.04_LTS-blue?style=flat-square&logo=Ubuntu)
![Static Badge](https://img.shields.io/badge/Python-3.8-blue?style=flat-square&logo=python)
![Static Badge](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Earth_science-Volcanology-blue?style=flat-square)

## Rerequistes
This repository has been developed under following enviornments:
- Ubuntu 20.04 LTS on VMware 17.5.0
- Python 3.8.10

Only the environments listed above have been confirmed to work.

To use this repositiory, the latest version of rhyolite-MELTS (`Melts-rhyolite-public`) is required. Rhyolite-MELTS can be downloadable at [developer's website](https://melts.ofm-research.org/unix.html). The downloaded file should be saved in the `automation-rhyolite-melts` directory.

The repository relies on the following third-party libraries:
- `Numpy`: carrying out numerical calculations
- `Pandas`: loading input files
- `Matplotlib`: visualisation of the calculation results

The easiest way to install third-party libraries is by running `pip install --user $(library_name)`.

```
automation-rhyolite-melts/
  ├ in/
  │  ├ input-0001.melts
  │  ├ ...
  │  └ input-9999.melts
  ├ out/
  │  ├ input-0001/
  │  │  ├ melts-liquid.csv
  │  │  ├ ...
  │  │  └ olivine.csv
  │  ├ ...
  │  └ input-9999/
  ├ summary/
  │  ├ summary-0001.csv
  │  ├ ...
  │  └ summary-****.csv
  ├ Melts-rhyolite-public
  └ auto-melts.py
```

## Usage
1. confirm that the `in` and `out` directories are empty.
1. run `gen_melts.py` to generate `input-$(number).melts` and `input.csv` files.
1. run `auto-melts.py`.
1. run `convert_results.py` and `processing.py` to generate result files in the `summary` directry.
1. run `search_liquidus.py` to plot liquidus lines.

## Notes
- This program is recommended to run on virtual machines (e.g. VMware) to prevent unexpected malfunction.
- If the program hang-up during running, type the command of `Ctrl+C` into the bash window.
- If you want to resume calculation, delete the calculated `input-$(number).melts` and run `auto-melts.py`.

## License
The repository is **not confidential** and available under the [MIT license](https://opensource.org/license/mit/).