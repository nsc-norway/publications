import pubdb
import sys
import codecs


top_of_page = """
====================================
Publications
====================================

.. uio-meta::
   :responsible-name: Arvind Sundaram / Marius Bjørnstad
   :responsible-email: post@seuencing.uio.no
   :image: papers_per_year.png

.. uio-introduction::

  Her er en ingress.

.. contents::

.. section-numbering::

In case we had missed your publication in the list below, please let us know
through our `publication registration form 
<https://nettskjema.uio.no/answer/61221.html>`.


Første hovedavsnitt
=======================
Med litt tekst

Andre hovedavsnitt
=======================
Med litt tekst også.
"""

def get_doc():
    output = top_of_page
    year = "0"
    for record in pubdb.get_records("DESC"):
        if record['sortyear'] != year:
            year = record['sortyear']
            output += year + "\n"
            output += "=========="

        # Authors, year and title        
        output += "| " + record['authors'] + ". " + record['year'] + ". " + record['title']
        # Trailing full stop for title
        if record['title'][-1] != ".":
            output += '.'
        # Journal in italics
        output += '*' + record['journal_abbrev'] + '*'
        if record['volume']:
            output += ' ' + record['volume']
            if record['pages']:
                html += ': ' + record['pages']
        output += "| " # To make a new line
        if record['doi']:
            output += 'doi: `{}<http://dx.doi.org/{}>`_ '.format(
                record['doi'], record['doi'])
        if record['pubmed']:
            output += 'PMID: `{}<http://www.ncbi.nlm.nih.gov/pubmed/?term={}>`_'.format(
                record['pubmed'], record['pubmed']
            )
        output += '\n\n'
    return output


if __name__ == "__main__":
    print(get_doc())
