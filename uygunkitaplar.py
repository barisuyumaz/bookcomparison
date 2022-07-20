import requests
from bs4 import BeautifulSoup
import pandas as pd
from helperfuncs import *

#İlk olarak DR sitesi için yapıyorum

df = pd.DataFrame(columns=["kitap_isim","yazar","yayınevi","fiyat"])

def sitelerde_kitaplari_ara(search):
	kitap_ismi = for_link(search)
	dr_kitap = "https://www.dr.com.tr/search?ActiveCategoryId=10001&Q="+kitap_ismi+"&redirect=search&MainCategoryId=0"
	#bu linkte kitap dışındaki ürünler çıkmıyor ve e-kitaplarda çıkmıyor sadece fiziksel kitaplar
	#örnek tam hali
	#https://www.dr.com.tr/search?ActiveCategoryId=10001&Q=B%C3%B6yle%20Buyurdu%20Zerd%C3%BC%C5%9Ft&redirect=search&MainCategoryId=0

	veri = soup_content(dr_kitap).find_all('div',{'class':'facet__group-content-list js-facet-list-persons'})[0]#yazar için
	yazar = veri.find_all('span',{'class':'facet__checkbox-text'})[0].text #en üstteki yazar
	#Yazar kısmındaki en üst yazarı seçiyoruz şimdilik / Sadece yazar seçili link(dil seçili değil)
	#dr_kitap_yazar = "https://www.dr.com.tr/search?ActiveCategoryId=10001&MainCategoryId=0&Page=1&Q="+kitap_ismi+"&redirect=search&Person[0]="+yazar

	#dil şimdilik sadece türkçe kalsın
	dr_kitap_yazar_dil = "https://www.dr.com.tr/search?ActiveCategoryId=10001&MainCategoryId=0&Page=1&Person[0]="+for_link(yazar)+"&Q="+for_link(kitap_ismi)+"&redirect=search&Lang[0]=Türkçe"
	#print(dr_kitap_yazar_dil)
	

	soup1 = soup_content(dr_kitap_yazar_dil)
	#aramanın kaç sayfa sürdüğünü sorgula, kaç li var?
	datali = soup1.find('ul',{'class':'pager pager-list dr-flex pagination js-facet-list-pagination flex-wrap'}).find_all("li")

	#sayfa sayısı 1
	if(len(datali)==1):#len(datali) sadece 1 mi yoksa daha fazlamı onu ölçüyor	
		kitaplari_gez(soup1,yazar,df)


	#sayfa sayısı 1'den fazla
	else:
		counts_of_li = int(datali[-2].find('a',{'class':'js-facet-link-pagination'})['data-number'])
		kitaplari_gez(soup1,yazar,df)

		for i in range(1,counts_of_li):
			link = for_linkpage(dr_kitap_yazar_dil,i+1)
			soup2 = soup_content(link)
			kitaplari_gez(soup2,yazar,df)


	


	#print(df)
	print(df.sort_values(by=['fiyat']))

	#print(df[df.duplicated()])
	#tekrar eden aynı satır var mı diye kontrol

#Bazı isimleri ararttımı solda yazar seçeneği çıkmadığı için, hata veriyor, orayı try except ile değiştiircez