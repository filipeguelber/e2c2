import os
import gspread


class GoogleSpreadsheet(object):
    SPREADSHEET = 'E2C2'
    WORKSHEET_USERS = 'Users'
    WORKSHEET_INSTANCE = 'Instances'
    WORKSHEET_PERMISSIONS = 'Permissions'

    def __init__(self):
        self.username = os.environ['GDRIVE_USERNAME']
        self.password = os.environ['GDRIVE_PASSWORD']

    def _login(self, username, password):
        return gspread.login(username, password)

    def _open_spreadsheet(self, worksheet):
        spreadsheet = self._login(self.username, self.password)
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
            instance, host = line
            instances[instance] = host

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

                permissions[user] = {}

                for instance, permission in zip(instances, line[1:]):
                    permissions[user][instance] = permission

            counter += 1

        return permissions