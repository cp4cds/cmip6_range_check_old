


##
## 23 tables
##
ntable = 23
table_list = "Oyr Omon AERmon Amon CFmon LImon SImon Emon EmonZ ImonGre AERmonZ ImonAnt day Oday CFday Eday EdayZ 3hr E3hr CF3hr 6hrPlev Ofx fx".split()


table_by_mode = {'all':"Oyr Ofx fx EdayZ".split(),
                 'sampledonepercent':"day Oday CFday Eday".split(),
                 'sampledtenpercent':"Omon AERmon Amon CFmon LImon SImon Emon EmonZ ImonGre AERmonZ ImonAnt".split(),
                 'sampledoneperthou':"3hr E3hr CF3hr 6hrPlev".split()
                }

mode_by_table = {}
for k,l in table_by_mode.items():
  for t in l:
    mode_by_table[t] = k

e1 = [x for x in mode_by_table.keys() if x not in table_list]
e2 = [x for x in table_list if x not in mode_by_table.keys()]
assert len(e1) == 0, "tables missing from mode_by_table: %s" % e1
assert len(e2) == 0, "extra tables in mode_by_table: %s" % e2
