import os
import glob

out_dirname = "out"
output_ext = ".tbl"
convert_ext = ".csv"

for out_dir in os.listdir(out_dirname):
    files = sorted(glob.glob(out_dirname + "/" + out_dir + "/*" + output_ext))
    for file in files:
        converted_file = file.replace(output_ext, convert_ext)
        os.rename(file, converted_file)

