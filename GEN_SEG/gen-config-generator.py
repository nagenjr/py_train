import csv
import os
from jinja2 import Template


data_file = "GEN-Device.csv" #File that contains list of data
jinja_template_file = "gen-template.j2" #File that contains J2 TEMPLATE
output_folder = "configs" #Folder to store output configs

#Reads the JINJA2 FILE and Convert it into JINJA PY TEMPLATE Object
with open(jinja_template_file) as f:
    interface_template = Template(f.read())

#Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

#Iterate over the data rows and generate configurations
with open(data_file) as f:
    reader = csv.DictReader(f) #Reads the source file
    for row in reader:
        #Generate file name based on Device name
        filename = f"{row['Device']}.txt"
        filepath = os.path.join(output_folder, filename)

        #Check if config file for this Device already exists
        if os.path.exists(filepath):
            print(f"Config for {row['Device']} already exists, skipping...")
            continue

        #Render the interface config template
        interface_config = interface_template.render(
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

        #Write config to file
        with open(filepath, "w") as f:
            f.write(interface_config)
            print(f"Config for {row['Device']} written to {filepath}")
