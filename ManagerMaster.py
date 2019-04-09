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

DATA_SAVE_FILE_PATH = "./.save_information.data"
data_save_file: TextIOWrapper = None


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


f = open("./.save_information.data", "a", encoding="utf-8")


# f.write(s.__str__() + "\n")
# f.flush()
# f.close()
#
# print('This is a \033[1;35;47m{text}\033[0m!')
def save2file(data: DataType) -> None:
    """
    将传入的DataType对象的信息存入文件
    :param data: 要存入文件的对象
    :return:
    """
    data_save_file.write(data.__str__() + "/n")
    data_save_file.flush()


def file2data() -> list[DataType]:
    data_type_list = []
    for data in data_save_file.readlines():
        propertys = data.split("\t")
        obj = DataType(propertys[0], propertys[1], propertys[2], propertys[3], propertys[4])
        data_type_list.append(obj)
    return data_type_list


def del_line_by_line_nums(num_of_line):
    with open('in.txt') as fp_in:
        with open('out.txt', 'w') as fp_out:
            fp_out.writelines(line for i, line in enumerate(fp_in) if i != 10)


def ShowPrompt():
    os.system("clear" if platform.system() == "Linux" else "cls")  # 清屏

    print('\033[1;35m{text}\033[0m'.format(text="Welcome to the shotback manager!").rjust(82))
    print(("*" * 50).rjust(80))
    print("".rjust(47) + "1.添加新的连接", end="\n")
    print("".rjust(47) + "2.查看当前已有的连接", end="\n")
    print("".rjust(47) + "3.退出", end="\n")
    print(("*" * 50).rjust(80))
    option = input("Please input your option:")
    if option == "3":
        print("bye")
        return
    if option == "1":
        os.system("clear" if platform.system() == "Linux" else "cls")  # 清屏


if __name__ == '__main__':
    ShowPrompt()
