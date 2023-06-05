import os
import csv

block_d1 = []
block_d2 = []
diff_flag = False

def read_block_d1(roll_num_1):
    global block_d1
    flag = False
    local_seek_1 = 0
    with open("dependency_1.csv",'r',encoding='UTF-8') as load_input_1:#打开要读取的csv文件进行只读操作
        ereader_1 = csv.reader(load_input_1) #用reader函数读入文件指针
        for row_list in ereader_1:
            for i in row_list:
                if i[0:5] == "Table":
                    flag = True
                    local_seek_1 += 1
                    block_d1.clear()
                if row_list[0] == "" and local_seek_1 == roll_num_1:
                    flag = False
                    print ("1")
                    print (block_d1)
                    return
            if flag == True and local_seek_1 == roll_num_1:
                block_d1.append(row_list)
        load_input_1.close()

def read_block_d2(roll_num_2):
    global block_d2
    flag = False
    local_seek_2 = 0
    with open("dependency_2.csv",'r',encoding='UTF-8') as load_input_2:#打开要读取的csv文件进行只读操作
        ereader_2 = csv.reader(load_input_2) #用reader函数读入文件指针
        for row_list in ereader_2:
            for i in row_list:
                if i[0:5] == "Table":
                    flag = True
                    local_seek_2 += 1
                    block_d2.clear()
                if row_list[0] == "" and local_seek_2 == roll_num_2:
                    flag = False
                    print ("2")
                    print (block_d2)
                    return
            if flag == True and local_seek_2 == roll_num_2:
                block_d2.append(row_list)
        load_input_2.close()

def check_diff_point():
    global block_d1
    global block_d2
    global diff_flag

    for line in block_d2:
        if line not in block_d1:
            diff_flag = True
            return
    for line in block_d1:
        if line not in block_d2:
            diff_flag = True
            return

def write_to_file(f1):
    global diff_flag
    global block_d2
    null_line = []
    writer = csv.writer(f1)
    if diff_flag is True:
        for line in block_d2:
            writer.writerow(line)
        writer.writerow(null_line)
        diff_flag = False
        print ("ok")

#运行区域
if __name__== "__main__" : 
    roll_num_1 = 0
    roll_num_2 = 0
    f1 = open("diff_point.csv", 'w', newline='',encoding='UTF-8')

    for n in range(145):
        read_block_d1(roll_num_1)
        read_block_d2(roll_num_2)
        roll_num_1 += 1
        roll_num_2 += 1
        check_diff_point()
        write_to_file(f1)

    f1.close()