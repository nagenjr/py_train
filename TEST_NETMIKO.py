from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException


#One-time Username & Password
username = input('Enter username: ')
password = getpass()

#Open a file with list of IP address
with open('device_list') as DL:
    device_list = DL.read().splitlines()

#Open a file with Commands
with open('config_file') as config:
    config_file = config.read().splitlines()

#Connect via SSH
for devices in device_list:
    print('Connecting to device ' + devices +'\n')
    ip_address_of_device = devices

    #Individual username and password for each device
    #username = input('Enter username for ' + devices +': ' )
    #password = getpass()

    ios = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }

    try:
        connect = ConnectHandler(**ios)
    except (AuthenticationException):
        print('Authentication Failed: ' + devices)
        continue

    output = connect.send_config_set(config_file, delay_factor=2)
    print(output)