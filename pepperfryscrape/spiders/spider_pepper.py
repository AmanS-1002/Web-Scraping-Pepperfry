import scrapy
import json
import os
import requests
#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
class pepperfryspider(scrapy.Spider):
    name = 'pepperfry_spider'
    BASE_DIR='./Pepperfry_data'
    MAX_CNT=20

    def start_requests(self):
        #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        base_url='https://www.pepperfry.com/site_product/search?q='
        items=['chair','gaming chair','sofa 2 seater']
        urls=[]
        dir_names = []
        for i in items:
            string_q='+'.join(i.split(' '))
            dir_name='-'.join(i.split(' '))
            dir_names.append(dir_name)
            urls.append(base_url+string_q)
            dir_path=self.BASE_DIR+dir_name
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        # print('asdfghjkl')
        # print(urls)
        for i in range(len(urls)):
            d={
                "dir_name":dir_names[i]
            }
            resp=scrapy.Request(url=urls[i],callback=self.parse,dont_filter=True)
            resp.meta['dir_name']=dir_names[i]
            yield resp

    def parse(self,response,**meta):
        product_list=response.css('div.clipCard__hd')[:5]
        url_list=[x.css('a::attr(href)').get() for x in product_list]
        for url in url_list:
            resp=scrapy.Request(url=url,callback=self.parser,dont_filter=True)
            resp.meta['dir_name']=response.meta['dir_name']
            yield resp

    def parser(self,response,**meta):
        img_urls=response.css('div.vipGallery__thumb-each a::attr(href)').getall()
        item_name=response.css('h1::text').get()
        item_name='_'.join(item_name.split())
        Cat_name=response.meta['dir_name']
        item_dir_url=os.path.join(self.BASE_DIR,os.path.join(Cat_name,item_name))
        if not os.path.exists(item_dir_url):
            os.makedirs(item_dir_url)
        d={
            'item_name':item_name,
        }
        with open(os.path.join(item_dir_url,'metadata.txt'),'w') as f:
            json.dump(d,f)

        for i,img_url in enumerate(img_urls):
            r=requests.get(img_url)
            with open(os.path.join(item_dir_url,'image_{}.jpg'.format(i)),'wb') as f:
                f.write(r.content)
        
        yield d

        
        