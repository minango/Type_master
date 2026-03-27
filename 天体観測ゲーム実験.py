file_path = "asu (1).tsv"

with open(file_path, encoding="utf-8") as f:
    for i, line in enumerate(f):
        print(i, repr(line))
        if i >= 30:
            break
