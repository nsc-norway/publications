# coding=utf-8
import sys
import codecs
import locale
import pubdb
import online
import re

# Script to add an entry to the publications database


# Set output encoding to allow international characters
sys.stdout.reconfigure(encoding='utf-8')


# Main function
def add_entry(doc_id=None):

    print("")
    print("Add a publication to the database")
    print("")

    if not doc_id:
        doc_id = input("Enter DOI or PubMed ID, or blank to skip: ")

    record = get_info(doc_id)
    print("")

    duplicate = pubdb.check_exists(record)
    if duplicate:
        print("")
        print("ABORTED. Specified publication is already in database. Existing record:")
        pubdb.print_record(duplicate)
        print("")
    else:
        pubdb.add(record)
        print("")
        print("Saved.")
        print("")


# Main data retrieval routine
def get_info(doc_id):
    record = pubdb.blank_record()
    manual = True
    if doc_id != "":
        doi = None
        try:
            pmid = str(int(doc_id))  # if numeric, assume PMID
        except ValueError:
            doi = re.sub(r"^https?://doi.org/", "", doc_id)  # otherwise, it's a DOI

        if doi:
            try:
                pmid = online.doi_to_pmid(doi)
            except:
                print("PubMed doesn't know about this DOI.")
                pmid = None

        if pmid:
            print("Getting info from PubMed...")
            data = online.get_info_from_pubmed(pmid)
            if not doi or ('doi' in data and data['doi'].upper() == doi.upper()):
                record['source'] = "pubmed"
            else:  # This happens :o
                print("DOI in pubmed doesn't match the one provided, reverting to crossref")
                record = pubdb.blank_record()
                pmid = None
        if not pmid:
            print("Getting info from CrossRef...")
            data = online.get_info_from_doi(doi)
            record['source'] = "crossref"

        for k, v in data.items():
            record[k] = v

        if record['source'] != '':
            print(" ** Retrieved publication data ** ")
            print("")
            pubdb.print_record(record)
            print("")
            duplicate = pubdb.check_exists(record)
            if duplicate:
                print("\n\nDUPLICATE: This already exists:")
                pubdb.print_record(duplicate)
                print("\n\n--You may still continue, but need to modify the new entry's pubmed/doi or it will be rejected")
                answer = input("Modify/cancel [m/c] ").lower()
            else:
                print("Select i to save as is, but mark as incomplete")
                answer = input("Add/modify/cancel/incomplete [A/m/c/i] ").lower()

            if (answer == "" or answer == "a"):
                manual = False
                record['complete'] = 'y'
            elif answer == "i":
                manual = False
                record['complete'] = ''
            elif answer == "m":
                manual = True
            else:
                print("\nCancelled.\n")
                sys.exit(1)

    if manual:
        record = pubdb.modify_record(record)
        record['source'] = 'manual'

    return record


if __name__ == '__main__':
    if len(sys.argv) > 1:
        add_entry(sys.argv[1])
    else:
        add_entry()
