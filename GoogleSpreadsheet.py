import json
import os
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


class GoogleSpreadsheet(object):
    SPREADSHEET = 'E2C2'
    WORKSHEET_USERS = 'Users'
    WORKSHEET_INSTANCE = 'Instances'
    WORKSHEET_PERMISSIONS = 'Permissions'

    def __init__(self):
        self.credentials_path = os.environ['CREDENTIALS_PATH']

    def _login(self):
        json_key = json.load(open(self.credentials_path))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        return gspread.authorize(credentials)

    def _open_spreadsheet(self, worksheet):
        spreadsheet = self._login()
        spreadsheet = spreadsheet.open(self.SPREADSHEET).worksheet(worksheet)
        return spreadsheet.get_all_values()

    def get_users(self):
        data = self._open_spreadsheet(self.WORKSHEET_USERS)
        return self._parse_users_worksheet(data)

    def add_user(self):
        raise NotImplementedError

    def get_instances(self):
        data = self._open_spreadsheet(self.WORKSHEET_INSTANCE)
        return self._parse_instances_worksheet(data)

    def add_instance(self):
        raise NotImplementedError

    def get_permissions(self):
        data = self._open_spreadsheet(self.WORKSHEET_PERMISSIONS)
        return self._parse_permissions_worksheet(data)

    def add_permision(self):
        raise NotImplementedError

    def _parse_users_worksheet(self, data):
        users = {}

        for line in data:
            user, public_key = line
            users[user] = public_key

        return users

    def _parse_instances_worksheet(self, data):
        instances = {}

        for line in data:
            instance = line[0]
            instances[instance] = {}
            instances[instance]['host'] = line[1]
            instances[instance]['key'] = line[2]

        return instances

    def _parse_permissions_worksheet(self, data):
        counter = 0
        instances = []
        permissions = {}

        for line in data:

            if counter == 0:
                instances = line[1:]
            else:
                user = line[0]
                if not hasattr(permissions, user):
                    permissions[user] = {}
                    for instance, permission in zip(instances, line[1:]):
                        if not instance == '':
                            permissions[user][instance] = permission

            counter += 1
        return permissions