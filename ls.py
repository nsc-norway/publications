import pubdb
import sys
import codecs

sys.stdout.reconfigure(encoding='utf-8')

def ls():
    for record in pubdb.get_records():
        pubdb.print_brief(record)

ls()
