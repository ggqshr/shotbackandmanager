"""
1.查看当前那些端口被使用，并且每个端口对应的Customer端口是多少，且可以显示备注
2.通过输出提示引导用户输入地址端口等信息，然后运行程序。
3.要有一个进程池，来管理所有的连接，每个连接都是一个进程，
4.应该是每次使用的时候才会运行，创建完连接线程后，就直接退出。
"""
import atexit
import os
from time import sleep
import platform


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


# f = open("./.save_information.data", "a", encoding="utf-8")
# f.write(s.__str__() + "\n")
# f.flush()
# f.close()
#
# print('This is a \033[1;35;47m{text}\033[0m!')


def ShowPrompt():
    os.system("clear" if platform.system() == "Linux" else "cls")  # 清屏

    print('\033[1;35m{text}\033[0m!'.format(text="Welcome to the shotback manager!"))
    print("*".center(50))


if __name__ == '__main__':
    ShowPrompt()
