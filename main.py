from modules.GoogleSpreadsheet import *
import json

gspread     = GoogleSpreadsheet('Users EC2')
permissions = gspread.getPermissions()

pretty_dict = json.dumps(permissions, sort_keys=True, indent=4, separators=(',', ': '))

print(pretty_dict)
