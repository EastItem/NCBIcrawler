import pandas as pd
from work import get_data,get_total
from tqdm import tqdm #进度条
data=pd.DataFrame()
total=get_total()
total_page=(total//10)+1
last=total%10
for i in tqdm(range(1,total_page+1),ncols=100,desc='总共'+str(total_page)+'页',unit='页',colour='green',mininterval=0.01):
 if i == total_page:
     data=data.append(get_data(i,end=last),ignore_index=True)
 else:
     data = data.append(get_data(i), ignore_index=True)

data.to_csv('data.csv')
print('over!!!!!')
