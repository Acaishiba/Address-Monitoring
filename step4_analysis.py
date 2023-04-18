import csv

input_file = "address_list3.csv"
output_file = "analysis_1.csv"

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


# 读取csv文件
with open(output_file, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# 计算比值
for row in rows[1:]:  # 从第二行开始遍历，避免操作列名
    balance_base = float(row[1])
    second_last_col = float(row[2]) if row[2] else 0  # 如果row[2]为空，second_last_col为0，否则为row[2]转换后的浮点数
    if balance_base != 0:
        ratio = (second_last_col / balance_base - 1) * 100
        ratio = f"{ratio:.2f}%"

    else:
        ratio = 'N/A'
    row.append(ratio)

# 写入新文件
with open('analysis_final.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)


print("输出完成")
