import csv
from jinja2 import Template


data_file = "switchport.csv" #File that contains list of data
jinja_template_file = "switchport-interface-template.j2" #File that contains J2 TEMPLATE
interface_configs = "" #String that will hold final full configuration of all interfaces

#Reads the JINJA2 FILE and Convert it into JINJA PY TEMPLATE Object
with open(jinja_template_file) as f:
    interface_template = Template(f.read())

with open(data_file) as f:
    reader = csv.DictReader(f) #Reads the source file
    for row in reader:
        interface_config = interface_template.render( #Puts the data to template
            interface = row["interface"],
            vlan = row["vlan"],
            server = row["server"],
            link = row["link"],
            purpose = row["purpose"]
        )
        interface_configs += interface_config #Append each output to the full config

print(interface_configs)

#Save the output into a configuration file
with open("../interface_configs.txt", "w") as f:
    f.write(interface_configs)