from yaml import safe_load
from csv import writer
from paramiko import SSHClient,AutoAddPolicy

def create_SSH_client (ssh_hostname, ssh_port, ssh_username, ssh_password):
    try:
        ssh_client = SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(hostname=ssh_hostname, port=ssh_port, username=ssh_username, password=ssh_password)
        return ssh_client
    except:
        return False
    
def get_os_info (ssh_client):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command('cat /etc/*release*')
    os_info = ssh_stdout.read().decode("utf8")

    ssh_stdin.close()
    ssh_stdout.close()
    ssh_stderr.close()

    return os_info

with open('config.yml', 'r') as yaml_config_file:
    config = safe_load(yaml_config_file)
    yaml_config_file.close()

    with open(config["ssh"]["list_ip_file"], "r") as list_ip_file:
        with open(config["output"]["csv"], 'w', newline='', encoding='utf-8') as output_csv_file:
            output_csv_writer = writer(output_csv_file)
            csv_header = ["IP", "OS Info"]
            output_csv_writer.writerow(csv_header)

            for ip_with_enter in list_ip_file:
                ip = ip_with_enter.replace("\n", "")
                print(ip)
                ssh_client = create_SSH_client(ip, config["ssh"]["port"], config["ssh"]["username"], config["ssh"]["password"])

                if ssh_client != False:
                    os_info = get_os_info(ssh_client)
                    csv_data = [ip, os_info]
                    output_csv_writer.writerow(csv_data)
                else:
                    csv_data = [ip, ""]
                    output_csv_writer.writerow(csv_data)

                ssh_client.close()
