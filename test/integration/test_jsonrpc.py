import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from absoluted import AbsoluteDaemon
from absolute_config import AbsoluteConfig


def test_absoluted():
    config_text = AbsoluteConfig.slurp_config_file(config.absolute_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000de52875a68d7bf6a5bb5ad1b89fd7df4d67a9603669327949923dc74d7e'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000de52875a68d7bf6a5bb5ad1b89fd7df4d67a9603669327949923dc74d7e'

    creds = AbsoluteConfig.get_rpc_creds(config_text, network)
    absoluted = AbsoluteDaemon(**creds)
    assert absoluted.rpc_command is not None

    assert hasattr(absoluted, 'rpc_connection')

    # Absolute testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = absoluted.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert absoluted.rpc_command('getblockhash', 0) == genesis_hash
