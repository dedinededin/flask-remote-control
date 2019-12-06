from flask import Flask
from flask import request
import subprocess

app = Flask('flaskshell')
ip_whitelist = ['192.168.1.124']
command_list = {
    "lock": "pmset displaysleepnow",
    "restart": "reboot",
    "shutdown": "shutdown -r now",
}


def valid_ip():
    client = request.remote_addr
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
        command = command_list[command_option]
        try:
            result_success = subprocess.check_output(
                [command], shell=True)
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to fetch task status updates."

        return f'Response\n{result_success}', 200
    else:
        return """You have no permission""", 404


if __name__ == '__main__':
    app.run(host='192.168.1.111')
