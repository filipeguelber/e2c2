import gspread, os
print os.environ["GDRIVE_USER"]
gdrive_user=os.environ["GDRIVE_USER"]
gdrive_pass=os.environ["GDRIVE_PASS"]
gc = gspread.login(gdrive_user, gdrive_pass)
wks = gc.open("Users EC2").sheet1
print wks.acell('B1').value
