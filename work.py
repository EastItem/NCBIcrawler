import requests
import pandas as pd
from lxml import html

def get_data(page,start=1,end=10,keyword='p53'):

 df = pd.DataFrame()  # 存储数据

 each_url='https://pubmed.ncbi.nlm.nih.gov/?term='+keyword+'%5BTitle%5D&filter=datesearch.y_1&page=' + str(page)
 header={
 'Referer':'https://www.ncbi.nlm.nih.gov/',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
 }
 res = requests.get(each_url, headers=header)
 tree = html.fromstring(res.content)
 res.close()

 if page == 1:
  strs = '//*[@id="search-results"]/section/div[1]/div/article'  #由于第一页和其他页XPATH地址不同，所以要开两个头
 else:
  strs = '//*[@id="search-results"]/section/div[2]/div/article'


 for i in range(start,end+1): #一页有11条数据

  #获取标题
  title1 =tree.xpath(strs + '[{}]/div[2]/div[1]/a/text()'.format(i))
  charu(title1) #由于获取的信息都是缺失了关键字的，所以要在两两之间插入关键字
  title=''.join(title1).strip() # 换成str，并去除前后空格，下类同

  #获取作者
  author=tree.xpath(strs + '[{}]/div[2]/div[1]/div[1]/span[1]/text()'.format(i))[0].split(',')[0]

  #获取日期
  infrom=tree.xpath(strs + '[{}]/div[2]/div[1]/div[1]/span[3]/text()'.format(i))[0]
  year=infrom.split('.')[1].split(';')[0].split(':')[0].strip()

  #发表期刊
  period=infrom.split('.')[0].strip()

  #存储在dataframe
  new=pd.DataFrame({'title':title,'author':author,'year':year,'period':period},index=[1])
  df=df.append(new,ignore_index=True)

 return df


def get_total(keyword='p53'):
 url = 'https://pubmed.ncbi.nlm.nih.gov/?term='+keyword+'%5BTitle%5D&filter=datesearch.y_1&page=1'
 header = {
  'Referer': 'https://www.ncbi.nlm.nih.gov/',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
 }
 res = requests.get(url, headers=header)
 tree = html.fromstring(res.content)
 res.close()
 # 获取总共结果数：
 total = int(tree.xpath('//*[@id="search-results"]/div[2]/div[1]/span/text()')[0].replace(',', ''))
 return total

def charu(s):
 for i in range(1, len(s)):  # i为插入次数
  s.insert(2 * i - 1, 'p53')


