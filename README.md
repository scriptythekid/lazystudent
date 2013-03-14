lazystudent
===========

parses the lvv and gives you a nice set of html pages for your personal scraping fun, a nice table with realtime search
is included, to access the search function enter the textarea on top and start typing

sorting by any argument is done by clicking the names of the tables, a good usage scenario would be finding all lvs
matching a weekday and then sorting by ects...


usage:

```python lazystudent.py <username> <semester> <abschnitt>```

* username = sMatrikelNr  e.g.: s1234567
* 	semester: SS or WS
* 	abschnitt: 1 or 2
* 
* e.g.: ```	python lazystudent.py s1234567 SS 2```


when the scraping is done run this:

```python parse_lazyoutput.py   <semester>```

e.g.:

```	python parse_layoutput.py SS```

then open the file ```./output/SS/index.html```
type in the search field on top to search...
have fun

