import pubdb, sys, codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def ls():
  for record in pubdb.get_records():
    pubdb.print_brief(record)

ls()

