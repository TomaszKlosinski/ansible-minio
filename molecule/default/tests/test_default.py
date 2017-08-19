import os
import yaml
import pytest

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleDefaults(Ansible):
    with open("../../defaults/main.yml", 'r') as stream:
        return yaml.load(stream)


@pytest.mark.parametrize('minio_bin', [
    'minio_server_bin_path',
    # TODO: Add client
    # 'minio_client_bin_path',
])
def test_minio_installed(File, AnsibleDefaults, minio_bin):

    f = File(AnsibleDefaults[minio_bin])
    assert f.exists
    assert f.user == AnsibleDefaults['minio_user']
    assert f.group == AnsibleDefaults['minio_group']
    assert oct(f.mode) == '0755'


def test_minio_service_running_and_enabled(Service):

    s = Service('minio')
    assert s.is_running
    assert s.is_enabled


# check ipv4 ('0.0.0.0') and ipv6 ('::') binding
@pytest.mark.parametrize('socket_address', [
    # FIXME: testinfra complains that minio is not listening on ipv4
    # 'tcp://0.0.0.0:9000',
    'tcp://:::9000'
])
def test_minio_service_listening(Socket, socket_address):

    socket = Socket(socket_address)
    assert socket.is_listening
