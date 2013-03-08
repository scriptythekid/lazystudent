#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from BeautifulSoup import BeautifulSoup
import codecs
from mako.template import Template
import re

try:
  semester = 'SS' if sys.argv[1].upper() == 'SS' else 'WS'
except Exception:
  print ""
  print "	","usage:"
  print ""
  print "	",sys.argv[0],"<semester>"
  print ""
  print "	",sys.argv[0],"WS"
  print "	",sys.argv[0],"SS"
  print ""
  sys.exit(1)
  
lvas=[]
for x in os.listdir('output/%s' % semester):
  fd=codecs.open(os.path.join('output',semester,x), encoding='utf-8')
  s = BeautifulSoup(fd.read())
  fd.close()
  
  lva={'lva_info':None,
	'personlink':None,
	'person':None,
	'descr':None,
	'nachweis':None,
	'ort':None,
	'anmerkungen':None,
	'has_DK':None,
	'ects':None,
	'wstd':None,
	'lvanr':None,
	'lvatype':None,
	'semester':None,
	'abschnitt':'not implemented yet',
	}
  lva['has_DK'] = False
  
  
  hasinfo = s.findAll(name='h1')
  if hasinfo:
    lva['lva_info'] = hasinfo[0].text
    #infos = [x.replace('(','').replace(')','').strip() for x in re.search('\([a-zA-Z0- .\/\)]*',lva['lva_info']).group(0).split('/')]
    infostr = lva['lva_info']
    infostr = infostr[infostr.rfind('('):]
    infos = [x.strip() for x in infostr.split('(')[1].split(')')[0].split('/')]

    
    lva['ects'] = re.search('[0-9,]+ ECTS',lva['lva_info']).group(0).replace('ECTS','').strip()
    lva['wstd'] = re.search('[0-9]+ WStd',lva['lva_info']).group(0).replace('WStd','').strip()
    lva['lvatype'] = infos[3]
    lva['lvanr'] = infos[4]
    lva['semester'] = infos[0]
    
  hasperson = s.findAll(name='h2')
  if hasperson:
    lva['personlink'] = hasperson[0].next.next
    lva['person'] = unicode(s.findAll(name='h2')[0].next.next.text)
  
  hasdescr = s.find(text="Themenstellung der Lehrveranstaltung")
  if hasdescr:
    lva['descr'] = hasdescr.findNext(name='tr').text
  
  hasnachweis = s.find(text="Nachweis der erworbenen Kompetenzen durch:")
  if hasnachweis:
    lva['nachweis'] = hasnachweis.findNext(name='tr').text
  
  hasort = s.find(text="Angaben zu Ort und Zeit der Lehrveranstaltung:")
  if hasort:
    lva['ort'] = hasort.findNext(name='tr').text
  
  hasanmerk = s.find(text="Anmerkungen:")
  if hasanmerk:
    lva['anmerkungen'] = hasanmerk.findNext(name='tr').text
  
  
  hasstudiplatz = s.find(text="Studienplanzuordnungen:")
  if hasstudiplatz:
    studieslist = [x.text for x in hasstudiplatz.findAllNext(name='tr')]
    studiestext = os.linesep.join(studieslist)
    lva['has_DK'] = 'digitale kunst' in studiestext.lower()
  lvas.append(lva)
  
  #dev h4x
  #if len(sys.argv) > 2 and sys.argv[2] and len(lvas) > 10: break


myt= Template(filename='index_template.mako', output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'],  encoding_errors='replace')
htmlout = myt.render_unicode(data=lvas)
outfilename=os.path.join('output',semester,'index.html')
fd = codecs.open(outfilename, 'w', encoding='utf-8')
fd.write(htmlout)
fd.close()
print "done"
print "output written to",outfilename


