#!/usr/bin/env python
# -*- coding: utf_8 -*-
# Подключаем модуль для работы с SSH сервером.
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from Options import ssh_port, login_device, password_device
from datetime import datetime
import time
import csv

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())


def writeinlog(str):
    with open('log.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, dialect='excel-tab', delimiter=";")
        writer.writerow(str)


def reboot():
    # Выполняем соединение с устройством.
    for i in range(5, 18, 1):
        ip_device = '192.168.40.' + str(i)
        try:
            ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
        except:
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
        time.sleep(30)


if __name__ == '__main__':
    reboot()
