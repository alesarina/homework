import urllib.request
import re
import os

ht = open('ПОЛИТИКЭР _ Адыгэ Макъ.html', 'r', encoding='utf-8').read()
retxt = re.compile('<p>(.*?)</p>', flags=re.U | re.DOTALL) #для аккуратности решила искать текст в разных тегах отдельно
alltxt = retxt.findall(ht)
reheads = re.compile('<h1>.*?<a .*?>(.*?)</a>.*?</h1>', flags=re.U | re.DOTALL)
allheads = reheads.findall(ht)
respans = re.compile('<span.*?>(.*?)</span>', flags=re.U | re.DOTALL)
allspans = respans.findall(ht)
alltxt.extend(allheads)
alltxt.extend(allspans)

regTag = re.compile('<.*?>', flags=re.DOTALL)
regSpace = re.compile('\s{2,}', flags=re.DOTALL)
regSmb = re.compile('«|»|\.|,|;|:|/|—|&#8230|[0-9]', flags=re.U | re.DOTALL)
artWords = []
for elem in alltxt:
    clean1 = regTag.sub(' ', elem)
    clean2 = regSpace.sub(' ', clean1)
    h = clean2.split(' ')
    for w in h:
        cleaned = regSmb.sub('', w)
        if cleaned != '':
            artWords.append(cleaned.lower())
pageWords = set(artWords)
f = open('adyghe-unparsed-words.txt', 'r', encoding='utf-8')
fWords = []
for line in f:
    fWords.append(line[:-2])
fileWords = set(fWords)
common = fileWords & pageWords
answer = open('wordlist.txt', 'w', encoding='utf-8')
for word in common:
    answer.write(word + '\n')
answer.close()

os.system(r'C:\Users\1\Desktop\Exam\mystem.exe -nid C:\Users\1\Desktop\Exam\wordlist.txt C:\Users\1\Desktop\Exam\output.txt')
mstl = open('output.txt', 'r', encoding='utf-8')
rusN = []
for line in mstl:
    if '=' in line:
        parts = line.split('=')
        part = parts[1]
        PoS = part[0]
        GN = parts[2]
        if PoS == 'S' and GN == 'им,ед}\n':
            fin = line.split('{')
            rusN.append(fin[0])
        if '|' in line:
            vr = line.split('|')
            j = 0
            while j < len(vr):
                qw = vr[j].split('=')
                PoS = (qw[1])[0]
                GN = qw[2]
                if PoS == 'S' and GN == 'им,ед}\n':
                    fin = line.split('{')
                    rusN.append(fin[0])
                elif PoS == 'S' and GN == 'им,ед':
                    fin = line.split('{')
                    rusN.append(fin[0])
                j += 1
mstl.close()
nounsf = open('rus_nouns.txt', 'w', encoding='utf-8')
for noun in rusN:
    nounsf.write(noun + '\n')
nounsf.close()

os.system(r'C:\Users\1\Desktop\Exam\mystem.exe -nid C:\Users\1\Desktop\Exam\rus_nouns.txt C:\Users\1\Desktop\Exam\rus_output.txt')
DB = open('sql.txt', 'w', encoding='utf-8')
DB.write('CREATE TABLE rus_words (wordform VARCHAR, lemma VARCHAR);' + '\n')
material = open('rus_output.txt', 'r', encoding='utf-8')
for line in material:
    p1 = line.split('{')
    wform = p1[0]
    p2 = p1[1].split('=')
    if '?' not in p2[0]:
        lemm = p2[0]
    else:
        lemm = (p2[0])[:-1]
    DB.write('INSERT INTO rus_words (wordform, lemma) VALUES ("' + wform + '", "' + lemm + '");' + '\n')
material.close()
DB.close()
