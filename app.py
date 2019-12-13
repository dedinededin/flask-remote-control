from flask import Flask
from flask import request
import subprocess

app = Flask('flaskshell')
ip_whitelist = ['192.168.1.124']
command_list = {
    "lock": "rundll32.exe user32.dll,LockWorkStation",
    "restart": "shutdown /r",
    "shutdown": "shutdown /s",
}


def valid_ip():
    client = request.remote_addr
    if '*' in ip_whitelist:
        return True
    if client in ip_whitelist:
        return True
    else:
        return False


@app.route('/help')
def show_commands():
    response_str = ""

    for command in command_list:
        response_str += f"{command} -> {command_list[command]}\n"

    return response_str


@app.route('/<command_option>')
def get_status(command_option):
    if valid_ip():
        try:
            command = command_list[command_option]
            result_success = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying run the command."
        except KeyError:
            return "Command not found"

        return f'Response\n{result_success}', 200
    else:
        return """You have no permission""", 404


if __name__ == '__main__':
    app.run(host='192.168.1.123')
