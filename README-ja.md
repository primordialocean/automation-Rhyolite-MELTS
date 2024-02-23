# automation-rhyolite-melts

![Static Badge](https://img.shields.io/badge/rhyolite--MELTS-1.2.0-blue?style=flat-square&logo=rhyolite-melts)
![Static Badge](https://img.shields.io/badge/Ubuntu-20.04_LTS-blue?style=flat-square&logo=Ubuntu)
![Static Badge](https://img.shields.io/badge/Python-3.8-blue?style=flat-square&logo=python)
![Static Badge](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

## Overview
`automation-Rhyolite-MELTS`はRhyolite-MELTS (Gualda et al., 2012) を自動化するためのプログラムです。

## Rerequistes
本リポジトリは以下の環境で開発されています。

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

動作には以下のサードパーティ製ライブラリを必要とします：

- `Numpy`
- `Pandas`
- `Matplotlib`
- `pyautogui`

## Installation
- `Melts-rhyolite-public`を[MELTS公式サイト](https://melts.ofm-research.org/unix.html)よりインストールし、プログラムと同じディレクトリ中に保存する。
- `libpng12-0`をインストールする。
```bash
sudo add-apt-repository ppa:linuxuprising/libpng12
sudo apt update
sudo apt install libpng12-0
```
- 実行権限を付与する。
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

## Notes
- 予期せぬ動作によるトラブルを防ぐため、専用のマシンまたは仮想環境（e.g. VMware）上での実行を推奨する。
- プログラムがハングアップした場合は、ターミナル上で`Ctrl+C`を入力する。
- 計算を途中から再開する場合は計算済みの`input-$(number).melts`を`in`ディレクトリから削除または移動し、`auto-melts.py`を実行する。

## References
1. Ghiorso, M., Sack, R., 1995. Chemical mass transfer in magmatic processes IV. A revised and internally consistent thermodynamic model for the interpolation and extrapolation of liquid-solid equilibria in magmatic systems at elevated temperatures and pressures. Contributions to Mineralogy and Petrology, 119, 197-212. https://doi.org/10.1007/BF00307281
1. Gualda, G., Ghiorso, M., Lemons, R., Carley, T., 2012. Rhyolite-MELTS: A modified calibration of MELTS optimized for silica-rich, fluid-bearing magmatic systems. Journal of Petrology, 53, 875-890. https://doi.org/10.1093/petrology/egr080
1. Ghiorso M., Gualda, G., 2015. An H2O-CO2 mixed fluid saturation model compatible with rhyolite-MELTS. Contributions to Mineralogy and Petrology, 165, 53. https://doi.org/10.1007/s00410-015-1141-8

## License
The repository is **not confidential** and available under the [MIT license](https://opensource.org/license/mit/).