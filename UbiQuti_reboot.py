#!/usr/bin/env python
# -*- coding: utf_8 -*-
# Подключаем модуль для работы с SSH сервером.
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from Options import ssh_port, login_device, password_device, ip_device_office, ip_device_larang, ip_device_polyclinica
from datetime import datetime
import time
import csv
pause = 30
    
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())


def writeinlog(str):
    with open('log.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, dialect='excel-tab', delimiter=";")
        writer.writerow(str)

def get_ip():
    iplist = []
    for i in ip_device_site1:
        iplist.append(i)
    for i in ip_device_site2:
        iplist.append(i)
    for i in range(5, 18, 1):
        ip_device = '192.168.40.' + str(i)
        iplist.append(ip_device)
    return iplist


def reboot():
    # Получаем IP адреса точек
    for ip_device in get_ip():

    # Выполняем соединение с устройством.
        try:
            ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
        except Exception as E:
            writeinlog(str=[ip_device, 'Failed to connect in', str(datetime.now())])
        else:
    # Выполняем перезагрузку устройства.
            try:
                cmd = 'reboot'
                ssh.exec_command(cmd)
            except Exception as E:
                writeinlog(str=[ip_device, 'reboot failed', str(datetime.now())])
            else:
                writeinlog(str=[ip_device, 'has been rebooted in', str(datetime.now())])

        ssh.close()
        time.sleep(pause)


if __name__ == '__main__':
    reboot()
