from napalm import get_network_driver
from netaddr import IPNetwork

import json

#get_network_driver() = select the OS version
#get_facts() = collect data of OS version, interface list, hostname

bgp_list = ['192.168.159.101',
            '192.168.159.102']

for ip_address in bgp_list:
    print('Connecting to device ' + str(ip_address))
    driver = get_network_driver('ios')
    device = driver(ip_address, 'admin', 'admin')
    device.open()
  # device.cli(commands='ip access-list extended 100')
    device.load_merge_candidate(filename='acl.cfg')
    diffs = device.compare_config()
    if len(diffs) > 0:
        print(diffs)
        device.commit_config()
    else:
        print(" --No Changes required-- ")
        device.discard_config()

    output = device.get_interfaces_ip()
    #for i in output:
    #   if "Vlan" in i:
    #        print(i)

    print(json.dumps(output, indent=4))
    device.close()

#output_facts = switch.get_facts()
#output_facts_json = json.dumps(output_facts, indent=4)

#output_interfaces_ip = switch.get_interfaces_ip()
#json_interfaces_ip = json.dumps(output_interfaces_ip, indent=4)

#output_arp = switch.get_arp_table()
#json_arp = json.dumps(output_arp, indent=4)

#output_ping = switch.ping('google.com')
#json_arp = json.dumps(output_ping, indent=4)

#output_bgp = switch.get_bgp_neighbors()
#json_bgp = json.dumps(output_bgp, indent=4)


#print(output_facts_json)
#print(json_interfaces_ip)

#print(json_bgp)
#print(tabulate(output_ping))
