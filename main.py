import sys
import os.path
import urllib.request
from urllib.parse import unquote
from bs4 import BeautifulSoup

targetdir = 'Z:\\1\\'

def progress(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*dMb / %dMb" % (percent, 5, readsofar/1024/1024, totalsize/1024/1024)
        sys.stderr.write(s)
        if readsofar >= totalsize:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (readsofar,))

with open('1.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src,'lxml')

urls = soup.find_all('a', class_='filename')
count = len(urls)
print(str(count) + ' серий найдено...')

totalsize = 0

#Проверка наличия файлов
for url in urls:
    try:
        remotefile = urllib.request.urlopen(url.attrs['href'])
    except:
        print('404 Not found! ' + url.attrs['href'])
        urls.remove(url)
        continue
    totalsize = totalsize + remotefile.length

print(str(count) + ' серий доступно...')
print('Общий размер в гигабайтах: ' + str(round(totalsize/1024/1024/1024,2)))

for url in urls:
    nam = urllib.parse.unquote(url.attrs['href'])
    idx = nam.find('filename=') + 9
    nam = nam [idx:]
    print (nam)
    targetfile = targetdir + nam
    if not os.path.exists(targetfile):
        urllib.request.urlretrieve(url.attrs['href'],targetfile,progress)
    print ('Скачано..')
    count -= 1
    print('Осталось: '+ str(count))