import unittest

from sslyze.server_connectivity_tester import ServerConnectivityTester
from sslyze.ssl_settings import ClientAuthenticationServerConfigurationEnum
from tests.openssl_server import ModernOpenSslServer, ClientAuthConfigEnum


class ClientAuthenticationTestCase(unittest.TestCase):

    @unittest.skipIf(not ModernOpenSslServer.is_platform_supported(), 'Not on Linux 64')
    def test_optional_client_auth(self):
        # Given a server that supports optional client authentication
        with ModernOpenSslServer(client_auth_config=ClientAuthConfigEnum.OPTIONAL) as server:
            server_test = ServerConnectivityTester(
                hostname=server.hostname,
                ip_address=server.ip_address,
                port=server.port
            )
            server_info = server_test.perform()

        # SSLyze correctly detects that client auth is optional
        self.assertEqual(server_info.client_auth_requirement, ClientAuthenticationServerConfigurationEnum.OPTIONAL)

    @unittest.skipIf(not ModernOpenSslServer.is_platform_supported(), 'Not on Linux 64')
    def test_required_client_auth(self):
        # Given a server that requires client authentication
        with ModernOpenSslServer(client_auth_config=ClientAuthConfigEnum.REQUIRED) as server:
            server_test = ServerConnectivityTester(
                hostname=server.hostname,
                ip_address=server.ip_address,
                port=server.port
            )
            server_info = server_test.perform()

        # SSLyze correctly detects that client auth is required
        self.assertEqual(server_info.client_auth_requirement, ClientAuthenticationServerConfigurationEnum.REQUIRED)
