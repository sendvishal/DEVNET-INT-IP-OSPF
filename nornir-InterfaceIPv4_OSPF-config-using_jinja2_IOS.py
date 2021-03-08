from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_title, print_result

nr = InitNornir(config_file="config.yml")


def basic_configuration(task):
    r = task.run(template_file,
                 template="InterfaceIP-ospf.j2", path=f"templates/")
    task.host["config"] = r.result
    output = task.host["config"]
    send = output.splitlines()
    task.run(netmiko_send_config,  config_commands=send)
    task.run(netmiko_send_command,
             command_string='show ip ospf neighbor')


print_title("Runbook to configure the interface")
result = nr.run(task=basic_configuration)
print_result(result)
