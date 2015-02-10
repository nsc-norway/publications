import pubdb, sys, codecs

if sys.stdout.encoding == 'US-ASCII':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def ls():
  for record in pubdb.get_records():
    author = record['authors'].split(',')[0]
    print "%4d %s %-20s %-20s %s" % (record['ROWID'], record['year'], author, record['journal_abbrev'], record['doi'])

ls()

