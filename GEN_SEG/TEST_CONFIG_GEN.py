import csv
from jinja2 import Template


data_file = "vip.csv" #File that contains list of data
jinja_template_file = "gen-template.j2" #File that contains J2 TEMPLATE
#interface_configs = "" #String that will hold final full configuration of all interfaces

#Reads the JINJA2 FILE and Convert it into JINJA PY TEMPLATE Object
with open(jinja_template_file) as f:
    interface_template = Template(f.read())

with open(data_file) as f:
    reader = csv.DictReader(f) #Reads the source file
    for row in reader:
        interface_config = interface_template.render( #Puts the data to template
            Device = row['Device'],
            Platform = row['Platform'],
            Product = row['Product'],
            VIP = row["VIP"],
            Mgmt1 = row["Mgmt1"],
            Mgmt2 = row["Mgmt2"],
            Gateway = row["Gateway"],
            New_VIP=row["New_VIP"],
            New_Mgmt1=row["New_Mgmt1"],
            New_Mgmt2=row["New_Mgmt2"],
            New_Gateway=row["New_Gateway"],
        )
        #interface_configs += interface_config #Append each output to the full config
        print(interface_config)
        #with open("../created_config.txt", "w") as f:
        #    f.write(interface_configs)

#print(interface_configs)

#Save the output into a configuration file
#with open("../created_config.txt", "w") as f:
#    f.write(interface_configs)