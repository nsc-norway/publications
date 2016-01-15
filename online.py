import requests
from xml.dom import minidom
import re
import datetime
import calendar


# XML tree navigation helper functions

# gets a "path" of tags, e.g. 'a','b','c' matches c in <a><b><c></c></b></a>
# because we can't use the XPath library with minidom
def get_path_element(base, path):
    elem = base
    for path_component in path:
        found = False
        if elem:
            for child in elem.childNodes:
                if child.nodeType == minidom.Node.ELEMENT_NODE and child.tagName == path_component:
                    elem = child
                    found = True
        if not found:
            elem = None
    return elem


# Get the text data in an xml tag
def get_path_data(base, path):
    element = get_path_element(base, path)
    if element:
        return element.firstChild.data.strip()
    else:
        return ''


# Data formatting
def format_author(first, last):
    strip_lower = u"".join(c for c in first if not c.islower())
    initials = re.sub(r"[. -]", '', strip_lower, re.UNICODE)[0:2]
    return unicode(last) + u" " + initials


# CrossRef DOI lookup functions
def format_crossref_authors(contributors):
    authors = []
    for person_name in contributors.childNodes:
        if person_name.nodeType == minidom.Node.ELEMENT_NODE and person_name.tagName == "person_name":
            first = get_path_data(person_name, ["given_name"])
            last = get_path_data(person_name, ["surname"])
            authors.append(format_author(first, last))

    return u", ".join(authors)


# Format pages, convert first and last page to a string range
# Using pubmed's notation where only different digits are shown in the end of
# the range.
def format_crossref_pages(pages_element):
    last = None
    first = None
    if pages_element:
        for ce in pages_element.childNodes:
            if ce.nodeType == minidom.Node.ELEMENT_NODE:
                if ce.tagName == "first_page":
                    first = ce.childNodes[0].data
                elif ce.tagName == "last_page":
                    last = ce.childNodes[0].data
    if last and first:
        i = 0
        if len(last) == len(first):
            while len(last) > 0 and first[i] == last[0]:
                last = last[1:]
                i = i + 1
        if len(last) > 0:
            return first + "-" + last
        else:
            return first
    elif first:
        return first
    else:
        return ""


# Returns (print publication date, electronic publication date,
# publication year)
def get_crossref_year(article):
    dates = article.getElementsByTagName("publication_date")
    print_year = sort_year = ''
    for d in dates:
        year = get_path_data(d, ["year"])
        media_type = d.getAttribute("media_type")
        if media_type == "online":
            sort_year = year
        elif media_type == "print":
            print_year = year
        else:
            if not print_year:
                print_year = year
            if not sort_year:
                sort_year = year

    if not sort_year:
        sort_year = print_year
    return (print_year, sort_year)


def read_journal(journal):
    article = get_path_element(journal, ["journal_article"])

    data = {}
    data["authors"] = format_crossref_authors(
        get_path_element(article, ["contributors"]))
    (data["year"], data["sortyear"]) = get_crossref_year(article)
    data["year"] = get_path_data(
        article, ["publication_date", "year"])
    data["title"] = get_path_data(article, ["titles", "title"])
    abbrev = get_path_data(
        journal, ["journal_metadata", "abbrev_title"])
    if abbrev:
        data["journal_abbrev"] = abbrev.replace(".", "")
    data["journal_full"] = get_path_data(
        journal, ["journal_metadata", "full_title"])
    data["volume"] = get_path_data(
        journal, ["journal_issue", "journal_volume", "volume"])
    data["issue"] = get_path_data(
        journal, ["journal_issue", "issue"])
    data["pages"] = format_crossref_pages(
        get_path_element(article, ["pages"]))
    data["doi"] = get_path_data(article, ["doi_data", "doi"])
    return data

