import os
import  bs4
import requests
import re
import time

import urllib.request 
start_time = time.time()

def connected_to_internet(url):
    
    while True:
        
        try:
            data = requests.get(url)
            #data = requests.get(url,time.sleep(seconds))
            break
        except requests.ConnectionError:
            #print("No internet connection available.")
            pass
    return data 

def get50Links(url):
    data = connected_to_internet(url)
    soup= bs4.BeautifulSoup(data.text, 'lxml')
    data=soup.find_all("table",attrs={'style':'padding-top: 0px; width: 80%; border-collapse: separate; font-size: 100%;'})
    allLink=[]
    for td in data[0].find_all("td"):
        for link in td:
            if isinstance(link, bs4.NavigableString): continue
            else: 
                s=link.get('href')
                if s[0]== "/":
                    allLink.append('https://bn.wikipedia.org'+s)
    return allLink

def getPorobortiPageLink(URL):
    dat = connected_to_internet(URL)
    sp= bs4.BeautifulSoup(dat.text, 'lxml') # 'html.parser')
    d=sp.find_all("div",attrs={'class':'mw-allpages-nav'})    
    I=0
    for t in d[0]:
        if isinstance(t, bs4.NavigableString): continue
        else: 
            if I is 1:
                s=t.get('href')
                if s[0]== "/": v= ('https://bn.wikipedia.org'+s)
        I+=1
        
    if I is 2: return v
    else: return 1
    
def getEveryLink(URL):
    dat= connected_to_internet(URL)
    soup= bs4.BeautifulSoup(dat.text, 'lxml')
    data=soup.find_all("ul",attrs={'class':'mw-allpages-chunk'})  
    allLinks=[]

    for links in data[0]:
        for link in links:
            if isinstance(link, bs4.NavigableString):
                print(link)
                
            if isinstance(link, str):
                if link[0]== "/":
                    v= ('https://bn.wikipedia.org'+link)
                    allLinks.append(v)
                #else: allLinks.append(v)
            else :
                n=link.get('href')
                if n[0]== "/":
                    v= ('https://bn.wikipedia.org'+n)
                    allLinks.append(v)
                else: allLinks.append(n)
                    
    return allLinks

    


url ="https://bn.wikipedia.org/wiki/%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%A7%E0%A6%BE%E0%A6%A8_%E0%A6%AA%E0%A6%BE%E0%A6%A4%E0%A6%BE"

LinksList=get50Links(url)
myfile = open('Links.txt', 'w')
fileCounter=1
LinksList.pop() # discard last element


for iii,addr in enumerate(LinksList): 
    
    while True:
        
        LinksInside=getEveryLink(addr)
        
        for LinkInside in LinksInside:
            myfile.writelines(LinkInside+"\n")
            fileCounter+=1

        v=getPorobortiPageLink(addr)
        addr=v
        if v is 1: break

    print("finished ",iii+1, " out of ",len(LinksList))
    
myfile.close()


# if not os.path.isfile('ALL_LINKS.txt') :
#     with open('ALL_LINKS.txt', 'w') as fp: 
#         pass  

# os.system("awk '!x[$0]++' Links.txt > ALL_LINKS.txt")  # To remove duplicate links
print("Total Files =",fileCounter) 
print("\n")
print("--- Execution time ====",(time.time() - start_time)/60)