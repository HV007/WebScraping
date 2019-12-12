import requests
import os
from bs4 import BeautifulSoup
import re
def get_key(val,my_dict): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key
d={'january':1,
   'february':2,
   'march':3,
   'april':4,
   'may':5,
   'june':6,
   'july':7,
   'august':8,
   'september':9,
   'october':10,
   'november':11,
   'december':12}
fin=open('input.txt','r')
lines=fin.readlines()
if lines[0]=='Random':
    URL='http://explosm.net/rcg'
    r=requests.get(URL)
    os.mkdir('./random')
    soup=BeautifulSoup(r.content,'html5lib')
    row=soup.find('div',attrs={'class':'rcg-panels'})
    images=row.find_all('img')
    for i in range(3):
        url=images[i]['src']
        fout=open('./random/frame'+str(i)+'.jpg','wb')
        fout.write(requests.get(url).content)
        fout.close()
elif (lines[0].split())[0]=='latest':
    n=int(lines[0].split()[1])
    URL='http://explosm.net/comics/archive'
#    r=requests.get(URL)
#    soup=BeautifulSoup(r.content,'html5lib')
    os.mkdir('./latest')
    i=2019
    j=12
    flag=True
    while flag:
        if j==12:
            nURL=URL+'/'+str(i)
        else :
            nURL=URL+'/'+str(i)+'/'+str(j)
        r=requests.get(nURL)
        soup=BeautifulSoup(r.content,'html5lib')
        rows1=soup.find_all('div',attrs={'class':'small-3 medium-3 large-3 columns'})
        rows2=soup.find_all('div',attrs={'id':'comic-author'})
        for k in range(len(rows2)):
            url='http://explosm.net'+rows1[k].a['href']
            s=rows2[k].text
            L=re.split(' |/n',s)
            author=L[1]
            date=L[0][1:11]
            new_r=requests.get(url)
            new_soup=BeautifulSoup(new_r.content,'html5lib')
            div=new_soup.find('div',attrs={'id':'comic-wrap'})
            new_url='http:'+div.img['src']
            fout=open('./latest/'+date+'-'+author+'.jpg','wb')
            fout.write(requests.get(new_url).content)
            fout.close()
            n-=1
            if n==0:
                flag=False
                break
        if j==0:
            j=12
            i-=1
        else :
            j-=1
else :
    start_month,start_year=(lines[0].split())
    end_month,end_year=(lines[1].split())
    authors=lines[2].split()
    fin.close()
    start=int(start_year)
    end=int(end_year)
    URL='http://explosm.net/comics/archive'
#    r=requests.get(URL)
#    soup=BeautifulSoup(r.content,'html5lib')
    for i in range(start,end+1):
        os.mkdir('./'+str(i))
        if start==end:
            start1=d[start_month]
            end1=d[end_month]
        elif i==start:
            start1=d[start_month]
            end1=12
        elif i==end:
            start1=1
            end1=d[end_month]
        for j in range(start1,end1+1):
            os.mkdir('./'+str(i)+'/'+get_key(j,d))
            if j==12:
                nURL=URL+'/'+str(i)
            else :
                nURL=URL+'/'+str(i)+'/'+str(j)
            r=requests.get(nURL)
            soup=BeautifulSoup(r.content,'html5lib')
            rows1=soup.find_all('div',attrs={'class':'small-3 medium-3 large-3 columns'})
            rows2=soup.find_all('div',attrs={'id':'comic-author'})
            for k in range(len(rows2)):
                url='http://explosm.net'+rows1[k].a['href']
                s=rows2[k].text
                L=re.split(' |/n',s)
                author=L[1]
                date=L[0][1:11]
                if author in authors:
                    new_r=requests.get(url)
                    new_soup=BeautifulSoup(new_r.content,'html5lib')
                    div=new_soup.find('div',attrs={'id':'comic-wrap'})
                    new_url='http:'+div.img['src']
                    fout=open('./'+str(i)+'/'+get_key(j,d)+'/'+date+'-'+author+'.jpg','wb')
                    fout.write(requests.get(new_url).content)
                    fout.close()