import pubdb
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def mark_complete_incomplete():
    for record in pubdb.get_records():
        old_complete = record['complete'] == "y"
        complete = record['doi'] and record['pubmed']
        if complete != old_complete:
            new_record = dict(record)
            new_record['ROWID'] = record['ROWID']
            new_record['complete'] = 'y' if complete else 'n'
            pubdb.set(new_record)

mark_complete_incomplete()
