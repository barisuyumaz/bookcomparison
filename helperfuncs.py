import requests
from bs4 import BeautifulSoup

#DR web-site functions
def kitaplari_gez(soupcode, author, addtodf):#dr için
	veri1 = soupcode.find_all('div',{'class':'prd-content-wrapper'})#o sayfadaki tüm kitapların bilgileri var
	
	for i in veri1:
		book_name = i.a['title']

		book_price = i.find('div',{'class':'prd-price'}).text
		bkprc_index = book_price.index(',')
		book_price_float = float(book_price[bkprc_index-2:bkprc_index+3].replace(",","."))

		book_publisher = i.find('a',{'class':'prd-publisher'})['title']

		addtodf.loc[len(addtodf)]=[book_name, author, book_publisher, book_price_float]
#-------

#General Functions
def for_link(name):#genel func
	return name.replace(" ","%20")

def for_linkpage(link,page): #linki gir, hangi sayfaya ulaşmak istediğini yaz, şu anlık dr içni
	index_of_page = link.index("Page")+5
	return link[:index_of_page]+str(page)+link[index_of_page+1:]

def soup_content(link):#genel func
	icerik = requests.get(link).content
	soup = BeautifulSoup(icerik,"html.parser")
	return soup
#-------