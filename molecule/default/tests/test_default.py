import os
import yaml
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.fixture()
def AnsibleDefaults(Ansible):
    with open("./defaults/main.yml", 'r') as stream:
        return yaml.load(stream)


@pytest.mark.parametrize('minio_bin_var', [
    'minio_server_bin_path',
    'minio_client_bin_path',
])
def test_minio_installed(File, AnsibleDefaults, minio_bin_var):

    f = File(AnsibleDefaults[minio_bin_var])
    assert f.exists
    assert f.user == AnsibleDefaults['minio_user']
    assert f.group == AnsibleDefaults['minio_group']
    assert oct(f.mode) == '0755'


def test_minio_service(Service):

    s = Service('minio')
    assert s.is_running
    assert s.is_enabled
