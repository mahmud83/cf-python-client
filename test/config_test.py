import os
import ConfigParser
import logging
from cloudfoundry_client.client import CloudFoundryClient

_client = None
_org_guid = None
_space_guid = None
_app_guid = None


def _init_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)5s - %(name)s -  %(message)s')


def build_client_from_configuration():
    global _client
    if _client is None:
        _init_logging()
        path = os.path.join(os.path.dirname(__file__), 'test.properties')
        if not (os.path.exists(path) and os.path.isfile(path) and os.access(path, os.R_OK)):
            raise IOError('File %s must exist. Please use provided template')
        cfg = ConfigParser.ConfigParser()
        cfg.read(path)
        proxy = None
        try:
            http = cfg.get('proxy', 'http')
            https = cfg.get('proxy', 'https')
            proxy = dict(http=http, https=https)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), _:
            pass
        skip_verification = False
        try:
            skip_verification_str = cfg.get('service', 'skip_ssl_verification')
            skip_verification = skip_verification_str.lower() == 'true'
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError), _:
            pass
        client = CloudFoundryClient(cfg.get('service', 'target_endpoint'), proxy=proxy,
                                    skip_verification=skip_verification)
        client.credentials_manager.init_with_credentials(cfg.get('authentification', 'login'),
                                                         cfg.get('authentification', 'password'))
        client.org_guid = cfg.get('test_data', 'org_guid')
        client.space_guid = cfg.get('test_data', 'space_guid')
        client.app_guid = cfg.get('test_data', 'app_guid')
        client.service_guid = cfg.get('test_data', 'service_guid')
        client.service_name = cfg.get('test_data', 'service_name')
        client.plan_guid = cfg.get('test_data', 'plan_guid')
        _client = client

    return _client
