#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import mechanize
import sys
from BeautifulSoup import BeautifulSoup
import getpass
import codecs
import os
import re

def usage():
  print "	","usage:"
  print ""
  print "	",sys.argv[0],"<username> <semester> <abschnitt>"
  print ""
  print "	","e.g.:"
  print "	",sys.argv[0],"s12345678 SS 2"
  print "	",""
  print "	","user:	   username"
  print "	","semester: SS or WS"
  print "	","abschnitt: 1 or 2" 

try:
  user = sys.argv[1]  
  semester = 'SS' if sys.argv[2].upper() == 'SS' else 'WS'
  abschnitt = 1 if sys.argv[3] == '1' else 2
  pwd = getpass.getpass()
except Exception:
  usage()
  sys.exit(1)

start_url = "http://ser"+"vice.un"+"i-a"+"k.a"+"c.a"+"t/"

if not os.path.exists('output'):
  os.mkdir('output')
if not os.path.exists('output/%s' % semester):
  os.mkdir('output/%s' % semester)
  
browser = mechanize.Browser()
browser.set_handle_equiv(True)
#browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17')]

resp = browser.open(start_url)
browser.follow_link(browser.find_link(url_regex='4DCGI/service', tag='frame'))
browser.follow_link(browser.find_link(url_regex='st_login'))
browser.select_form(nr=0)

browser['USR_http_userid_t'] = user
browser['USR_http_Passwort_t'] = pwd
#ugly hack to make it work:
browser.form.enctype = 'application/x-www-form-urlencoded'
resp = browser.submit()
browser.follow_link(browser.find_link(text_regex='Studienplananalyse'))

if abschnitt == 1:
  mylinks = [x for x in browser.links() if 'st_analyse_pr_liste' in x.url][:3]
else:
#relevant links .. (first 3: 1ter abschnitt, rest 2nd abschnitt)
  print "2ter abschnitt"
  mylinks = [x for x in browser.links() if 'st_analyse_pr_liste' in x.url][3:]



lvas = []
lvadict = []
idx=0
for x in mylinks:
  print "following:",x.url
  browser.follow_link(x)
  browser.follow_link(browser.find_link(text_regex='Aktuelles Lehrangebot zu diesem Fach'))
  
  semlinks=[]
  pagelinks = [x for x in browser.links() if 'st_sp_lv_liste' in x.url]
  if len(pagelinks) > 0:
    for page in pagelinks:
      print "following:",page.url
      browser.follow_link(page)
      semlinks = semlinks + [x for x in browser.links() if semester in x.text]
  else:
    semlinks = [x for x in browser.links() if semester in x.text]
  
  for lv in semlinks:
    print "following:",lv.url
    browser.follow_link(lv)
    resp = browser.response()
    lvas.append(resp.get_data())
    try:
      a = re.search('le_lv_inhalt\?[A-Za-z0-9]+\?', browser.geturl())
      lva_name = a.group(0).replace('le_lv_inhalt','').replace('?','')
      print "lva_name:",lva_name
      
    except Exception,e:
      print "error getting lva number"
      lva_name = idx
      
    try:
      lvadict.append({'name':lva_name,'html':resp.get_data()})
    except Exception,e:
      print "error adding lva to lvadict"
    
    idx+=1
    

print "done scraping"
print "writing html files"

for x in lvadict:
  lva_name = x['name']
  lvahtml = x['html']
  outfilename = 'output/%s/%s.html' % (semester, lva_name)
  outf = codecs.open(outfilename, 'w', encoding='utf-8')
  outf.write(unicode(lvahtml, encoding='utf-8'))
  #outf.write(unicode(os.linesep))
  print "written:",outfilename
  outf.close()



