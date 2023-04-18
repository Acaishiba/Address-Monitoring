import requests
import csv
import os.path

# 设置请求的URL和参数
url = 'https://polkadot.api.subscan.io/api/scan/transfers'
api_key = 'xxxxxxxxxxxxxx'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key
}

# 读取CSV文件
filename = 'address_list3.csv'

# 检查文件是否存在，如果不存在，则创建新文件并写入表头
if not os.path.isfile(filename):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['block_mark', 'address', 'balance_base','rate_base'])



address_set = set()

if os.path.exists(filename):
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        # 跳过表头
        next(reader)
        # 读取已经存在的地址
        for row in reader:
            address_set.add(row[0])


# 打开CSV文件进行追加写入
with open(filename, mode='a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # 循环查询50页数据
    for page in range(1, 5):
        # 设置区块范围参数
        params = {'row': 25, 'page': page, 'from_block':14000000,'to_block':14001800, 'direction': 'all'}
        # 发送请求并获取响应
        response = requests.post(url, json=params, headers=headers)
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
                            # 新地址写入第二列，其它列填充空值
                            writer.writerow(['',to_address,'10','0'])
                            address_set.add(to_address)
            else:
                print('No transfers found in response')
                break
        else:
            print('Query failed for page', page)
            break
