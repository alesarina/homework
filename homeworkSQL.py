import os
import re
os.system(r'C:\Users\1\Desktop\Homework\mystem.exe --eng-gr -nid C:\Users\1\Desktop\Homework\input.txt C:\Users\1\Desktop\Homework\output.txt')

f = open('output.txt', 'r', encoding='utf-8').readlines()
DB = open('DB.txt', 'w')
DB.write('CREATE TABLE maint (id INTEGER PRIMARY KEY, wordforms VARCHAR, position INTEGER, leftPunc VARCHAR, rightPunc VARCHAR, lemmNum INTEGER);' + '\n')
DB.write('CREATE TABLE lemmt (id INTEGER PRIMARY KEY, wordforms VARCHAR, lemm VARCHAR);' + '\n')

forms = []
lemms = []
rlemms = []
rforms = []
trforms = []
for line in f:
    p = line.split('{')
    wform = p[0]
    forms.append(wform)
    trforms.append(wform.lower())
    p2 = p[1]
    wlemm = str(p2).split('=')[0]
    lemms.append(wlemm.lower())
slemm = set(lemms)
swords = set(trforms)
for lem in lemms:
    if lem in slemm:
        rlemms.append(lem)
        slemm.remove(lem)
for wf in trforms:
    if wf in swords:
        rforms.append(wf)
        swords.remove(wf)
d1 = {}
d2 = {}
h = 0
w = 0
y = 0
d0 = {}
m = 0
while m < len(forms):
    d0[forms[m]] = trforms[m]
    m += 1
while h < len(rforms):
    Mb = trforms.index(rforms[h])
    d1[rforms[h]] = lemms[Mb] 
    h += 1
while w < len(rforms):
    d2[rforms[w]]=str(w)
    w += 1   
j = 0
while j < len(rforms): 
    twrFORM = rforms[j]
    twrLEMM = d1[twrFORM]
    twrN = d2[twrFORM]
    towr2 = 'INSERT INTO lemmt (id, wordforms, lemm) VALUES (' + str(j) + ', "' + twrFORM + '", "' + twrLEMM + '");' + '\n'
    DB.write(towr2)
    j += 1

trf = open('input.txt', 'r', encoding='utf-8').read()
reg = re.compile('[a-яА-Я0-9]+|[.,;:!?]+')
smb = reg.findall(trf)
#пишем отдельно для первого слова
towr0 = 'INSERT INTO maint (id, wordforms, position, leftPunc, rightPunc, lemmNum) VALUES (' + str(0) + ', "' + forms[0] + '", ' + str(1)
neeN0 = rforms.index(forms[0].lower())
nee0 = rforms[neeN0]
fl0 = d1[nee0] 
Nb0 = d2[nee0]
lPunc0 = '_'
if smb[1] not in '.,;!?:': 
    rPunc0 = '_'
else:
    rPunc0 = smb[1]
DB.write(towr0 + ', "' + lPunc0 + '", "' + rPunc0 + '", ' + Nb0 +  ');' + '\n')
smb.remove(smb[0])
smb.insert(0, '_')
ex = 1
for i in smb:
    if i in forms:
        towr1 = 'INSERT INTO maint (id, wordforms, position, leftPunc, rightPunc, lemmNum) VALUES (' + str(ex) + ', "' + i + '", ' + str(ex+1)
        neeN = rforms.index(i.lower())
        nee = rforms[neeN]
        fl = d1[nee]
        Nb = d2[nee]
        tri = []
        tri.append(smb[smb.index(i)-1])
        tri.append(i)
        tri.append(smb[smb.index(i)+1])
        if tri[0] in forms:
            lPunc = '_'
        else:
            lPunc = tri[0]
        if tri[2] in forms:
            rPunc = '_'
        else:
            rPunc = tri[2]
        DB.write(towr1 + ', "' + lPunc + '", "' + rPunc + '", ' + Nb +  ');' + '\n')
        ex += 1
    else:
        continue
DB.close()
