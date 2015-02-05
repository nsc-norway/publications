record_id = ['authors', 'year', 'title', 'journal', 'doi', 'pubmed']
record_name = {
    'authors': 'Authors', 'year':'Year', 'title':'Title', 
    'journal': 'Journal', 'doi': 'DOI', 'pubmed': 'PubMed ID'}


def print_record(record):
  for ri in record_id:
    rn = record_name[ri]
    print (rn + ":"), " " * (12-len(rn)), record[ri]


def modify_record(record):
  for ri in record_id:
    rn = record_name[ri]
    if record[ri]:
      rd = raw_input(rn + " [" + record[ri] + "]: ")
    else:
      rd = raw_input(rn + ": ")
    if rd != "":
      record[ri] = rd
  return record


def open_db():
  pass


def check_duplicates():
  return None


def add():
  pass

