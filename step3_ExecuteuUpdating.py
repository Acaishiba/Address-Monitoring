import requests
import csv
import os.path
import pandas as pd
from datetime import datetime, timedelta
import sys



# 设置请求的URL和参数
url = 'https://polkadot.api.subscan.io/api/scan/transfers'
url_v2 = 'https://polkadot.api.subscan.io/api/v2/scan/search'
url3 = 'https://polkadot.api.subscan.io/api/scan/metadata'
api_key1 = '4a33096d8d0d4b52acfe6151fec5cb34'
api_key2 = '67c0f369625748d7b6d9d372019cbeac'
headers1 = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key1
}

headers2 = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key2
}
input_filename = 'address_list3.csv'

# 读取CSV文件为DataFrame对象
df = pd.read_csv(input_filename)
# 获取block_mark列的第一个值
block_mark = df.iloc[0].at['block_mark']
block_mark=int(block_mark)
print('from_block is',block_mark)

#获取当前区块高度
response = requests.post(url3, headers=headers1)
response_get_num = response.json()
blocknum_now = response_get_num['data']['blockNum']
blocknum_now = int(blocknum_now)
print('当前区块高度为:', blocknum_now)

#判断目前区块区间够不够一次执行程序
if block_mark+1800 >= blocknum_now:
    sys.exit('block is not enough')    #不够就退出
else:
    print('block is enough to continue')  #够就继续执行后续

# 读取CSV文件
filename = input_filename
# 读取CSV文件为DataFrame对象

# 检查文件是否存在，如果不存在，则创建新文件并写入表头
if not os.path.isfile(filename):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['block_mark', 'address', 'balance_base','rate_base'])



address_set = set()

if os.path.exists(filename):
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # 跳过表头
        next(reader)
        # 读取已经存在的地址
        for row in reader:
            address = row[1]
            address_set.add(address)

###########一下为测试环节#########

# 设置时间格式和当前时间
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 读取CSV文件
df = pd.read_csv(input_filename)

# 获取倒数第二列表头
second_last_col = df.columns[-2]

time_col = f'{current_time}_balance'
rate_col = f'{current_time}_ChangeRate'
# 判断是否存在 0 值
has_zero = (df[second_last_col] == 0).any()

# 遍历每个地址并查询余额
for index, row in df.iterrows():
    old_address = row['address']

    params_old_adress = {'key': old_address}
    response_old_adress = requests.post(url_v2, json=params_old_adress, headers=headers2)
    response_old_adress_data = response_old_adress.json()
    recent_old_address_balance = float(response_old_adress_data['data']['account']['balance'])
    df.loc[index, time_col] = recent_old_address_balance   

    # 计算并填充 rate_col 列，加入分母为0的判断
    if has_zero and df.loc[index, second_last_col] == 0:
        # 分母为 0 的情况
        df.loc[index, rate_col] = 0  # 或者 df.loc[index, rate_col] = np.nan
    else:
        # 分母不为 0 的情况
        df.loc[index, rate_col] = '{:.2%}'.format((df.loc[index, time_col] / df.loc[index, second_last_col] - 1))
    



# 以下为解决备用办法#######
# 遍历每个地址并查询余额
#for index, row in df.iterrows():
#    old_address = row['address']

#    params_old_adress = {'key': old_address}
#    response_old_adress = requests.post(url_v2, json=params_old_adress, headers=headers1)
#    response_old_adress_data = response_old_adress.json()
#    recent_old_address_balance = float(response_old_adress_data['data']['account']['balance'])
#    df.loc[index, time_col] = recent_old_address_balance   

    # 计算并填充 rate_col 列，加入分母为0的判断
#    if df.loc[index,second_last_col] != 0;
#        value = (df.loc[index,time_col]/df,loc[index,second_last_col]-1)* 100
#        value = value.apply(lambda x: '{:.2%}'.format(x))
#    else:
#         value = 0
        
#        df.loc[index, rate_col] = value




# 将修改后的数据写回CSV文件
df.to_csv(input_filename, index=False)


    

# 打开CSV文件进行追加写入
with open(filename, mode='a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # 循环查询50页数据
    for page in range(1, 24):
        # 设置区块范围参数
        params = {'row': 25, 'page': page, 'from_block':block_mark,'to_block':block_mark+1800, 'direction': 'all'}
        # 发送请求并获取响应
        response = requests.post(url, json=params, headers=headers1)
        data = response.json()
        print(data)

        # 判断是否查询成功
        if data['code'] == 0:
            if data['data']['transfers'] is not None:
            # 写入数据
                for transfer in data['data']['transfers']:
                    if float(transfer['amount']) > 1000:
                        to_address = transfer['to']
                        print(to_address)
                        if to_address not in address_set:
                            #开始查询新增预新增地址的余额
                            params = {'key': to_address}
                            response_bal = requests.post(url_v2, json=params, headers=headers2)
                            response_bal_data = response_bal.json()
                            print(response_bal_data)
                            to_address_balance=float(response_bal_data['data']['account']['balance'])
                            # 新地址写入第二列，余额写入第三列，第一/四列留空
                            writer.writerow(['',to_address,to_address_balance,0])
                            address_set.add(to_address)
            else:
                print('No transfers found in response')
                break
        else:
            print('Query failed for page', page)
            break

# 读取CSV文件为DataFrame对象
df = pd.read_csv(input_filename)


# 打印原始数据
print(df)

# 重置block_mark
df.at[0, 'block_mark'] = block_mark+1800
print('refresh block done ,block is ',block_mark+1800)
# 将修改后的数据写回CSV文件
df.to_csv(input_filename, index=False)

# 打印修改后的数据
print(df)
