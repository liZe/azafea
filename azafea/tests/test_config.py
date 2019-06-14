import pytest

import azafea.config
from azafea.logging import setup_logging
from azafea.utils import get_cpu_count


def test_defaults():
    number_of_workers = get_cpu_count()
    config = azafea.config.Config()

    assert not config.main.verbose
    assert config.main.number_of_workers == number_of_workers
    assert config.redis.host == 'localhost'
    assert config.redis.port == 6379
    assert config.postgresql.host == 'localhost'
    assert config.postgresql.port == 5432
    assert config.postgresql.user == 'azafea'
    assert config.postgresql.password == 'CHANGE ME!!'
    assert config.postgresql.database == 'azafea'

    assert str(config) == '\n'.join([
        '[main]',
        'verbose = false',
        f'number_of_workers = {number_of_workers}',
        '',
        '[redis]',
        'host = "localhost"',
        'port = 6379',
        '',
        '[postgresql]',
        'host = "localhost"',
        'port = 5432',
        'user = "azafea"',
        'password = "** hidden **"',
        'database = "azafea"',
        '',
        '[queues]',
    ])


def test_get_nonexistent_option():
    config = azafea.config.Config()

    with pytest.raises(azafea.config.NoSuchConfigurationError) as exc_info:
        config.main.gauche

    assert f"No such configuration option: 'gauche'" in str(exc_info.value)


def test_override(monkeypatch, make_config):
    def process(*args, **kwargs):
        pass

    def mock_get_handler(module):
        return process

    with monkeypatch.context() as m:
        m.setattr(azafea.config, 'get_handler', mock_get_handler)
        config = make_config({
            'main': {'number_of_workers': 1},
            'redis': {'port': 42},
            'postgresql': {'host': 'pg-server'},
            'queues': {'some-queue': {'handler': 'azafea.tests.test_config'}},
        })

    assert not config.main.verbose
    assert config.main.number_of_workers == 1
    assert config.redis.host == 'localhost'
    assert config.redis.port == 42
    assert config.postgresql.host == 'pg-server'
    assert config.postgresql.port == 5432
    assert config.postgresql.user == 'azafea'
    assert config.postgresql.password == 'CHANGE ME!!'
    assert config.postgresql.database == 'azafea'

    assert str(config) == '\n'.join([
        '[main]',
        'verbose = false',
        'number_of_workers = 1',
        '',
        '[redis]',
        'host = "localhost"',
        'port = 42',
        '',
        '[postgresql]',
        'host = "pg-server"',
        'port = 5432',
        'user = "azafea"',
        'password = "** hidden **"',
        'database = "azafea"',
        '',
        '[queues.some-queue]',
        'handler = "azafea.tests.test_config"',
    ])


def test_override_with_nonexistent_file():
    config = azafea.config.Config.from_file('/no/such/file')

    # Ensure we got the defaults
    assert config == azafea.config.Config()


@pytest.mark.parametrize('value', [
    42,
    'true',
])
def test_override_verbose_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'main': {'verbose': value}})

    assert ('Invalid [main] configuration:\n'
            f'* verbose: {value!r} is not a boolean') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    '42',
])
def test_override_number_of_workers_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'main': {'number_of_workers': value}})

    assert ('Invalid [main] configuration:\n'
            f'* number_of_workers: {value!r} is not an integer') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    -1,
    0,
])
def test_override_number_of_workers_negative_or_zero(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'main': {'number_of_workers': value}})

    assert ('Invalid [main] configuration:\n'
            f'* number_of_workers: {value!r} is not a strictly positive integer'
            ) in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    42,
])
def test_override_redis_host_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'host': value}})

    assert ('Invalid [redis] configuration:\n'
            f'* host: {value!r} is not a string') in str(exc_info.value)


def test_override_redis_host_empty(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'host': ''}})

    assert ('Invalid [redis] configuration:\n'
            f"* host: '' is empty") in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    'foo',
])
def test_override_redis_port_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'port': value}})

    assert ('Invalid [redis] configuration:\n'
            f'* port: {value!r} is not an integer') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    -1,
    0,
])
def test_override_redis_port_not_positive(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'redis': {'port': value}})

    assert ('Invalid [redis] configuration:\n'
            f'* port: {value!r} is not a strictly positive integer') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    42,
])
def test_override_postgresql_host_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'host': value}})

    assert ('Invalid [postgresql] configuration:\n'
            f'* host: {value!r} is not a string') in str(exc_info.value)


def test_override_postgresql_host_empty(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'host': ''}})

    assert ('Invalid [postgresql] configuration:\n'
            f"* host: '' is empty") in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    'foo',
])
def test_override_postgresql_port_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'port': value}})

    assert ('Invalid [postgresql] configuration:\n'
            f'* port: {value!r} is not an integer') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    -1,
    0,
])
def test_override_postgresql_port_not_positive(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'port': value}})

    assert ('Invalid [postgresql] configuration:\n'
            f'* port: {value!r} is not a strictly positive integer') in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    42,
])
def test_override_postgresql_user_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'user': value}})

    assert ('Invalid [postgresql] configuration:\n'
            f'* user: {value!r} is not a string') in str(exc_info.value)


def test_override_postgresql_user_empty(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'user': ''}})

    assert ('Invalid [postgresql] configuration:\n'
            f"* user: '' is empty") in str(exc_info.value)


@pytest.mark.parametrize('value', [
    False,
    True,
    42,
])
def test_override_postgresql_password_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'password': value}})

    assert ('Invalid [postgresql] configuration:\n'
            f'* password: {value!r} is not a string') in str(exc_info.value)


def test_override_postgresql_password_empty(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'password': ''}})

    assert ('Invalid [postgresql] configuration:\n'
            f"* password: '' is empty") in str(exc_info.value)


def test_postgresql_default_password(capfd):
    setup_logging(verbose=False)
    azafea.config.Config()

    capture = capfd.readouterr()
    assert 'Did you forget to change the PostgreSQL password?' in capture.err


@pytest.mark.parametrize('value', [
    False,
    True,
    42,
])
def test_override_postgresql_database_invalid(make_config, value):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'database': value}})

    assert ('Invalid [postgresql] configuration:\n'
            f'* database: {value!r} is not a string') in str(exc_info.value)


def test_override_postgresql_database_empty(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'postgresql': {'database': ''}})

    assert ('Invalid [postgresql] configuration:\n'
            f"* database: '' is empty") in str(exc_info.value)


def test_add_queue_with_nonexistent_handler_module(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'queues': {'some-queue': {'handler': 'no.such.module'}}})

    assert ('Invalid [queues] configuration:\n'
            f"* handler: Could not import handler module 'no.such.module'"
            ) in str(exc_info.value)


def test_add_queue_with_invalid_handler_module(make_config):
    with pytest.raises(azafea.config.InvalidConfigurationError) as exc_info:
        make_config({'queues': {'some-queue': {'handler': 'azafea'}}})

    assert ('Invalid [queues] configuration:\n'
            f"* handler: Handler 'azafea' is missing a \"process\" function"
            ) in str(exc_info.value)