import add
import sys

data_input = open(sys.argv[1]).readlines()
doi_list = [d.rstrip("\n") for d in data_input]

for doi in doi_list:
    add.add_entry(doi)