def read_report(report):
    md = get_path_element(report, ["report-paper_metadata"])
    data = {}
    data["authors"] = format_crossref_authors(
        get_path_element(md, ["contributors"]))
    data["year"] = data["sortyear"] = get_path_data(
        md, ["publication_date", "year"])
    data["title"] = get_path_data(md, ["titles", "title"])
    data["doi"] = get_path_data(md, ["doi_data", "doi"])
    data["journal_full"] = "bioRxiv" if data["doi"].startswith("10.1101") else "(report)"
    data["journal_abbrev"] = data["journal_full"]
    data["volume"] = ""
    data["issue"] = ""
    data["pages"] = ""
    return data

# Main function for looking up a DOI
# example
# https://doi.crossref.org/servlet/query?pid=marius.bjornstad@medisin.uio.no&format=unixsd&id=10.3389/fmicb.2015.00017
def get_info_from_doi(doi):
    params = {"pid": "marius.bjornstad@medisin.uio.no",
              "format": "unixsd", "id": doi}
    r = requests.get("https://doi.crossref.org/servlet/query", params=params)
    if r.status_code == 200:
        response = r.text
        dom = minidom.parseString(r.text.encode('utf-8'))
        query = dom.getElementsByTagName("query")

        if len(query) == 1:
            q = query[0]
            if q.getAttribute("status") == "resolved":
                journal = get_path_element(
                    q, ["doi_record", "crossref", "journal"])
                if journal: # It's a journal article
                    return read_journal(journal)
                else:
                    report = get_path_element(q, 
                            ["doi_record", "crossref", "report-paper"])
                    if report:
                        return read_report(report)
                    else:
                        raise RuntimeError("Received an unexpected type of document from CrossRef")
            else:  # status != resolved
                raise Exception("Unable to resolve the DOI")

    raise Exception(
        "The CrossRef server returned invalid data or an error status")


# Takes an XML element (Name="AuthorList") as returned by the pubmed (entrez) service
# Returns a comma separated list of authors
def pubmed_authors(authors_list):
    authors = []
    for a in authors_list.getElementsByTagName("Item"):
        if a.getAttribute('Name') == "Author":
            authors.append(a.childNodes[0].data)

    return ", ".join(authors)


# See if the DOI is known in pubmed and get pubmed ID
def doi_to_pmid(doi):
    # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=10.1021/bi902153g
    url_doi2pmid = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": doi + "[doi]"}
    r = requests.get(url_doi2pmid, params=params)
    dom = minidom.parseString(r.text.encode('utf-8'))
    return dom.getElementsByTagName("Id")[0].childNodes[0].data


def getdata(cn):
    if len(cn) >= 1:
        return cn[0].data
    else:
        return ""


# PubMed lookup function
def get_info_from_pubmed(pmid):

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
                        printyear = getdata(cn).split(" ")[0]
                        if printyear:
                            data['year'] = printyear
                            if not data.has_key("sortyear"):
                                data['sortyear'] = printyear
                    elif name == "EPubDate":
                        epubyear = getdata(cn).split(" ")[0]
                        if epubyear:
                            data['sortyear'] = epubyear
                            if not data.has_key("year"):
                                data['year'] = epubyear
                    elif name == "Title":
                        data['title'] = getdata(cn)
                    elif name == "Source":
                        data['journal_abbrev'] = getdata(cn)
                    elif name == "FullJournalName":
                        data['journal_full'] = getdata(cn)
                    elif name == "Volume":
                        data['volume'] = getdata(cn)
                    elif name == "Issue":
                        data['issue'] = getdata(cn)
                    elif name == "Pages":
                        data['pages'] = getdata(cn)
                    elif name == "DOI":
                        data['doi'] = getdata(cn)
                elif item.nodeType == minidom.Node.ELEMENT_NODE and item.tagName == "Id":
                    data['pubmed'] = item.childNodes[0].data

            return data
        else:
            raise Exception("No data for this Pubmed ID.")

    raise Exception(
        "Received status code " + str(r.status_code) + " from server.")
