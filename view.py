import pubdb, sys, codecs

if sys.stdout.encoding == 'US-ASCII':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def view(publication_id):
  row_id = None
  doi = None
  pmid = None
  try:
    row_id = int(publication_id)
  except:
    if publication_id.startswith("P"):
      pmid = publication_id[1:]
    else:
      doi = publication_id

  if row_id:
    rec = pubdb.get(row_id)
  elif pmid:
    rec = pubdb.get_by_pmid(pmid)
  else:
    rec = pubdb.get_by_doi(doi)

  if rec:
    pubdb.print_record(rec)
  else:
    print "record not found"
    sys.exit(1)

if len(sys.argv[1]) >= 1:
  view(sys.argv[1])
else:
  print "use: view.py {row_id|doi}"
  sys.exit(1)

