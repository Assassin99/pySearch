from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
class Crawler:
    #sites to search text in in:
    #sites=['https://www.mehrnews.com/','http://www.irna.ir/','http://www.farsnews.com/','https://www.isna.ir/']    #for storing links to visit later
    sites=[]
    unVisitedLinks =[]
    visitedLinks =[]    
    resultPages=[]
    links = []
    depthLimit=0

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
        self.depthLimit=int(depth)
        self.sites.append(site)

        for startPage in self.sites:
            depth=0
            self.unVisitedLinks.append(startPage)
            print("\n Searching in "+startPage+" :")

            while(len(self.unVisitedLinks)!=0):
                if depth>self.depthLimit:
                    break

                currentPage=self.unVisitedLinks.pop()
                if currentPage in self.visitedLinks:
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
                    self.resultPages.append({'A':currentPage,'P':ptag,'H':htag})
                                    

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
                        if l not in self.resultPages:
                            self.resultPages.append(l)

                    if (linkText not in self.unVisitedLinks 
                        and (startPage in linkText or linkText.startswith("/")) # if link does not point to other sites
                        and '/ads/' not in linkText # not an advertiseing link
                        and len(link.get('href'))>0
                        and 'facebook' not in linkText):  #not an empty link 

                        self.unVisitedLinks.append(linkText)
                depth+=1

                
                self.visitedLinks.append(currentPage)
        return(self.resultPages)
        #return(self.visitedLinks)

