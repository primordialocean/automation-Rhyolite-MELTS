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
- `Melts-rhyolite-public`を[MELTS公式サイト](https://melts.ofm-research.org/unix.html)よりインストールし、プログラムと同じディレクトリ中に保存する。
- 必要なソフトウェアをインストールする。
```bash
sudo apt install ${software name}
```
- `libpng12-0`はリポジトリの追加が必要となる。以下の方法でリポジトリを追加する。
```bash
sudo add-apt-repository ppa:linuxuprising/libpng12
sudo apt update
sudo apt install libpng12-0
```
- `Melts-rhyolite-public`に実行権限を付与する。
```bash
sudo chmod +x Melts-rhyolite-public
```
- (Optional: 仮想環境中にライブラリをインストールする場合) 仮想環境を作成する。
```bash
python -m venv ${the name of a new virtual environment}
```

- ライブラリをインストールする。
```bash
pip install --user ${the name of third-party libraries}
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
- (Optional: P-T-X図をプロットする場合) `plot_ptx.py`を実行する。
- (Optional: リキダス相図をプロットする場合) `search_liquidus.py`を実行する。

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

- `"plot_liquidus"`: `"plot_liquidus.py"`の設定を含む
  - `"plot_phase"`: プロットする相を`true`、プロットしない相を`false`で選択する。
  - `p1_xlim`: P-T-X図のx軸（温度範囲）を`[min, max]`の形式で設定する。
  - `p1_ylim`: P-T_X図およびP-Σresidual図のy軸（圧力範囲）を`[min, max]`の形式で設定する。
  - `p2_xlim`: P-Σresidual図のx軸（残差平方和範囲）を`[min, max]`の形式で設定する。

## Notes
- 予期せぬ動作によるトラブルを防ぐため、専用のマシンまたは仮想環境（e.g. VMware）上での実行を推奨する。
- プログラムがハングアップした場合は、ターミナル上で`Ctrl+C`を入力する。
- 計算を途中から再開する場合は計算済みの`input-$(number).melts`を`in`ディレクトリから削除または移動し、`auto_melts.py`を実行する。

## References
- Ghiorso, M., Sack, R., 1995. Chemical mass transfer in magmatic processes IV. A revised and internally consistent thermodynamic model for the interpolation and extrapolation of liquid-solid equilibria in magmatic systems at elevated temperatures and pressures. Contributions to Mineralogy and Petrology, 119, 197-212. https://doi.org/10.1007/BF00307281
- Gualda, G., Ghiorso, M., Lemons, R., Carley, T., 2012. Rhyolite-MELTS: A modified calibration of MELTS optimized for silica-rich, fluid-bearing magmatic systems. Journal of Petrology, 53, 875-890. https://doi.org/10.1093/petrology/egr080
- Ghiorso M., Gualda, G., 2015. An H2O-CO2 mixed fluid saturation model compatible with rhyolite-MELTS. Contributions to Mineralogy and Petrology, 165, 53. https://doi.org/10.1007/s00410-015-1141-8

## License
本リポジトリは[MIT license](https://opensource.org/license/mit/)において公開される。