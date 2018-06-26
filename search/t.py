from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from Core import Crawler

print(Crawler().search('تعرفه آگهی')[0]['A']);