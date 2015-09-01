#coding=utf-8

import threading
import paramiko
import subprocess


def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    
    # 可以设置使用密钥来代替密码进行验证
    # client.load_host_keys('/root/.ssh/known_hosts')
    
    # 设置策略自动添加和保存目标SSH服务器的SSH密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return


ssh_command('123.57.28.63', 'sfish', 'sfish_1XX', 'id')
