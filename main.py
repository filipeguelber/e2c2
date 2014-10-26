from modules.GoogleSpreadsheet import *
import json

gspread     = GoogleSpreadsheet('Users EC2')
permissions = gspread.getPermissions()

pretty_dict = json.dumps(permissions, sort_keys=True, indent=4, separators=(',', ': '))

print(pretty_dict)

exit

import gspread, os, commands
print os.environ["GDRIVE_USER"]
gdrive_user=os.environ["GDRIVE_USER"]
gdrive_pass=os.environ["GDRIVE_PASS"]

gc = gspread.login(gdrive_user, gdrive_pass)


def get_public_key(user):
	return "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8CGShienalh9Yd3FxiVi9UYIAWdrsZW49dVq/jkfv1pfLs/zjB3d2fTyusyd/qikZ8sVZ92rQVczBNZfqTUq5aMPxnI/LvOUP2D8SqU9laLQ33kVgY57uLDvi3YApAxXnvoaZguke0AvwUahlloIlfc5T7gOMytJh1dugc1C6RqUgNpkOpedvUc4oNhdqEf8Kw0si6Xq/JJlOMoOJdgtn1+0sIBem2VwtLFz7K2OSppK8Nn7janhuigdM1xSiFnKB6mTqsuBOKuWGD8n1WLbXdmYpCobSCnLnUEZLYAJxpF7avJy1iGUoWWYYvn8KJY70cWYEzbDd99nu/hZR15JP filipe@Filipes-MacBook-Pro.local"


def get_host(instance):
	return "ubuntu@ec2-54-207-84-100.sa-east-1.compute.amazonaws.com"

def get_pem_file_path(instance):
	return "~/UptimeKeyPair.pem"

def create_user_on_instance(user, instance):
	resp = commands.getstatusoutput ("ssh -i "+get_pem_file_path(instance)+" "+get_host(instance)+" 'sudo adduser "+user+" --gecos \"\" --disabled-password'")	
	print resp;
	return 1

def copy_ssh_key_to_instance(ssh_key,user, instance):
	home_dir = "/home/"+user+"/"
	create_dir="sudo -u"+user+" mkdir "+home_dir+".ssh;sudo -u"+user+" chmod 700 "+home_dir+".ssh;sudo -u"+user+" touch "+home_dir+".ssh/authorized_keys;sudo -u"+user+" chmod 600 "+home_dir+".ssh/authorized_keys"
	print "ssh -i "+get_pem_file_path(instance)+" "+get_host(instance)+" '"+create_dir+"'"
	write_ssh_to_file="sudo -u"+user+" sh -c 'echo \""+ssh_key+"\" >>/home/"+user+"/.ssh/authorized_keys'"
	print "ssh -i "+get_pem_file_path(instance)+" "+get_host(instance)+" \""+write_ssh_to_file+"\""
	resp = commands.getstatusoutput ("ssh -i "+get_pem_file_path(instance)+" "+get_host(instance)+" \""+create_dir+"\"")	
	resp = commands.getstatusoutput ("ssh -i "+get_pem_file_path(instance)+" "+get_host(instance)+" \""+write_ssh_to_file+"\"")	
	#print resp;
	return 1



wks_users = gc.open("Users EC2").worksheet("Users")
users_data = wks_users.get_all_values()

wks_instances = gc.open("Users EC2").worksheet("Instances")
instances_data = wks_instances.get_all_values()

wks_permissions = gc.open("Users EC2").worksheet("Permissions")
permissions_data = wks_permissions.get_all_values()

user = "filipeg"
instance = "inst1"
pub_key = get_public_key(user)
create_user_on_instance(user,instance)
copy_ssh_key_to_instance(pub_key,user,instance)


