import os

with open('test123') as f:
    device_list = f.read()
    device_list = device_list.splitlines()
#    print(device_list)

for ip in device_list:
    response = os.popen(f"ping -c 1 {ip}").read()
    if ("0 received") in response:
        print(ip + ' is down')
    else:
        print(ip + ' is up')
