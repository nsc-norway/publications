# Update script
# Checks for more information on entries which are not marked as complete

import codecs
import sys
import pubdb
import online

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

entries = pubdb.get_not_complete()

for ei in entries:
    rec = {}
    e = dict(ei)
    e['ROWID'] = ei['ROWID']
    if e.get("pubmed"):
        rec = online.get_info_from_pubmed(e['pubmed'])
    elif e.get("doi"):
        rec = online.get_info_from_doi(e['doi'])

    for k, v in rec.items():
        e[k] = v

    # If it is "waiting to complete", set it to complete if we have
    # full journal data
    if e['complete'] == "" and (rec['volume'] or rec['issue'] or rec['pages']):
        e['complete'] = 'y'
    else:
        print "Updated record:"
        pubdb.print_record(e)
        resp = raw_input(
            "Enter new complete status (y/n)? [" + e['complete'] + "] ")
        if resp != "":
            e['complete'] = resp
    pubdb.set(e)
