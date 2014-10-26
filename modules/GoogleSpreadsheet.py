from modules.gspread import gspread
import os

class GoogleSpreadsheet(object):
	def __init__(self, name):
		self.name = name
		self.read_spreadsheet()
	
	def get_authorized_object(self):
		user     = os.environ['GDRIVE_USER']
		password = os.environ['GDRIVE_PASSWORD']
		
		gc = gspread.login(user, password)
		
		return gc
	
	def read_spreadsheet(self):
		gc             = self.get_authorized_object()
		permissions_ws = gc.open(self.name).worksheet('Permissions')
		
		return permissions_ws
	
	def getPermissions(self):
		spreadsheet = self.read_spreadsheet()
		data        = spreadsheet.get_all_values()
		
		counter = 0
		
		instances   = []
		permissions = {}
		
		for line in data:
			if counter == 0:
				instances = line[1:]
			else:
				user = line[0]
				
				permissions[user] = {}
				
				for instance, permission in zip(instances, line[1:]):
					permissions[user][instance] = permission
		
			counter += 1
		
		return permissions
