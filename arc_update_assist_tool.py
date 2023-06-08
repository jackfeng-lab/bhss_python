import os
import csv
import shutil

block_d1 = []
block_d2 = []
diff_flag = False
delete_flag = False
add_flag = False
number_of_table_1 = 0
number_of_table_2 = 0
table_name = ""
dependency_1_path = "dependency_1.csv"
dependency_2_path = "dependency_2.csv"

#读取dependency 1 中的table数量
def read_table_1_count():
    global number_of_table_1

    with open("dependency_1.csv",'r',encoding='UTF-8') as load_input_1:
        ereader_1 = csv.reader(load_input_1)
        for row_list in ereader_1:
            for i in row_list:
                if i[0:5] == "Table":
                    number_of_table_1 += 1
        load_input_1.close()
    return number_of_table_1

#读取dependency 2 中的table数量
def read_table_2_count():
    global number_of_table_2

    with open("dependency_2.csv",'r',encoding='UTF-8') as load_input_2:
        ereader_2 = csv.reader(load_input_2)
        for row_list in ereader_2:
            for i in row_list:
                if i[0:5] == "Table":
                    number_of_table_2 += 1
        load_input_2.close()
    return number_of_table_2

#读取dependency 1中的一个表
def read_block_d1(roll_num, path):
    global block_d1
    global table_name
    flag = False
    local_seek_1 = 0
    with open(path,'r',encoding='UTF-8') as load_input_1:
        ereader_1 = csv.reader(load_input_1)
        for row_list in ereader_1:
            for i in row_list:
                if i[0:5] == "Table":
                    flag = True
                    local_seek_1 += 1
                    block_d1.clear()
                    if local_seek_1 == roll_num:
                        table_name = i[6:]
                        # print (table_name, local_seek_1)

                if row_list[0] == "" and local_seek_1 == roll_num:
                    return
            if flag == True and local_seek_1 == roll_num:
                block_d1.append(row_list)
        load_input_1.close()

#读取dependency 2中的一个表
def read_block_d2(path):
    global block_d2
    global table_name
    flag = False

    with open(path,'r',encoding='UTF-8') as load_input_2:
        ereader_2 = csv.reader(load_input_2)
        for row_list in ereader_2:
            for i in row_list:
                if i[6:] == table_name:
                    # print (table_name + "已找到")
                    flag = True
                    block_d2.clear()
                if row_list[0] == "" and flag == True:
                    # print (block_d2)
                    return flag
            if flag == True:
                block_d2.append(row_list)
        load_input_2.close()
    return flag

#检查表1 和表2是否存在差异
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

#如果存在任何差异，输出整张Table
def write_to_file(f1, block):
    global diff_flag
    global delete_flag
    global add_flag
    null_line = []

    writer = csv.writer(f1)
    if diff_flag is True:
        for line in block:
            writer.writerow(line)
        writer.writerow(null_line)
        diff_flag = False
    
    if delete_flag is True:
        writer.writerow(['***----------DELETE----------***', '', ''])
        for line in block:
            writer.writerow(line)
        writer.writerow(null_line)
        delete_flag = False
    
    if add_flag is True:
        writer.writerow(['***----------NEW ADD----------***', '', ''])
        for line in block:
            writer.writerow(line)
        writer.writerow(null_line)
        add_flag = False

#复制变更组件的xml文件到新目录下
def copy_diff_xml():
    global diff_flag
    global table_name
    global delete_flag
    global add_flag

    if diff_flag is True or add_flag is True:
        # print (table_name[1:-11])
        if os.path.exists("Diff//" + table_name[1:-11]):
            shutil.rmtree("Diff//" + table_name[1:-11])

        if not os.path.exists(table_name[1:-11]):
            os.makedirs("Diff//" + table_name[1:-11])
        
        shutil.copyfile("Output//Dependency " + table_name[1:-11] + ".xml", "Diff//" + table_name[1:-11] +"//Dependency " + table_name[1:-11] + ".xml")
        shutil.copyfile("Output//Interface " + table_name[1:-11] + ".xml", "Diff//" + table_name[1:-11] +"//Interface " + table_name[1:-11] + ".xml")
    
    if delete_flag is True:
        if os.path.exists("Diff//" + table_name[1:-11]):
            shutil.rmtree("Diff//" + table_name[1:-11])

        if not os.path.exists(table_name[1:-11]):
            os.makedirs("Diff//" + table_name[1:-11])
        
        with open("Diff//" + table_name[1:-11] + "//please delete this xml.txt",'w') as warning:
            warning.close()

#运行区域
if __name__== "__main__" :
    roll_num = 1
    ret = 0

    f1 = open("diff_point.csv", 'w', newline='',encoding='UTF-8')
    number_of_table_1= read_table_1_count()
    number_of_table_2= read_table_2_count()

    #有模块删除
    if number_of_table_1 > number_of_table_2:
        print ("有模块删除")
        for n in range(number_of_table_1):
            read_block_d1(roll_num, dependency_1_path)
            ret = read_block_d2(dependency_2_path)
            if ret == False:
                delete_flag = True
                copy_diff_xml()
                write_to_file(f1, block_d1)
            else:
                check_diff_point()
                copy_diff_xml()
                write_to_file(f1, block_d2)

            roll_num += 1
    #有模块增加
    elif number_of_table_1 < number_of_table_2:
        print ("有模块增加")
        for n in range(number_of_table_2):
            read_block_d1(roll_num, dependency_2_path)
            ret = read_block_d2(dependency_1_path)
            if ret == False:
                add_flag = True
                copy_diff_xml()
                write_to_file(f1, block_d1)
            else:
                check_diff_point()
                copy_diff_xml()
                write_to_file(f1, block_d2)

            roll_num += 1
    #无模块增删
    else:
        print ("无模块增删")
        for n in range(number_of_table_1):
            read_block_d1(roll_num, dependency_1_path)
            read_block_d2(dependency_2_path)
            roll_num += 1
            check_diff_point()
            copy_diff_xml()
            write_to_file(f1, block_d2)
    
    f1.close()