'''
Created on 2017年3月22日

@author: HL
'''
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

class ready_to_get(object):
    
    '''
    Pass as many keword as passible to get the database
    Such as: 
    ready_to_get.get_current_stuff() to get the ongoing sell
    ready_to_get.()
    '''
    
    url_of_PChome = ''
    url_of_yahoo = ''
    url_of_momo = ''
    sales_info = {}
    info_of_pchome = {}
    info_of_momo = {}
    info_of_myfone = {}
    
    def __init__(self,*args, **kwargs):
        #整點特賣
        self.url_of_PChome = 'http://24h.pchome.com.tw/onsale/v3/{0}/#!3c.htm'
        self.url_of_momo = 'https://www.momoshop.com.tw/ajax/promotionEvent_CustExclbuy.jsp'                                             
        
        self.url_of_yahoo = 'https://tw.buy.yahoo.com/bestbuy/'
        self.url_of_rakuten = 'http://www.rakuten.com.tw/event/supersale/?gid=dc5592411a4812b4d49c97c27022d010&scid=ichannel_1604'
        print('args=', args)
        print('kwargs=', kwargs)
    def get_PCHOME_timelimite(self):
        # coding=utf-8
        #reg = requests.get(self.url_of_PChome) # get url in html
        driver = webdriver.Chrome(executable_path="D:\GitHub\Compare\Compare\chromedriver") # drive by Chrome
        today = datetime.datetime.today()
        url_for_search = self.url_of_PChome.format(today.strftime("%Y%m%d"))
        driver.get(url_for_search)
        reg = driver.page_source
        driver.close()
        soup = BeautifulSoup(reg,"lxml") #use lxml as Parser
        #make sure there is on-sale
        Get_on_sale = soup.find_all("dl", class_ = "site_onsale")
        times = [10,15,21]
        if Get_on_sale != []:
            # get the sales data
            Get_sale_url = soup.select('dl[class=site_onsale] > dd')
            for count,item in enumerate(Get_sale_url):
                pchome_data = []
                #get price
                Get_price = item.select('span[class=value]')[0].text
                pchome_data.append(Get_price)
                #get decription
                Get_decr_info = item.select('h5[class=prod_name] > a')[0].text
                pchome_data.append(Get_decr_info)
                # picture address
                Get_img_info = item.select('a[class=prod_img] > img')
                Get_img_url = Get_img_info[0]['src']
                url_of_pic = "http:" + Get_img_url
                pchome_data.append(url_of_pic)
                #saving name
                pic_name = './Pics/PCHOME_' + str(count) +'.jpg'
                #save picture
                r = requests.get(url_of_pic)
                with open(pic_name,'wb') as f:
                    f.write(r.content)
                #get url
                Get_url_info = item.select('a[class=prod_img]')[0]['href']
                pchome_data.append(Get_url_info)
                #save all information
                self.info_of_pchome[times[count]]= pchome_data
            print(self.info_of_pchome)
                
        else:
            print("Empty")
    def get_momo_timelimite(self):
        #setup your header and cookies of browser, 
        #momo will block any request without header
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
        cookies = {'_ts_id':  '999999999999999999', }
        reg = requests.get(self.url_of_momo, headers=headers, cookies=cookies)
        soup = BeautifulSoup(reg.text,"lxml") #use lxml as Parser
        #sale times
        times = [8,12,14,20,24]
        
        '''
        Get_sale_times = soup.select('div[class=period] > span')
        today = datetime.datetime.today()
        today = today.strftime("%m/%d")
        for item in Get_sale_times:
            time_for_sell = item.text.split("~"+today+' ')
            times.append(time_for_sell[1])
        '''
        #price
        Get_sale_img = soup.select('li[class=box1]')
        momo_data = []
        for count,box_item in enumerate(Get_sale_img,1):
        #get price
            momo_data.append(box_item.select('div[class=price]')[0].text)
        #get describtion
            desc = box_item.select('#gdsBrand_1')[0].text+ " " + box_item.select('#gdsName_1')[0].text
            momo_data.append(desc)
        #get picture
            #src
            url_of_pic = box_item.select('#nowPImg_1')[0]['src']
            momo_data.append(url_of_pic)
            #save picture
            pic_name = "./Pics/momo_" + str(count) + ".jpg"
            r = requests.get(url_of_pic)
            with open(pic_name,'wb') as f:
                f.write(r.content)
        #get url
            momo_data.append(box_item.select('#gdsHref_1')[0]['href'])   
            if count % 6 == 0:
                # save all the information
                self.info_of_momo[times[int(count/6)-1]]= momo_data
                momo_data = []
        print(self.info_of_momo)
        
    def get_yahoo_timelimite(self):
        #setup your header and cookies of browser, 
        #momo will block any request without header
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
        cookies = {'_ts_id':  '999999999999999999', }
        reg = requests.get(self.url_of_yahoo, headers=headers, cookies=cookies)
        soup = BeautifulSoup(reg.text,"lxml") #use lxml as Parser
        all_items = soup.select('.ui-product-list-s')
        print(soup)
    
    def get_rakuten_timelimite(self):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
        cookies = {'_ts_id':  '999999999999999999', }
        reg = requests.get(self.url_of_rakuten, headers=headers, cookies=cookies)
        soup = BeautifulSoup(reg.text,"lxml") #use lxml as Parser
        #sale times
        times = [10,12,14,15,17,18,19,20,21,22]       
        #get price
        all_items = soup.select('.ui-product-list-s')
        for item in all_items:
            print(item.select('img[class=cate-img]'))
        
        
if __name__ == '__main__':
    get_url = ready_to_get()  
#get_url.get_PCHOME_timelimite()  
#get_url.get_momo_timelimite()  

