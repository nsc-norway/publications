import requests
import sys
from xml.dom import minidom
import sqlite3
doi_list = ["10.3389/fmicb.2015.00017"]



response = """<?xml version="1.0" encoding="UTF-8"?>
<crossref_result xmlns="http://www.crossref.org/qrschema/3.0" version="3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.crossref.org/qrschema/3.0 http://www.crossref.org/schema/queryResultSchema/crossref_query_output3.0.xsd">
  <query_result>
    <head>
      <doi_batch_id>none</doi_batch_id>
    </head>
    <body>
      <query status="resolved">
        <doi type="journal_article">10.2174/1874285801408010148</doi>
        <crm-item name="publisher-name" type="string">Bentham Science Publishers Ltd.</crm-item>
        <crm-item name="prefix-name" type="string">Bentham Science</crm-item>
        <crm-item name="member-id" type="number">965</crm-item>
        <crm-item name="citation-id" type="number">73511187</crm-item>
        <crm-item name="journal-id" type="number">70407</crm-item>
        <crm-item name="deposit-timestamp" type="number">201501027</crm-item>
        <crm-item name="owner-prefix" type="string">10.2174</crm-item>
        <crm-item name="last-update" type="date">2015-01-27 05:11:51.0</crm-item>
        <crm-item name="citedby-count" type="number">0</crm-item>
        <doi_record>
          <crossref xmlns="http://www.crossref.org/xschema/1.1" xsi:schemaLocation="http://www.crossref.org/xschema/1.1 http://doi.crossref.org/schemas/unixref1.1.xsd">
            <journal>
              <journal_metadata language="en">
                <full_title>The Open Microbiology Journal</full_title>
                <abbrev_title>TOMICROJ</abbrev_title>
                <issn media_type="print">18742858</issn>
              </journal_metadata>
              <journal_issue>
                <publication_date media_type="print">
                  <month>1</month>
                  <day>21</day>
                  <year>2015</year>
                </publication_date>
                <journal_volume>
                  <volume>8</volume>
                </journal_volume>
                <issue>1</issue>
              </journal_issue>
              <journal_article publication_type="full_text">
                <titles>
                  <title>Pathogens in Urine from a Female Patient with Overactive Bladder Syndrome Detected by Culture-independent High Throughput Sequencing: A Case Report</title>
                </titles>
                <contributors>
                  <person_name sequence="additional" contributor_role="author">
                    <given_name>Huma</given_name>
                    <surname>Siddiqui</surname>
                  </person_name>
                  <person_name sequence="additional" contributor_role="author">
                    <given_name>Karin</given_name>
                    <surname>Lagesen</surname>
                  </person_name>
                  <person_name sequence="additional" contributor_role="author">
                    <given_name>Alexander</given_name>
                    <surname>J. Nederbragt</surname>
                  </person_name>
                  <person_name sequence="additional" contributor_role="author">
                    <given_name>Lars</given_name>
                    <surname>M. Eri</surname>
                  </person_name>
                  <person_name sequence="additional" contributor_role="author">
                    <given_name>Stig</given_name>
                    <surname>L. Jeansson</surname>
                  </person_name>
                  <person_name sequence="first" contributor_role="author">
                    <given_name>Kjetill</given_name>
                    <surname>S. Jakobsen</surname>
                  </person_name>
                </contributors>
                <publication_date>
                  <month>1</month>
                  <day>21</day>
                  <year>2015</year>
                </publication_date>
                <pages>
                  <first_page>148</first_page>
                  <last_page>153</last_page>
                </pages>
                <publisher_item>
                  <identifier id_type="sici">LiveAll1</identifier>
                </publisher_item>
                <doi_data>
                  <doi>10.2174/1874285801408010148</doi>
                  <resource>http://benthamopen.com/openaccess.php?tomicroj/articles/V008/148TOMICROJ.htm</resource>
                </doi_data>
              </journal_article>
            </journal>
          </crossref>
        </doi_record>
      </query>
    </body>
  </query_result>
</crossref_result>"""



# Main function 

def add_entry(doi = None):

  print ""
  print "Add a publication to the database"
  print ""

  record = {"authors":"", "year":"", "title":"", "journal":"", "doi":"", "pubmed":""}
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
  search_term = None
  if record['doi']:
    search_term = record['doi'] + '[doi]'
  else:
    search_term = pmid + '[uid]'
  
  if search_term: 
    data = get_info_from_pubmed(search_term)
  


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
  return get_path_element(base, path).firstChild.data


# Data formatting
def format_author(first, last):
  return last + " " + first[0:1]


# CrossRef DOI lookup functions

def format_crossref_authors(contributors):
  authors = []
  for person_name in contributors.childNodes:
    if person_name.nodeType == minidom.Node.ELEMENT_NODE and person_name.tagName == "person_name":
      first = get_path_data(person_name, ["given_name"])
      last = get_path_data(person_name, ["surname"])
      authors.append(format_author(first, last))

  return ", ".join(authors)
  

# example https://doi.crossref.org/servlet/query?pid=marius.bjornstad@medisin.uio.no&format=unixsd&id=10.3389/fmicb.2015.00017
def get_info_from_doi(doi):
  params = {"pid": "marius.bjornstad@medisin.uio.no", "format": "unixsd", "id":doi}
  #r = requests.get("https://doi.crossref.org/servlet/query", params=params)
  if True: #r.status_code == 200:
    #response = r.text
    dom = minidom.parseString(response)
    query = dom.getElementsByTagName("query")

    if len(query) == 1:
      q = query[0]
      if q.getAttribute("status") == "resolved":
        data = {}
        journal = get_path_element(q, ["doi_record", "crossref", "journal"])
        article = get_path_element(journal, ["journal_article"])

        data["authors"] = format_crossref_authors(get_path_element(article, ["contributors"]))
        data["year"] =    int(get_path_data(article, ["publication_date", "year"]))
        data["title"] =   get_path_data(article, ["titles", "title"])
        data["journal"] = get_path_data(journal, ["journal_metadata", "abbrev_title"])
        data["doi"] =     get_path_data(article, ["doi_data", "doi"])
        return data
      else: # status != resolved
        raise Exception("Unable to resolve the DOI")

  raise Exception("The CrossRef server returned invalid data or an error status")


# PubMed lookup functions
# e.g. http://www.ncbi.nlm.nih.gov/pubmed/?term=20140528&report=xml&format=text
def get_info_from_pubmed(search_term):
  url = "http://www.ncbi.nlm.nih.gov/pubmed/"
  params = {"term": search_term, "report": "xml", "format": "text"}

  r = requests.get(url, params)
  if r.status_code == 200:
    dom = minidom.parseString(r.text)

    data = {}
    article = dom.getElementsByTagName("Article")[0]
    data['year'] = 
    data['journal'] = get_path_data(article, ["Journal", "ISOAbbreviation"])
    return data
  else:
    raise Exception("Received status code " + r.status_code + " from server.")

if len(sys.argv) > 1:
  add_entry(sys.argv[1])
else:
  add_entry()

