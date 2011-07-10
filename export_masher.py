import sys
import os

script, safety = sys.argv
if safety:
    path = "a:/economy"
    csv_files = []
    for _,_,files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(file)

    csv_text = ""
    for csv in csv_files:
        file_path = "%s/%s" % (path, csv)
        with open(file_path) as f:
            csv_text += "".join(f.readlines()[1:])

    with open("a:/large.csv", "w+") as f:
        f.write(csv_text)


