"""
1.查看当前那些端口被使用，并且每个端口对应的Customer端口是多少，且可以显示备注
2.通过输出提示引导用户输入地址端口等信息，然后运行程序。
3.要有一个进程池，来管理所有的连接，每个连接都是一个进程，
4.应该是每次使用的时候才会运行，创建完连接线程后，就直接退出。
"""
import atexit
import os
from io import TextIOWrapper
from time import sleep
import platform
from typing import List
import subprocess

DATA_SAVE_FILE_PATH = "./.save_information.data"
START_MASTER_COMMAND = "nohup ~/.pyenv/shims/python3 master.py -m 0.0.0.0:{master_port} -c 0.0.0.0:{customer_port} " \
                       "> nohup.out 2>&1 &"
data_save_file = None


@atexit.register
def clean_func():
    """
    退出的时候关闭文件
    :return:
    """
    if data_save_file is not None:  # type:
        if not data_save_file.closed:
            data_save_file.flush()
            data_save_file.close()


class DataType():
    message = None  # 对应的程序的备注，是什么用途等
    process_pid = None  # 对应的程序的PID，用来关闭程序
    master_ip = None  # master 的IP
    master_port = None  # master的Port
    customer_port = None  # customer监听的端口

    def __init__(self, process_pid, customer_port, master_port, message="未知", master_ip='0.0.0.0', ):
        self.process_pid = process_pid
        self.customer_port = customer_port
        self.master_port = master_port
        self.message = message
        self.master_ip = master_ip

    def __str__(self):
        return "\t".join([str(i) for i in self.__dict__.values()])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.master_port == self.master_port and other.customer_port == self.customer_port


def save2file(data: DataType) -> None:
    """
    将传入的DataType对象的信息存入文件
    :param data: 要存入文件的对象
    :return:
    """
    data_save_file.write(data.__str__() + "\n")
    data_save_file.flush()


def file2data() -> List[DataType]:
    data_save_file.seek(0, 0)
    data_type_list = []
    for data in data_save_file.readlines():
        propertys = data.split("\t")
        obj = DataType(propertys[0], propertys[1], propertys[2], propertys[3], propertys[4])
        data_type_list.append(obj)
    return data_type_list


def del_line_by_line_nums(num_of_line) -> None:
    """
    根据文件行数删除文件某一行
    :param num_of_line: 文件的行数
    :return:
    """
    with open(DATA_SAVE_FILE_PATH, "r", encoding="utf-8") as f_read:
        lines = f_read.readlines()
        with open(DATA_SAVE_FILE_PATH, 'w', encoding="utf-8") as fp_out:
            fp_out.writelines(line for i, line in enumerate(lines) if i != num_of_line)
            fp_out.flush()


def close_process_and_del_file(num_of_line, data) -> str:
    """
    根据传入的下标来删除对应文件中的内容，并且根据传入的数据关闭相应的进程
    :param num_of_line: 下标
    :param data: 下标对应的数据
    :return:
    """
    process = subprocess.Popen("kill -9 {id}".format(id=data.process_pid), stderr=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, shell=True)

    del_line_by_line_nums(num_of_line)

    return "关闭成功"


def insert_new_connects() -> str:
    blank_str = "".rjust(47)
    master_port = input(blank_str + "请输入主机监听slave的端口> ")
    customer_port = input(blank_str + "请输入服务Customer的端口> ")
    message = input(blank_str + "请输入备注> ")
    dataList = file2data()
    tmp_data_type = DataType(customer_port=customer_port, master_port=master_port, process_pid=1)

    if dataList.count(tmp_data_type) != 0:
        return blank_str + "端口已经被占用，\n被占用的端口信息为:" + dataList[dataList.index(tmp_data_type)].__str__()

    current_command = START_MASTER_COMMAND.format(master_port=master_port, customer_port=customer_port)
    process = subprocess.Popen(current_command, shell=True, stderr=subprocess.DEVNULL)
    data = DataType(master_port=master_port, customer_port=customer_port, message=message, process_pid=process.pid + 1)
    save2file(data)
    return blank_str + "添加成功\n" + blank_str + "PID:{pid}\tmaster_port:{m_port}\tcustomer_port:{c_port}\tmessage:{meg}".format(
        pid=data.process_pid,
        m_port=data.master_port,
        c_port=data.customer_port,
        meg=data.message
    )


def show_current_all_connects():
    """
    显示当前的所有的连接
    :return:
    """
    start_str = ("*" * 90)
    blank_str = "".rjust(47)
    all_data = file2data()
    print(start_str.rjust(136))
    print(blank_str + "index\t\tPID\t\tC Port\t\tM Port\t\tMessage\t\tMaster IP", end="\n")
    print(start_str.rjust(136))
    for index, data in enumerate(all_data):
        print(blank_str + str(index) + "\t\t" + "\t\t".join([str(i) for i in data.__dict__.values()]))
    print(start_str.rjust(136))
    print(blank_str + "退出请输入{key} ".format(key='\033[1;35m{text}\033[0m'.format(text="q")))
    option = input(
        blank_str + "启动删除模式请输入{key}并回车\n".format(key='\033[1;35m{text}\033[0m'.format(text="d")) + "".rjust(46) + " > ")
    if option == "q":
        return
    elif option == "d":
        while True:
            index = input(blank_str + "请输入要删除的连接的下标 > ")
            if not index.isdigit():
                print(blank_str + "请输入数字,回车重试")
                input()
                continue
            index = int(index)
            if index >= len(all_data):
                print(blank_str + "请输入对应的下标！回车重试")
                input()
                continue
            info = close_process_and_del_file(index, all_data[index])
            print(blank_str + info)
            input()
            return


def ShowPrompt():
    while True:
        os.system("clear" if platform.system() == "Linux" else "cls")  # 清屏
        print('\033[1;35m{text}\033[0m'.format(text="Welcome to the shotback manager!").rjust(82))
        print(("*" * 50).rjust(80))
        print("".rjust(47) + "1.添加新的连接", end="\n")
        print("".rjust(47) + "2.查看当前已有的连接", end="\n")
        print("".rjust(47) + "3.退出", end="\n")
        print(("*" * 50).rjust(80))
        option = input("Please input your option > ")
        if option == "3":
            print("bye")
            return
        if option == "1":
            os.system("clear" if platform.system() == "Linux" else "cls")  # 清屏
            prompt = insert_new_connects()
            print(prompt)
            input()
        if option == "2":
            os.system("clear" if platform.system() == "Linux" else "cls")  # 清屏
            show_current_all_connects()


if __name__ == '__main__':
    data_save_file = open("./.save_information.data", "a+", encoding="utf-8")
    ShowPrompt()
    # for i in range(4):
    #     save2file(DataType(i,i,i))
