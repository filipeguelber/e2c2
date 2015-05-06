from subprocess import Popen, PIPE, STDOUT


def execute_shell_command(command):
        cmd = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        result = str(cmd.communicate()[0])
        return result

if __name__ == '__main__':
    command = "pip install -r requirements.txt"
    print execute_shell_command(command)