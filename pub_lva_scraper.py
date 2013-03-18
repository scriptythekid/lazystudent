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

from pprint import pprint

print ""
print "This program is provided for educational services only. Use at your own risk."
inp = raw_input("continue?[y/n]").lower()
if inp != 'y':
    sys.exit(0)
print ""

def usage():
  print "	","usage:"
  print ""
  print "	",sys.argv[0], "<year+semester>"
  print ""
  print "   ","e.g.:", sys.argv[0],"2013S"
  print "               summer semester 2013",
  print "   ","e.g.:", sys.argv[0],"2013W"
  print "               winter semester 2013",

if len(sys.argv) > 1:
    semester = sys.argv[1]
else:
    print ""
    print "missing semester you're looking for"
    usage()
    sys.exit(1)

if not re.search('^[0-9]{4}W|S',semester):
    print "your semester seems malformed:",semester
    usage()
    sys.exit(1)

##FIXME
##sanitize input better for semester.  has to be in form: 2013S  or 2013W
##

start_url = "ht"+"tp:/"+"/diea"+"ngew"+"and"+"te.at"
publvadir='publiclvadir'

if not os.path.exists('output'):
  os.mkdir('output')
if not os.path.exists('output/%s' % publvadir):
  os.mkdir('output/%s' % publvadir)
  
browser = mechanize.Browser()
browser.set_handle_equiv(True)
#browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17')]

resp = browser.open(start_url)
browser.follow_link(browser.find_link(text_regex='Lehrveranstaltungen Online'))
#1st form = search, 2nd form = lva search
browser.select_form(nr=1)

browser.submit()

rhtml = browser.response().get_data()
s=BeautifulSoup(rhtml)
outdir = os.path.join('output',publvadir)
outfname = 'all.html'
fd = codecs.open(outfname, 'w', encoding='utf-8')
fd.write(unicode(rhtml, encoding=s.declaredHTMLEncoding))
fd.close()


def saveLVApage(lvanr,lvasem,rhtml,htmlencoding):
    ''''''
    tmpfname = lvasem + "_" + lvanr + ".html"
    tmpfd = codecs.open(os.path.join(outdir, tmpfname), 'w', encoding='utf-8')
    tmpfd.write(unicode(rhtml, encoding=htmlencoding))
    tmpfd.close()
    print lvanr,lvasem,"saved"
    
def parseLVApage(url,idx):
    ''''''
    ##FIXME global    learn to code...
    global browser
    global failedlvas
    lvanr = None
    vasem = None
    rhtml = None
    htmlencoding = None
    idx=unicode(idx)
    
    browser.open(url)
    rhtml= browser.response().get_data()
    tmps = BeautifulSoup(rhtml)
    htmlencoding=tmps.declaredHTMLEncoding
    try:    
        t=tmps.findAll(name='h2')[0]    #find first h2 tag
        lvanr = re.search('S[0-9]{3,7}', t.nextSibling.text).group(0)       #extract LVA-Nr e.g.S00106
    except Exception:
        print "error getting lva nr, using",idx,"as filename"
        lvanr = idx
    

    try:
        lvasem = tmps.findAll(name='h2')[0].nextSibling.text.split('/')[0].strip()
    except Exception:
        print "error extracting Semester of LVA. dunno what to do..."
        print "lva:",lvanr
        failedlvas.append(lvanr)
    
    print lvanr,lvasem,len(rhtml),htmlencoding
    
    return lvanr,lvasem,rhtml,htmlencoding
    
    
    
#XXX
#workaround because nr of links found via browser.links somehow doesnt return right amount of links
lvalinks = [x for x in s.findAll(name='a') if x.has_key('href') and 'inhalt' in x.attrMap['href']]

print len(lvalinks),"lva links"

failedlvas=[]
lvaidx=0

for link in lvalinks:
    print "idx:",lvaidx
    lvanr,lvasem,rhtml,htmlencoding = parseLVApage(link['href'],lvaidx)
    saveLVApage(lvanr,lvasem,rhtml,htmlencoding)
    
    if lvasem != semester:
        #the page we just fetched is not for the semester we're looking for...
        #is there a link to "next semester"?
        try:
            next_sem_link = browser.find_link(text_regex='chstes Semester')            
            lvanr,lvasem,rhtml,htmlencoding = parseLVApage(next_sem_link.absolute_url,unicode(lvaidx)+'b')
            saveLVApage(lvanr,lvasem,rhtml,htmlencoding)
            if lvasem != semester:
                #print "     STILL NOT selected semester. page saved but ignoring further links"
                print lvanr, "giving up for", semester
                pass
            else:
                pass
        except Exception,e:
            print "     Exception while trying next_sem_link..."
            print Exception
            print e
            print "     no next sem link"
                        
    else:
        print lvanr,"went fine on 1st hit"
        pass        
    #print "current url:", browser.geturl()    
    lvaidx += 1

