import json
import socket
import shutil
import logging
import subprocess

import jinja2
import paramiko


def get_interafce_ip_addr(hostname, username, password, interface):
    """
        SSH to a host and get its IP
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to remote host
        ssh.connect(hostname=hostname, username=username, password=password, timeout=15)
        cmd = "/usr/sbin/ip -4 -o addr show dev {}|awk '{{print $4}}'|cut -d '/' -f1".format(interface)
        _, stdout, _ = ssh.exec_command(cmd)
        mlnx_ip = stdout.read().strip()

        # Validate it's an IP
        socket.inet_aton(mlnx_ip)

        # Close SSH connection
        ssh.close()
    except Exception:
        raise Exception('Failed to connect/get bond0 IP from {}'.format(hostname))
    return mlnx_ip


class ClientNode(object):

    def __init__(self, mgmt_ip, user, password):
        self.mgmt_ip = mgmt_ip
        self.user = user
        self.password = password

    @classmethod
    def from_naipi(cls, config):
        return cls(config['address'], config['username'], config['password'])


class ServerHost(object):

    def __init__(self, mgmt_ip, user, password, data_interface, has_etcd, is_master):
        self.mgmt_ip = mgmt_ip
        self.user = user
        self.password = password
        self.data_ip = get_interafce_ip_addr(mgmt_ip, user, password, data_interface)
        self.has_etcd = has_etcd
        self.is_master = is_master

    @classmethod
    def from_naipi(cls, config):
        roles = config['roles']
        if 'kube-node' not in roles:
            return None

        mgmt_ip = config['address']
        user = config['username']
        password = config['password']
        data_interface = config.get('dataplane-interface', 'bond0')

        return cls(mgmt_ip, user, password, data_interface,
                   has_etcd='kube-etcd' in roles, is_master='kube-master' in roles)


def _gen_templates(path, **kwargs):
    with open(path + '.jinja2') as fh:
        data = fh.read()

    template = jinja2.Template(
        data, keep_trailing_newline=True, trim_blocks=True,
        undefined=jinja2.StrictUndefined)
    generated_data = template.render(**kwargs)

    with open(path, 'w') as fh:
        fh.write(generated_data)


def get_servers(ips, user, password):
    masters_count = 3 if len(ips) >= 3 else 1
    for i, (mgmt_ip, data_iface) in enumerate(ips):
        is_master = i < masters_count
        yield ServerHost(mgmt_ip, user, password, data_iface, has_etcd=is_master, is_master=is_master)


def gen(servers, clients):
    shutil.copytree('inventory/sample/group_vars', 'inventory/igz/group_vars')
    cmd = ['python3', 'contrib/inventory_builder/inventory.py']
    cmd.extend(s.mgmt_ip for s in servers)
    subprocess.check_output(cmd, env={'CONFIG_FILE': 'inventory/igz/hosts.ini'})

    logging.info('generating template files')
    _gen_templates(path='inventory/igz/hosts.ini', servers=servers, clients=clients)


def from_naipi(data):
    config = json.loads(data)['setup']
    servers = (ServerHost.from_naipi(c) for c in config['clients'])
    servers = [s for s in servers if s is not None]
    if servers:
        clients = [ClientNode.from_naipi(c) for c in config['nodes']]
    else:
        clients = []

    gen(servers, clients)


def from_cli(servers, clients, user, password):
    servers = list(get_servers(servers, user, password))
    if servers:
        clients = [ClientNode(ip, user, password) for ip in clients]
    else:
        clients = []

    gen(servers, clients)
