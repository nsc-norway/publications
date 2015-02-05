# coding=utf-8
import requests
import sys, codecs
from xml.dom import minidom
import sqlite3
import pubdb

# Script to add an entry to the publications database


# US ASCII is useless for printing accented letters. This sets the encoding of the
# terminal output to utf-8.
if sys.stdout.encoding == 'US-ASCII':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


# Main function 
def add_entry(doi = None):

  print ""
  print "Add a publication to the database"
  print ""

  record = get_info(doi)
  print ""

  duplicate = pubdb.check_duplicates(record)
  if duplicate:
    print "Record appears to already exist. Existing record:"
    pubdb.print_record(duplicate)
    print ""
  else:
    pubdb.add(record)
    print ""
    print "Saved."
    print ""




# Data entry routine
def get_info(doi):
  record = {"authors":"", "year":"", "title":"", "journal":"", "doi":"", "pubmed":""} 
  pmid = None

  if not doi:
    doi = raw_input("Enter DOI, or blank for no DOI: ")
  
  if len(doi.strip()) > 0:
    try:
      print "Querying CrossRef..."
      doi_data = get_info_from_doi(doi)
      for k,v in doi_data.items():
        record[k] = v
    except Exception as e:
      print e
      print ""
      abort = raw_input("Abort? [y]")
      if abort == "" or abort == "y":
        sys.exit(1) 
      record['doi'] = doi
  else: # no doi
    pmid = raw_input("Enter PubMed ID, or blank for none: ")
  
  # Look up pubmed info, either with DOI or PMID
  if record['doi'] or pmid: 
    try:
      print "Querying PubMed..."
      data = get_info_from_pubmed(pmid, doi)
      for k,v in data.items():
        record[k] = v
    except Exception as e:
      print e
      print ""
      abort = raw_input("Abort? [y]")
      raise e
      if abort == "" or abort == "y":
        sys.exit(1) 
      record['pubmed'] = pmid
  
  manual = False
  if record['doi'] or record['pubmed']:
    print " ** Retrieved publication data ** "
    print ""
    pubdb.print_record(record)
    print ""

    answer = raw_input("Modify this before adding to database? [n] ")
    if not (answer == "" or answer == "n"):
      manual = True
  
  if manual:
    record = pubdb.modify_record(record)
  
  return record






# XML tree navigation helper functions

# gets a "path" of tags, e.g. 'a','b','c' matches c in <a><b><c></c></b></a>
def get_path_element(base, path):
  elem = base
  for path_component in path:
    found = False
    for child in elem.childNodes:
      if child.nodeType == minidom.Node.ELEMENT_NODE and child.tagName == path_component:
        elem = child
        found = True
    if not found:
      raise Exception("Element " + path_component + " not found in " + str(elem))
  return elem

# Get the text data in an xml tag
def get_path_data(base, path):
  return get_path_element(base, path).firstChild


# Data formatting
def format_author(first, last):
  return str(last) + " " + str(first)[0:1]


# CrossRef DOI lookup functions

def format_crossref_authors(contributors):
  authors = []
  for person_name in contributors.childNodes:
    if person_name.nodeType == minidom.Node.ELEMENT_NODE and person_name.tagName == "person_name":
      first = get_path_data(person_name, ["given_name"])
      last = get_path_data(person_name, ["surname"])
      authors.append(format_author(first, last))

  return u", ".join(authors)
  

# Main function for looking up a DOI
# example https://doi.crossref.org/servlet/query?pid=marius.bjornstad@medisin.uio.no&format=unixsd&id=10.3389/fmicb.2015.00017
def get_info_from_doi(doi):
  params = {"pid": "marius.bjornstad@medisin.uio.no", "format": "unixsd", "id":doi}
  r = requests.get("https://doi.crossref.org/servlet/query", params=params)
  if r.status_code == 200:
    response = r.text
    dom = minidom.parseString(r.text.encode('utf-8'))
    query = dom.getElementsByTagName("query")

    if len(query) == 1:
      q = query[0]
      if q.getAttribute("status") == "resolved":
        data = {}
        journal = get_path_element(q, ["doi_record", "crossref", "journal"])
        article = get_path_element(journal, ["journal_article"])

        data["authors"] = format_crossref_authors(get_path_element(article, ["contributors"]))
        data["year"] =    get_path_data(article, ["publication_date", "year"])
        data["title"] =   get_path_data(article, ["titles", "title"])
        data["journal"] = get_path_data(journal, ["journal_metadata", "abbrev_title"])
        data["doi"] =     get_path_data(article, ["doi_data", "doi"])
        return data
      else: # status != resolved
        raise Exception("Unable to resolve the DOI")

  raise Exception("The CrossRef server returned invalid data or an error status")


# Takes an XML element (Name="AuthorList") as returned by the pubmed (entrez) service
# Returns a comma separated list of authors
def pubmed_authors(authors_list):
  authors = []
  for a in authors_list.getElementsByTagName("Item"):
    if a.getAttribute('Name') == "Author":
      authors.append(a.childNodes[0].data)

  return ", ".join(authors)


# PubMed lookup function
# e.g. http://www.ncbi.nlm.nih.gov/pubmed/?term=20140528&report=xml&format=text
def get_info_from_pubmed(pmid, doi):

  # First get pubmed ID from DOI (skip this if we have pubmed id)
  if not pmid:
    # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=10.1021/bi902153g
    url_doi2pmid = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": doi + "[doi]"}
    r = requests.get(url_doi2pmid, params=params)
    dom = minidom.parseString(r.text.encode('utf-8'))
    pmid = dom.getElementsByTagName("Id")[0].childNodes[0].data

  # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=20235548
  url_pubmed = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
  params = {"db": "pubmed", "id": pmid}
  r = requests.get(url_pubmed, params=params)
  if r.status_code == 200:
    dom = minidom.parseString(r.text.encode('utf-8'))

    data = {}
    doc_sum = dom.getElementsByTagName("DocSum")
    if len(doc_sum) == 1:
      for item in doc_sum[0].childNodes:
        if item.nodeType == minidom.Node.ELEMENT_NODE and item.tagName == "Item":
          name = item.getAttribute("Name")
          cn = item.childNodes
          if name == "AuthorList":
            data['authors'] = pubmed_authors(item)
          elif name == "PubDate":
            # date string example "2010 Apr 13"
            data['year'] = cn[0].data.split(" ")[0]
          elif name == "Title":
            data['title'] = cn[0].data
          elif name == "Source":
            data['journal'] = cn[0].data
          elif name == "DOI":
            data['doi'] = cn[0].data
        elif item.nodeType == minidom.Node.ELEMENT_NODE and item.tagName == "Id":
          data['pubmed'] = item.childNodes[0].data

      return data
    else:
      raise Exception("No data for this Pubmed ID.")
      

  raise Exception("Received status code " + str(r.status_code) + " from server.")


if len(sys.argv) > 1:
  add_entry(sys.argv[1])
else:
  add_entry()

