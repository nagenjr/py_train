from napalm import get_network_driver
from netaddr import IPNetwork

import json
from tabulate import tabulate

#get_network_driver() = select the OS version
#get_facts() = collect data of OS version, interface list, hostname

device = get_network_driver('ios')
switch = device('192.168.159.101', 'admin', 'admin')

switch.open()

#output_facts = switch.get_facts()
#output_facts_json = json.dumps(output_facts, indent=4)

#output_interfaces_ip = switch.get_interfaces_ip()
#json_interfaces_ip = json.dumps(output_interfaces_ip, indent=4)

output_arp = switch.get_arp_table()
json_arp = json.dumps(output_arp, indent=4)

output_ping = switch.ping('google.com')
json_arp = json.dumps(output_ping, indent=4)

#print(output_facts_json)
#print(json_interfaces_ip)

print(json_arp)
print(tabulate(output_ping))
