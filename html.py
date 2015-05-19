import pubdb
import sys
import codecs


def get_html():
    html = ''
    year = "0"
    for record in pubdb.get_records("DESC"):
        if record['sortyear'] != year:
            year = record['sortyear']
            html += '\n<p class="MsoNormal">&nbsp;</p>'
            html += ''
            html += '<p class="MsoNormal"><b>' + year + '</b></p>'
            html += '\n\n'

        # First line on normal left margin, next lines indented
        html += '<p class="MsoNormal" style="margin-left:36.0pt;text-indent:-36.0pt"><span style="mso-ascii-font-family:Cambria;mso-hansi-font-family:Cambria;mso-no-proof:yes">'
        # Authors, year and title
        html += record['authors'] + ". " + \
            record['year'] + ". " + record['title']
        # Trailing full stop for title
        if record['title'][-1] != ".":
            html += '.'
        html += '</span> '
        # Journal in italics
        html += '<i style="text-indent: -36pt;">' + \
            record['journal_abbrev'] + '</i>'
        if record['volume']:
            html += ' ' + record['volume']
            # if record['issue']: don't print issue number
            if record['pages']:
                html += ': ' + record['pages']
        html += '.<br/>'
        html += '<span style="text-indent: -36pt;">'
        if record['doi']:
            html += 'doi: <a href="http://dx.doi.org/'
            html += record['doi'] + '">' + record['doi'] + '</a> '
        if record['pubmed']:
            html += 'PMID:'
            html += '<a href="http://www.ncbi.nlm.nih.gov/pubmed/?term=' + \
                record['pubmed']
            html += '">' + record['pubmed'] + '</a> '
        html += '</span></p>'
        html += '\n\n'
    return html.encode('utf-8')


print get_html()
