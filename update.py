# Update script
# Checks for more information on entries which are not marked as complete

import codecs, sys
import pubdb
import online

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

entries = pubdb.get_not_complete()

for e in entries:
  print e


