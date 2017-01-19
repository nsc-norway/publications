import pubdb
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def modify(publication_id):
    row_id = None
    doi = None
    try:
        row_id = int(publication_id)
    except:
        doi = publication_id

    if row_id:
        rec = pubdb.get(row_id)
    else:
        rec = pubdb.get_by_doi(doi)

    if rec:
        new_rec = pubdb.modify_record(rec)
        new_rec['source'] = 'manual'
        pubdb.set(new_rec)
        print "\nUpdated.\n"
    else:
        print "\nrecord not found\n"
        sys.exit(1)


if len(sys.argv[1]) >= 1:
    modify(sys.argv[1])
else:
    print "use: modify.py {row_id|doi}"
    sys.exit(1)
