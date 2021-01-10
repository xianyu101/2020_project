#0 导入项目所需模块
import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm

class CoronaVirusSpider(object):

    def __init__(self):
        self.home_url='https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def get_content_from_url(self,url):
        
        #1.通过requests从url处获得字符串数据

        # 发送请求 获取疫情首页
        response = requests.get(url)

        return response.content.decode()

    def parse_home_page(self,home_page):

        #2. 解析获取的数据并将其从json格式转换为python类型

        # 从疫情首页中提取一日内各国疫情数据
        soup=BeautifulSoup(home_page,'lxml')
        script = soup.find(id='getListByCountryTypeService2true')
        text=script.string
        #print(text)

        # 获取json字符串
        json_str=re.findall(r'\[.+\]',text)[0]
        #print(json_str) 

        # json -> python
        data=json.loads(json_str)
        #print(data)

        return data

    
    
    def save(self,data,path):

        #3.保存数据

        # 以json格式保存一日内各国疫情数据
        with open(path,'w',encoding='utf-8') as fp:
            json.dump(data,fp,ensure_ascii=False)

    def crawl_last_day_corona_virus(self):

        #爬取一日内各国疫情信息
        # 1.-2.-3.

        home_page = self.get_content_from_url(self.home_url)
        last_day_corona_virus = self.parse_home_page(home_page)
        self.save(last_day_corona_virus,'data/last_day_corona_virus.json')
    
    def crawl_corona_virus(self):

        #采集自xx日期以来的各国疫情数据

        with open(r'data\last_day_corona_virus.json',encoding='utf-8') as fp:
            last_day_corona_virus = json.load(fp)
        #print(last_day_corona_virus)


        corona_virus = []


        for country in tqdm(last_day_corona_virus,'采集国际疫情信息'):
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
            #print(statistics_data)
            for one_day in statistics_data:
                one_day['provinceName'] = country['provinceName']
                one_day['countryShortCode'] = country['countryShortCode']
            #print(statistics_data)
            corona_virus.extend(statistics_data)
        self.save(corona_virus,'data/corona_virus.json')
    
    def crawl_last_day_corona_virus_of_china(self):
        
        #采集一日内国内疫情数据

        home_page = self.get_content_from_url(self.home_url)

        soup=BeautifulSoup(home_page,'lxml')
        script = soup.find(id='getAreaStat')
        text=script.string
        #print(text)

        # 获取json字符串
        json_str=re.findall(r'\[.+\]',text)[0]
        #print(json_str) 

        # json -> python
        data=json.loads(json_str)

        self.save(data,'data/last_day_corona_virus_of_china.json')

    def crawl_corona_virus_of_china(self):
        
        #采集自xx日的全国各省疫情

        with open('data/last_day_corona_virus_of_china.json',encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)

        
            corona_virus = []


        for country in tqdm(last_day_corona_virus_of_china,'采集国内疫情信息'):
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
            #print(statistics_data)
            for one_day in statistics_data:
                one_day['provinceName'] = country['provinceName']
                
            #print(statistics_data)
            corona_virus.extend(statistics_data)
            #print(corona_virus)
        self.save(corona_virus,'data/corona_virus_of_china.json')


    def run(self):
        #self.crawl_last_day_corona_virus()
        self.crawl_corona_virus()
        #self.crawl_last_day_corona_virus_of_china()
        self.crawl_corona_virus_of_china()


if __name__=='__main__':
    spider = CoronaVirusSpider()
    spider.run()




