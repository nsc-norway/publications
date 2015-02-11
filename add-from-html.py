import sys
import re
import add
import pubdb

htmlfile = open(sys.argv[1]).read()

# Each entry is separated by double line breaks
entries = htmlfile.split("\n\n")

doc_id = []
doi_blacklist = [
  ]
pmid_blacklist = [
  "25613625" # incorrect on website, used doi instead
  ]

# Process a single paragraph of the html, i.e. a publication entry
def process_entry(e):
  # search for PMID:
  pmid_match = re.search(r"pubmed/([\d]+)", e)
  if not pmid_match:
    pmid_match = re.search(r"pubmed/\?term=([\d]+)", e)
  if pmid_match:
    pmid = pmid_match.group(1)
    if pubdb.get_by_pmid(pmid):
      print "Already have PMID", pmid
    elif pmid not in pmid_blacklist:
      add.add_entry(pmid)

  else:
    doi_match = re.search(r"\d\d\.\d\d\d\d/[\da-zA-Z\./\-]*[\da-zA-Z]", e)
    if doi_match: 
      doi = doi_match.group(0)
      if pubdb.get_by_doi(doi):
        print "Already have doi", doi
      elif doi not in doi_blacklist:
        add.add_entry(doi)
    else:
      print "No match at all for:"
      print e
      choice = raw_input("Enter doi, pmid, m to enter manually or enter to skip: ")
      if choice == "m":
        add.add_entry()
      elif choice != "":
        add.add_entry(choice)


# Looping over the HTML file
for i,e in enumerate(reversed(entries)):
  n_i_end = e.count("</i>")
  print "Entry (%d/%d):" % (i+1, len(entries))
  if n_i_end == 0:
    #print "\n\n not a paper? ", e
    pass
  elif n_i_end == 1:
    process_entry(e)
  else:
    print "MULTI-PAPER!!"
    sys.exit(1)

