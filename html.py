import pubdb, sys, codecs

if sys.stdout.encoding == 'US-ASCII':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def get_html():
  html = ''
  year = "0"
  for record in pubdb.get_records():
    if record['year'] != year:
      year = record['year']
      html += '\n<p class="MsoNormal">&nbsp;</p>'
      html += ''
      html += '<p class="MsoNormal"><b>' + year + '</b></p>'
      html += '\n\n'

    # First line on normal left margin, next lines indented
    html += '<p class="MsoNormal" style="margin-left:36.0pt;text-indent:-36.0pt"><span style="mso-ascii-font-family:Cambria;mso-hansi-font-family:Cambria;mso-no-proof:yes">'
    # Authors, year and title
    html += record['authors'] + ". " + record['year'] + ". " + record['title']
    # Trailing full stop for title
    if record['title'][-1] != ".":
      html += '.'
    html += '</span> '
    # Journal in italics
    html += '<i style="text-indent: -36pt;">' + record['journal_abbrev'] + '</i>'
    if record['volume']:
      html += ' ' + record['volume']
      #if record['issue']: don't print issue number
      if record['pages']:
        html += ': ' + record['pages']
    html += '.<br/>'
    html += '<span style="text-indent: -36pt;">doi: <a href="http://dx.doi.org/'
    html += record['doi'] + '">' + record['doi'] + '</a> PMID:'
    html += '<a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=' + record['pubmed']
    html += '">' + record['pubmed'] + '</a> </span></p>'
    html += '\n\n'
  return html
    

print get_html()


