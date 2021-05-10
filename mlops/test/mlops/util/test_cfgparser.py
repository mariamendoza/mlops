import pytest
from mlops.util.cfgparser import CfgParser

@pytest.fixture
def cfgparser():
    return CfgParser()

@pytest.mark.parametrize("str_config, expected", [
    ('{"key": "value"}', {"key": "value"})
])
def test_read(cfgparser, tmpdir, str_config, expected):
    f = tmpdir.join("endpoint.json")
    f.write(str_config)

    actual = cfgparser.read(f)

    assert actual == expected

@pytest.mark.parametrize("str_config, expected", [
    ('{"key": "val"}', {"key": "val"}), # key, val
    ('{"key": {"key1": "val1"}}', {"key": {"key1": "val1"}}), # key, dict
    ('{"key": ["item1"]}', {"key": ["item1"]}), # key, list
    ('{"key": {"key1": {"key2": "val2"}}}', {"key": {"key1": {"key2": "val2"}}}), # key, dict, dict
    ('{"key": [{"key1": "val1"}]}', {"key": [{"key1": "val1"}]}) # key, list, dict
])
def test_parse_no_secret(cfgparser, tmpdir, str_config, expected):
    f = tmpdir.join("endpoint.json")
    f.write(str_config)

    config = cfgparser.read(f)
    actual = cfgparser.parse(config, {})

    assert actual == expected