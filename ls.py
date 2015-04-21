import pubdb
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def ls():
    for record in pubdb.get_records():
        pubdb.print_brief(record)

ls()
