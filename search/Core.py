from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
class Crawler:
    #sites to search text in in:
    #sites=['https://www.mehrnews.com/','http://www.irna.ir/','http://www.farsnews.com/','https://www.isna.ir/']    #for storing links to visit later

    #correct the found URL if it's relative
    def correctURL(self,link,domain): 
        link=urljoin(domain,link)  
        return link

    #check if a page contains the text we're looking for
    def TextExistsInPage(self,soup,text):
        H1=soup.find_all('h1')
        if H1:
            for h1 in H1:
                if(text in h1.get_text()):
                    return True
        A=soup.find_all('a', href=True)
        if A:
            for a in A:
                if('tag' in a.get('href') or 'key' in a.get('href')):
                    if (text in a.get_text()):
                        return True
        return False

    #main search function
    def search(self,text,depth,site):
        unVisitedLinks =[]
        visitedLinks =[]    
        links = []
        depthLimit=0
        resultPages=[]
        depthLimit=int(depth)

        startPage =site
        depth=0
        unVisitedLinks.append(startPage)
        print("\n Searching in "+startPage+" :")

        while(len(unVisitedLinks)!=0):
            if depth>depthLimit:
                break

            currentPage=unVisitedLinks.pop()
            if currentPage in visitedLinks:
                continue

            try:
                page = requests.get(currentPage)
                
                print(currentPage)
            except Exception as e:
                print(str(e))
                continue

            soup = BeautifulSoup(page.content,'html.parser')

            #add page to results if text exists in it
            if (self.TextExistsInPage(soup,text)):
                htag=''
                ptag=''
                H1=soup.find_all('h1')
                for h1 in H1:
                    if(text in h1.get_text()):
                        htag=h1.get_text()
                P=soup.find_all('p')
                for p in P:
                    if(text in p.get_text()):
                        ptag=p.get_text()
                resultPages.append({'A':currentPage,'P':ptag,'H':htag})
                                

            if 'https://' in startPage:
                links=soup.findAll('a', attrs={'href': re.compile("^https://|^/")})
            else:
                links=soup.findAll('a', attrs={'href': re.compile("^http://|^/")})


            #if depth
            #and addedlinks<self.searchDepth
            #iterate through links
            for link in links:
                linkText=link.get('href')
                linkText=self.correctURL(linkText, currentPage) #correct relative URLs

                if(text in link.get_text() ):
                    l={'A':linkText,'H':link.get_text()}
                    if l not in resultPages:
                        resultPages.append(l)

                if (linkText not in unVisitedLinks 
                    and (startPage in linkText or linkText.startswith("/")) # if link does not point to other sites
                    and '/ads/' not in linkText # not an advertiseing link
                    and len(link.get('href'))>0
                    and 'facebook' not in linkText):  #not an empty link 

                    unVisitedLinks.append(linkText)
            depth+=1

            
            visitedLinks.append(currentPage)
        return(resultPages)

