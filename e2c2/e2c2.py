import json
from GoogleSpreadsheet import GoogleSpreadsheet
from logger import Logger
from subprocess import Popen, PIPE, STDOUT


class E2C2(Logger):
    CREATE_USER_ON_INSTANCE = "ssh -i {PEM_PATH} {INSTANCE} 'sudo adduser {USER} --gecos \"\" --disabled-password'"
    HOME_DIR = '/home/{USER}/'
    SSH_DIR = '/home/{USER}/.ssh'
    CREATE_DIR = "ssh -i {PEM_PATH} {INSTANCE} \
    'sudo -u {USER} mkdir -p {SSH_DIR}'"
    ADD_USER_KEY_TO_AUTHORIZED_KEYS = "ssh -i {PEM_PATH} {INSTANCE} \"sudo -u {USER} sh -c \'echo \"{USER_KEY}\" >> {SSH_DIR}/authorized_keys\'\""
    CHECK_USER_EXISTS = "ssh -i {PEM_PATH} {INSTANCE} 'cut -d: -f1 /etc/passwd | grep {USER}'"
    DELETE_USER_ON_INSTANCE = "ssh -i {PEM_PATH} {INSTANCE} 'sudo userdel {USER}'"

    def __init__(self):
        Logger.__init__(self)
        self.spreadsheet = GoogleSpreadsheet()
        self.logger.info('Downloading spreadsheets')
        self.users = self.spreadsheet.get_users()
        self.instances = self.spreadsheet.get_instances()
        self.permissions = self.spreadsheet.get_permissions()
        self.logger.info('Spreadsheets are downloaded')

    def formatted_json(self, json_):
        return json.dumps(json_, sort_keys=True, indent=4, separators=(',', ': '))

    def get_public_key(self, user):
        self.logger.info("Get public key by %s" % user)
        return self.users[user]

    def get_host(self, instance):
        self.logger.info("Get host by %s" % instance)
        return self.instances[instance]['host']

    def get_pem_file(self, instance):
        return 'keys/' + self.instances[instance]['key']

    def user_exists(self, user, instance):
        command = self.CHECK_USER_EXISTS.format(
            PEM_PATH=self.get_pem_file(instance),
            USER=user,
            INSTANCE=self.get_host(instance)
        )
        self.logger.debug("CHECK_USER_EXISTS:\n%s" % command)
        result = self.execute_shell_command(command)
        if result != "":
            return True
        else:
            return False

    def delete_user(self, user, instance):

        if self.user_exists(user, instance):
            self.logger.debug("DELETE_USER_ON_INSTANCE:\n user found")
            command = self.DELETE_USER_ON_INSTANCE.format(
                PEM_PATH=self.get_pem_file(instance),
                USER=user,
                INSTANCE=self.get_host(instance)
            )
            self.logger.debug("DELETE_USER_ON_INSTANCE:\n%s" % command)
            self.execute_shell_command(command)
        else:
            self.logger.debug("DELETE_USER_ON_INSTANCE:\n user not found")

    def create_user_on_instance(self, user, instance):

        if self.user_exists(user, instance):
            self.logger.debug("CREATE_USER_ON_INSTANCE:\n user found")
        else:
            command = self.CREATE_USER_ON_INSTANCE.format(
                PEM_PATH=self.get_pem_file(instance),
                USER=user,
                INSTANCE=self.get_host(instance)
            )
            self.logger.debug("CREATE_USER_ON_INSTANCE:\n%s" % command)

            self.execute_shell_command(command)

            command = self.CREATE_DIR.format(
                USER=user,
                SSH_DIR=self.SSH_DIR.format(USER=user),
                PEM_PATH=self.get_pem_file(instance),
                INSTANCE=self.get_host(instance)
            )
            self.logger.debug("CREATE_DIR:\n%s" % command)

            self.execute_shell_command(command)

    def add_user_key_to_instance(self, user, instance):
        self.create_user_on_instance(user, instance)

        command = self.ADD_USER_KEY_TO_AUTHORIZED_KEYS.format(
            USER=user,
            USER_KEY=self.get_public_key(user),
            SSH_DIR=self.SSH_DIR.format(USER=user),
            PEM_PATH=self.get_pem_file(instance),
            INSTANCE=self.get_host(instance)
        )
        self.logger.debug("ADD_USER_KEY_TO_AUTHORIZED_KEYS:\n%s" % command)
        self.execute_shell_command(command)

    def execute_shell_command(self, command):
        cmd = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        result = str(cmd.communicate()[0])
        self.logger.debug("SHELL_COMMAND_RESULT:\n%s" % result)
        return result
