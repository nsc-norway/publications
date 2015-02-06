import pubdb, sys, codecs

if sys.stdout.encoding == 'US-ASCII':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def get_html():
  html = ''
  year = "0"
  for record in pubdb.get_records():
    if record['year'] != year:
      year = record['year']
      print '<p class="MsoNormal">&nbsp;</p>'
      print ''
      print '<p class="MsoNormal"><b>' + year + '</b></p>'
      print ''

    html += '<p class="MsoNormal" style="margin-left:36.0pt;text-indent:-36.0pt"><span style="mso-ascii-font-family:Cambria;mso-hansi-font-family:Cambria;mso-no-proof:yes">'
    html += record['authors'] + ". " + record['year'] + ". "
    html += record['title'] + '</span><i style="text-indent: -36pt;">' + record['journal'] + '. </i><br/>'
    html += '<span style="text-indent: -36pt;">doi: <a href="http://dx.doi.org/'
    html += record['doi'] + '">' + record['doi'] + '</a> PMID:'
    html += '<a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=' + record['pubmed']
    html += '">' + record['pubmed'] + '</a> </span></p>'
    html += '\n\n'
  return html
    

print get_html()


