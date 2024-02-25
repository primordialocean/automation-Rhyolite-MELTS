# automation-Rhyolite-MELTS

![Static Badge](https://img.shields.io/badge/rhyolite--MELTS-1.2.0-blue?style=flat-square&logo=rhyolite-melts)
![Static Badge](https://img.shields.io/badge/Ubuntu-20.04_LTS-blue?style=flat-square&logo=Ubuntu)
![Static Badge](https://img.shields.io/badge/Python-3.8-blue?style=flat-square&logo=python)
![Static Badge](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

[English README](README.md)

## Overview
`automation-Rhyolite-MELTS`はRhyolite-MELTS (Gualda et al., 2012) を自動化するためのプログラムである。

## Rerequistes
本リポジトリは以下の環境で開発された。

- Ubuntu 20.04 LTS on VMware 17.5.0
- Python 3.8.10

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

事前に以下のソフトウェアが必要となる：
- `scrot`
- `python3-tk`
- `python3-dev`
- `libpng12-0`

以下のサードパーティ製Pythonライブラリを必要とする：
- `numpy`
- `pandas`
- `matplotlib`
- `opencv-python`
- `pyautogui`

## Installation
- `Melts-rhyolite-public`を[MELTS公式サイト](https://melts.ofm-research.org/unix.html)よりインストールし、`automation-Rhyolite-MELTS`直下のディレクトリ中に保存する。
- 必要なソフトウェアをインストールする。
```bash
sudo apt install ${software name}
```
- `libpng12-0`のインストールにはリポジトリの追加が必要となる。以下の方法でリポジトリを追加する。
```bash
sudo add-apt-repository ppa:linuxuprising/libpng12
sudo apt update
sudo apt install libpng12-0
```

- (Optional: 仮想環境中にライブラリをインストールする場合) 仮想環境を作成する。
```bash
python -m venv ${the name of a new virtual environment}
```

- ライブラリをインストールする。
```bash
pip install --user ${the name of third-party libraries}
```

- `Melts-rhyolite-public`に実行権限を付与する。
```bash
sudo chmod +x Melts-rhyolite-public
```

- 通常の方法で`Melts-rhyolite-public`が起動できるか確認する。
```bash
./Melts-rhyolite-public

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
rhyolite-MELTS (1.0.2, 1.1.0, 1.2.0) pMELTS (5.6.1) - (Jul 31 2015 - 14:52:41)
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
---> Reading environment variables...
<><> There are three releases of rhyolite-MELTS and a version of pMELTS included in this package:
     (*) rhyolite-MELTS v. 1.0.2 (original version, with corrections) - old H2O model, no mixed fluids.
     (*) rhyolite-MELTS v, 1.1.0 (mixed fluid version that perserves the ternary minimum) - old H2O model.
     (*) rhyolite-MELTS v. 1.2.0 (mixed fluid version optimal for mafic and alkalic melts) - new H2O model.
     (*) pMELTS v. 5.6.1 (original version, with corrections) - - old H2O model, no mixed fluids.
<><> Visit the website melts.ofm-research.org for information on which version to use for your application.
---> Default calculation mode is rhyolite-MELTS (v. 1.0.2).  Change this? (y or n): y
     Set calculation mode to rhyolite-MELTS (public release v 1.1.0)? (y or n): n
     Set calculation mode to rhyolite-MELTS (public release v 1.2.0)? (y or n): y
---> ************************************************************
---> Calculation mode is rhyolite-MELTS (public release v 1.2.0).
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

`.py`ファイルを実行するには`python ${filename}.py`または`python3 ${filename}.py`コマンドを用いる。

- `start.csv`ファイルに出発組成・温度・圧力・温度or圧力ステップ・酸素バッファを入力する。
- `config.json`を設定する。
- `in`および`out`ディレクトリが空であることを確認する。
- `gen_melts.py`を実行し、入力に用いる`input-${number}.melts`および`input.csv`を生成する。`input-${number}.melts`は手動で`Melts-rhyolite-public`を実行する際に使用することもできる。
- `auto_melts.py`を実行する。
- `convert_results.py`を実行し、`out`ディレクトリ中の`.tbl`ファイルを`.csv`ファイルに変換する。
- `processing.py`を実行し、`summary`ディレクトリに計算結果を出力する。
- (Optional: P-T-X図をプロットする場合) `plot_ptx.py`を実行する。※動作未確認
- (Optional: リキダス相図をプロットする場合) `plot_liquidus.py`を実行する。※動作未確認

## About `start.csv`
- `Sample`: サンプル名を入力する。
- `SiO2`, `TiO2`, `Al2O3`, `Fe2O3`, `FeO`, `MnO`, `MgO`, `CaO`, `Na2O`, `K2O`, `P2O5`, `H2O`: 出発物質組成をwt%で入力する。出発組成は自動で100 wt%に規格化されるため生データと規格化済みデータのどちらでも入力可能。
- `Initial Temperature (C)`, `Final Temperature (C)`, `Increment Temperature (C)`: 計算開始・終了温度、温度ステップを摂氏温度で入力する。
- `Initial Pressure (MPa)`, `Final Pressure (MPa)`, `Increment Pressure (MPa)`: 計算開始・終了圧力、圧力ステップをMPaで入力する。
- `dp/dt`: 温度と圧力を同時に変化させる場合の設定項目だが、現在未対応のため`0`に設定する。
- `log fo2 Path`: `MH`, `NNO`, `FMQ`, `WM`, `IW`のいずれかまたはdFMQの形式（e.g. `+1FMQ`）で設定する。dFMQは`-9FMQ`から`+3FMQ`の範囲で設定できる。
- `Mode`: `Equilibrium`（平衡結晶作用）と`Fractionate Solids`（分別結晶作用）から選択する。

## About `config.json`
- `"gen_melts"`: `"gen_melts.py"`の設定を含む
  - `"Normalise with H2O"`: 出発組成を合計100 wt%に規格化する際、H2Oを含めるかどうかを選択する。H2Oを含めて規格化する場合は`true`を、含めない場合は`false`を選ぶ。

- `"processing"`: `"processing.py"`の設定を含む
  - `"l_sample"`, `"l_H2O_wt"`, `"l_oxbuffer"`: 出発組成のサンプル番号、H2O、fO2 bufferのうち、summaryに出力する値をリスト形式で設定する。
  - `"Mode"`: 設定した計算モードのうち、`Equilibrium`（平衡結晶作用）と`Fractionate Solids`（分別結晶作用）からsummaryに出力するものを設定する。

- `"plot_liquidus"`: `"plot_liquidus.py"`の設定を含む
  - `"plot_phase"`: プロットする相を`true`、プロットしない相を`false`で選択する。
  - `p1_xlim`: P-T-X図のx軸（温度範囲）を`[min, max]`の形式で設定する。
  - `p1_ylim`: P-T_X図およびP-Σresidual図のy軸（圧力範囲）を`[min, max]`の形式で設定する。
  - `p2_xlim`: P-Σresidual図のx軸（残差平方和範囲）を`[min, max]`の形式で設定する。

## Notes
- 予期せぬ動作によるトラブルを防ぐため、専用のマシンまたは仮想環境（e.g. VMware）上での実行を推奨する。
- プログラムがハングアップした場合は、ターミナル上で`Ctrl+C`を入力する。
- 計算を途中から再開する場合は計算済みの`input-${number}.melts`を`in`ディレクトリから削除または移動し、`auto_melts.py`を実行する。

## References
- Ghiorso, M., Sack, R., 1995. Chemical mass transfer in magmatic processes IV. A revised and internally consistent thermodynamic model for the interpolation and extrapolation of liquid-solid equilibria in magmatic systems at elevated temperatures and pressures. Contributions to Mineralogy and Petrology, 119, 197-212. https://doi.org/10.1007/BF00307281
- Gualda, G., Ghiorso, M., Lemons, R., Carley, T., 2012. Rhyolite-MELTS: A modified calibration of MELTS optimized for silica-rich, fluid-bearing magmatic systems. Journal of Petrology, 53, 875-890. https://doi.org/10.1093/petrology/egr080
- Ghiorso M., Gualda, G., 2015. An H2O-CO2 mixed fluid saturation model compatible with rhyolite-MELTS. Contributions to Mineralogy and Petrology, 165, 53. https://doi.org/10.1007/s00410-015-1141-8

## License
本リポジトリは[MIT license](https://opensource.org/license/mit/)において公開される。