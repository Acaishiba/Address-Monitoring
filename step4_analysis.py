import csv

input_file = "address_list3.csv"
output_file = "analysis.csv"

with open(input_file, "r") as f, open(output_file, "w", newline="") as out_f:
    reader = csv.reader(f)
    writer = csv.writer(out_f)

    # 读取文件头并写入到输出文件中
    header = next(reader)
    writer.writerow(["address", "balance_base", "second_last_col"])

    # 获取倒数第二列、adress_base列和adress列数据，并写入到输出文件中
    for row in reader:
        data = (row[header.index("address")], row[header.index("balance_base")], row[-2])
        writer.writerow(data)

print("输出完成")
