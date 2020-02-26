import pubdb
import sys
import codecs

sys.stdout.reconfigure(encoding='utf-8')

def rm(pub_id):
    record = pubdb.get(pub_id)
    author = record['authors'].split(',')[0]
    print("%4d %s %-20s %-20s %s" % (record['ROWID'], record['year'], author, record['journal_abbrev'], record['doi']))
    ans = input("Delete? [Y/n] ")
    if ans.lower() == "y" or ans == "":
        pubdb.remove(pub_id)
        print("\nRemoved.\n")


if len(sys.argv) > 1:
    rm(sys.argv[1])
else:
    print("use: rm <row-id>")
