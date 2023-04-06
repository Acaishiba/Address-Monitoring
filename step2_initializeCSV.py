import pandas as pd
import sys

input_filename = 'address_list3.csv'

if __name__ == "__main__":
    # 读取传入的参数
    arg1 = sys.argv[1]

    # 读取CSV文件为DataFrame对象
    df = pd.read_csv(input_filename)


    # 打印原始数据
    print(df)

    # 将Alex的年龄设为18
    df.at[0, 'block_mark'] = arg1

    # 将修改后的数据写回CSV文件
    df.to_csv(input_filename, index=False)

    # 打印修改后的数据
    print(df)
