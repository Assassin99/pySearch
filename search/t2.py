from bs4 import BeautifulSoup
import requests 

def TextExistsInPage(soup,text):
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

page = requests.get("https://www.mehrnews.com/news/2409272/")
soup = BeautifulSoup(page.content,'html.parser')
print(TextExistsInPage(soup,"تعرفه آگهی"))
