import html

print("Generating files...")

constant_html = '<p class=\"MsoNormal\" style=\"margin-left:36.0pt;text-indent:-36.0pt\">&nbsp;</p>\n\n<p class=\"MsoNormal\">&nbsp;&nbsp;<img alt=\"\" height=\"333\" src=\"/publications/papers_per_year.png\" style=\"width: 726px; height: 333px;\" width=\"726\" /><br />\n&nbsp;</p>\n\n<p class=\"MsoNormal\" style=\"margin-left: 36pt; text-indent: -36pt;\"><span style=\"mso-ascii-font-family:Cambria;mso-hansi-font-family:Cambria;mso-no-proof:yes\">In case we had missed your publication in the list below, please let us know through our&nbsp;<a href=\"https://nettskjema.uio.no/answer/61221.html\">publication registration form</a>.</span></p>\n\n<p>&nbsp;</p>'

content = constant_html + html.get_html()

with open("index.html", "w") as f:
    f.write("""{
   "resourcetype": "structured-article",
   "properties": {
      "showAdditionalContent": "false",
      "title": "Publications",
      "content": "%s",
      "hidePicture": "false"
   }
}""" % (content.replace("\n", "\\n").replace("\"", "\\\"")))

import graph #execute it

print("Upload index.html and papers_per_year.png to the WebDAV at:")
print("https://www-dav.sequencing.uio.no/publications/")

