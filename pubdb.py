import sqlite3
import datetime, locale

# Publication tracking database

# columns and display names
record_name = {
    'authors': 'Authors',
    'title': 'Title', 
    'journal_full': 'Journal full name',
    'journal_abbrev': 'Journal abbrev.',
    'volume': 'Volume',
    'issue': 'Issue number',
    'pages': 'Pages',
    'date': 'Publication date',
    'epubdate': 'Electr. pub. date',
    'year': 'Publication year',
    'doi': 'DOI',
    'pubmed': 'PubMed ID', 
    'source': 'Source'}

# The source field can be pubmed / crossref / manual
# There is also column ROWID which is created by sqlite, which acts as the primary key
record_data = record_name.keys()
columns = ", ".join(record_data)

_conn = False

def blank_record():
  return dict((k,'') for k in record_name)


# Print a publication entry
def print_record(record):
  for ri in record_data:
    rn = record_name[ri]
    print (rn + ":"), " " * (17-len(rn)), record[ri]


# Interactively modify the record data in memory
def modify_record(record):
  new_rec = dict(record)
  try:
    new_rec['ROWID'] = record['ROWID']
  except KeyError:
    pass
  for ri in record_data:
    if ri == 'source': 
      continue # don't modify the source
    rn = record_name[ri]
    if record[ri]:
      rd = unicode(raw_input(rn + " [" + record[ri] + "]: "), 'utf8')
    else:
      rd = unicode(raw_input(rn + ": "), 'utf8')
    if rd != "":
      new_rec[ri] = rd
  return new_rec


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


# Check if this publication is already saved
def check_exists(record):
  conn = open_db()
  c = conn.cursor()
  for r in c.execute('SELECT '+columns+' FROM publications WHERE doi=?', (record['doi'],)):
    return r

  for r in c.execute('SELECT '+columns+' FROM publications WHERE pubmed=?', (record['pubmed'],)):
    return r

  return None


# Add a publication to the database
def add(record):
  conn = open_db()
  c = conn.cursor()
  c.execute("INSERT INTO publications (" + columns + ") VALUES ("\
     + ",".join([":"+col for col in record_data]) + ")", record)
  conn.commit()
  
# Update a record, identified by the ROWID in the supplied dict record
def set(record): 
  conn = open_db()
  c = conn.cursor()
  sql = "UPDATE publications SET "
  values = []
  for col in record_data:
    values.append(record[col]) 
  nval = len(values)
  assign = ", ".join(rec_id + "=?" for rec_id in record_data)
  c.execute("UPDATE publications SET " + assign +\
    " WHERE ROWID=?", tuple(values + [record['ROWID']]))
  conn.commit()
  

# Get publications ordered by year
def get_records():
  conn = open_db()
  c = conn.cursor()
  recs = []
  for row in c.execute("SELECT ROWID," + columns + " FROM publications ORDER BY year DESC"):
    recs.append(row)
  return recs

# Get a record identified by ROWID
def get(row_id):
  conn = open_db()
  c = conn.cursor()
  for row in c.execute("SELECT ROWID," + columns + " FROM publications WHERE ROWID=?", (row_id,)):
    return row
  return None

# Get a record identified by DOI
def get_by_doi(doi):
  conn = open_db()
  c = conn.cursor()
  for row in c.execute("SELECT ROWID," + columns + " FROM publications WHERE doi=?", (doi,)):
    return row
  return None

def remove(pub_id):
  conn = open_db()
  c = conn.cursor()
  c.execute("DELETE FROM publications WHERE ROWID=?", (pub_id,))
  conn.commit()

def parse_us_date(date_string, format):
  locale_tmp = locale.getlocale(locale.LC_TIME)
  locale.setlocale(locale.LC_TIME, 'en_US') 
  print datetime.datetime.strptime(date_string, format)
  locale.setlocale(locale.LC_TIME, locale_tmp) 

