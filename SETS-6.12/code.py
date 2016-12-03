import re
import urllib.request
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
commonUrl = 'https://news.rambler.ru/weapon/35447948-ssha-zakupili-rossiyskie-pistolety-osa/items/'

req = urllib.request.Request(commonUrl, headers={'User-Agent':user_agent})
with urllib.request.urlopen(req) as response:
    ht = response.read().decode('utf-8')
relinks = re.compile('<a\nhref="(\S*?)"\nclass="j-metrics__clicks-out-source-subject article-sources__subject".*?>.*?</a>', flags=re.U | re.DOTALL)
links = relinks.findall(ht) #тут массив ссылок на сторонние сайты с новостями

#TASS
TASS = urllib.request.Request(links[5], headers={'User-Agent':user_agent})
with urllib.request.urlopen(TASS) as response:
    pTASS = response.read().decode('utf-8')
reTASS = re.compile('<p>(.*?)</p>', flags=re.U | re.DOTALL)
lTASS = reTASS.findall(pTASS)#массив, содержащий все абзацы текста с сайта RNS
tTASS = ' '.join(lTASS)
reclean = re.compile('\"|\"|\(|\)|,|\.|- ', flags=re.U | re.DOTALL)
reclean1 = re.compile('\xa0', flags=re.U)
reclean2 = re.compile('штатов ', flags=re.U)
cleanedTASS1 = reclean.sub('', tTASS)
cleanedTASS2 = reclean1.sub(' ', cleanedTASS1)
cleanedTASS = reclean2.sub('штатов', cleanedTASS2)
TASSwords = set(cleanedTASS.lower().split(' ')[4:])

#Rambler News Service
RNS = urllib.request.Request(links[2], headers={'User-Agent':user_agent})
with urllib.request.urlopen(RNS) as response:
    pRNS = response.read().decode('utf-8')
reRNS = re.compile('<p>(.*?)</p>', flags=re.U | re.DOTALL)
lRNS = reRNS.findall(pRNS)
tRNS = ' '.join(lRNS)
reclean1 = re.compile('— |- |\"|\"|»|«|,|\.|\(|\)|&quot;', flags=re.U)
reclean2 = re.compile('\\xa0', flags=re.U)
cleanedRNS1 = reclean1.sub('', tRNS)
cleanedRNS = reclean2.sub(' ', cleanedRNS1)
cleanedRNS = cleanedRNS.lower()
RNSwords = set(cleanedRNS.lower().split(' ')[:-1])

#РЕН ТВ
RTV = urllib.request.Request(links[6], headers={'User-Agent':user_agent})
with urllib.request.urlopen(RTV) as response:
    pRTV = response.read().decode('utf-8')
reRTV = re.compile('<p>(.*?)</p>', flags=re.U | re.DOTALL)
lRTV = reRTV.findall(pRTV)
lRTV = lRTV[:4]
tRTV = ' '.join(lRTV)
reclean1 = re.compile('– |\"|,|\.|<em>|</em>', flags=re.U)
reclean2 = re.compile('&nbsp;', flags=re.U)
cleanedRTV1 = reclean1.sub('', tRTV)
cleanedRTV = reclean2.sub(' ', cleanedRTV1)
RTVwords = set(cleanedRTV.lower().split(' '))

#Вестник Кавказа
VK = urllib.request.Request(links[8], headers={'User-Agent':user_agent})
with urllib.request.urlopen(VK) as response:
    pVK = response.read().decode('utf-8')
reVK = re.compile('<p>(.*?)</p>', flags=re.U | re.DOTALL)
lVK = reVK.findall(pVK)
lVK = lVK[:5]
tVK = ' '.join(lVK)
reclean = re.compile(' - |&quot;|,|\.|\(|\)', flags=re.U)
cleanedVK = reclean.sub('', tVK)
VKwords = set(cleanedVK.lower().split(' '))

c1 = TASSwords & RNSwords
c2 = RTVwords & VKwords
com = c1 & c2
f_com = open('common.txt', 'w')
for word in sorted(list(com)):
    f_com.write('%s\n' % word)
f_com.close()

un1 = TASSwords ^ RNSwords
un2 = RTVwords ^ VKwords
uniq = un1 ^ un2
f_un = open('unique.txt', 'w')
for word in sorted(list(uniq)):
    f_un.write('%s\n' % word)
f_un.close()
