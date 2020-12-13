import os
import  bs4
import requests
import re
import time
from random import random
from time import sleep
import urllib.request 

start_time = time.time()

bangla_directory='Bangla_text'
english_directory='English_text'
bangla_html_directory= 'Bangla_html'
english_html_directory= 'English_html'

if not os.path.exists(bangla_directory):      os.makedirs(bangla_directory)
if not os.path.exists(english_directory):     os.makedirs(english_directory)  
if not os.path.exists(bangla_html_directory): os.makedirs(bangla_html_directory)
if not os.path.exists(english_html_directory):os.makedirs(english_html_directory)
    
def connected_to_internet(url):
    
    while True:
        
        try:
            data = requests.get(url)
            break
        except requests.ConnectionError:
            sleep(random()*3)
            #print("No internet connection available.")
            pass
    return data 

def write_html(url,file):
    
    while True:
        
        try:
            urllib.request.urlretrieve(url,file)
            break
            
        except Exception as e:
            sleep(random()*3)
            if str(e)== "HTTP Error 404: Not Found":
                page = requests.get(url)
                soup = bs4.BeautifulSoup(page.content, 'html.parser')
                f = open(file, "a")
                f.write(soup.prettify())
                f.close()
                break
                            #print("No internet connection available.")
            pass

def ScrapText(URL,count,lang):
    dat =connected_to_internet(URL)
    
    sp= bs4.BeautifulSoup(dat.text, 'lxml')
    
    allText=sp.find_all("p")
    if lang is "bangla"  :
        file1=bangla_directory+"/"+str(count)+"_bn.txt"
        file2=bangla_html_directory+"/"+str(count)+"_bnhtml.txt"
        
    if lang is "english" :
        file1=english_directory+"/"+str(count)+"_eng.txt"
        file2=english_html_directory+"/"+str(count)+"_enghtml.txt"
    
    with open(file1, 'w', encoding='utf-8') as f_out:
        for textContents in allText:
            f_out.write(textContents.text)
      
    write_html(URL,file2)
            
def checkAndGetEnglishLink(URL):
    dat = connected_to_internet(URL)
    sp= bs4.BeautifulSoup(dat.text, 'html.parser') 
    #print(sp)
    d=sp.find_all('a',attrs={'class':'interlanguage-link-target','lang':'en'})  
    
    if len(d) is not 0:  #checking if english is available   
        for links in d:
            return links.get('href')
    if len(d) is 0: return 1
    


def countFile():
    init1=len([name for name in os.listdir(bangla_directory) if os.path.isfile(os.path.join(bangla_directory, name))])
    init2=len([name for name in os.listdir(english_directory) if os.path.isfile(os.path.join(english_directory, name))])
    init3=len([name for name in os.listdir(bangla_html_directory) if os.path.isfile(os.path.join(bangla_html_directory, name))])
    init4=len([name for name in os.listdir(english_html_directory) if os.path.isfile(os.path.join(english_html_directory, name))])
    
    return min([init1,init2,init3,init4])
    

 ####### 
def RUN():
    global fcounter
    init= countFile()
    if init is not 0: 
        init-=1
        fcounter=init      
    if init is 0:fcounter=1
        
    with open('ALL_LINKS.txt') as f:
        for count,LinkInside in enumerate(f,1):
            
            #if (count%1000)==0:print(count)

            if count >init:
                
                URL_txt= checkAndGetEnglishLink(LinkInside[:-1])
                print(LinkInside[:-1])
                if URL_txt is not 1:
                    
                    ScrapText(LinkInside,fcounter,"bangla")
                    #sleep(random()*3)
                    #print("done")
                    ScrapText(URL_txt,fcounter,"english")
                    fcounter+=1
                    

                                   
while True:
    try:
        RUN()
        break
    except Exception as e:
        print(str(e))
        sleep(random()*5)
        
print("\n")
print("--- Execution time in hour ====",(time.time() - start_time)/3600)