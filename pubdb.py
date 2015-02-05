import sqlite3


record_data = ['authors', 'year', 'title', 'journal', 'doi', 'pubmed', 'source']
columns = ", ".join(record_data)
record_name = {
    'authors': 'Authors', 'year':'Year', 'title':'Title', 
    'journal': 'Journal', 'doi': 'DOI', 'pubmed': 'PubMed ID', 
    'source': 'Source'}

# source can be pubmed / crossref / manual

_conn = False

# Print a publication entry
def print_record(record):
  for ri in record_data:
    rn = record_name[ri]
    print (rn + ":"), " " * (12-len(rn)), record[ri]


# Interactively modify the record data in memory
def modify_record(record):
  for ri in record_data:
    if ri == 'source': 
      continue # don't modify the source
    rn = record_name[ri]
    if record[ri]:
      rd = raw_input(rn + " [" + record[ri] + "]: ")
    else:
      rd = raw_input(rn + ": ")
    if rd != "":
      record[ri] = rd
  return record


# Open a connection to the database or use an existing one
def open_db():
  global _conn

  if _conn:
    return _conn

  _conn = sqlite3.connect("publications.db")
  _conn.row_factory = sqlite3.Row
  c = _conn.cursor()
  for row in c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="publications"'):
    return _conn
  
  # Does not exist
  create_columns = ", ".join([ri + " TEXT" for ri in record_data])
  c.execute("CREATE TABLE publications(" + create_columns + ")") 

  return _conn


def check_duplicates(record):
  conn = open_db()
  c = conn.cursor()
  for r in c.execute('SELECT '+columns+' FROM publications WHERE doi=?', (record['doi'],)):
    return r

  for r in c.execute('SELECT '+columns+' FROM publications WHERE pubmed=?', (record['pubmed'],)):
    return r

  return None


def add(record):
  conn = open_db()
  c = conn.cursor()
  c.execute("INSERT INTO publications (" + columns + ") VALUES ("\
     + ",".join([":"+col for col in record_data]) + ")", record)
  conn.commit()
  

def get_records():
  conn = open_db()
  c = conn.cursor()
  recs = []
  for row in c.execute("SELECT ROWID," + columns + " FROM publications ORDER BY year DESC"):
    recs.append(row)

  return recs

def get(row_id):
  conn = open_db()
  c = conn.cursor()
  for row in c.execute("SELECT ROWID," + columns + " FROM publications WHERE ROWID=?", (row_id,)):
    return row

  return None


def get_by_doi(doi):
  conn = open_db()
  c = conn.cursor()
  for row in c.execute("SELECT ROWID," + columns + " FROM publications WHERE doi=?", (doi,)):
    return row

  return None

