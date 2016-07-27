import pytest

import os

from dnsimple import DNSimple, DNSimpleException

@pytest.fixture
def credentials_file():
    return os.path.join(os.getcwd(), '.dnsimple')

class TestAuth(object):

    def setup_method(self, method):
        self.remove_credentials_file()

    def teardown_method(self, method):
        self.remove_credentials_file()

    def remove_credentials_file(self):
        try:
            os.remove(credentials_file())
        except:
            pass

    def test_authentication_with_no_credentials_raises(self):
        with pytest.raises(DNSimpleException) as exception:
            client = DNSimple()

        assert 'No authentication details provided.' in str(exception.value)

    def test_authentication_with_invalid_credentials_raises(self):
        with pytest.raises(DNSimpleException) as exception:
            client = DNSimple(username = 'user@host.com', password = 'bogus')
            client.domains()

        assert 'Authentication failed' in str(exception.value)

    def test_basic_authentication_raises_no_exceptions(self):
        client = DNSimple(
            username = os.getenv('DNSIMPLE_EMAIL'),
            password = os.getenv('DNSIMPLE_PASSWORD'),
            sandbox  = True
        )

        client.domains()

    def test_user_token_auth_raises_no_exception(self):
        client = DNSimple(
            email     = os.getenv('DNSIMPLE_EMAIL'),
            api_token = os.getenv('DNSIMPLE_API_TOKEN'),
            sandbox   = True
        )

        client.domains()

    def test_basic_authentication_from_credentials_file_raises_no_exception(self, credentials_file):
        # Create local credentials file
        file = open(credentials_file, 'w')
        file.writelines([
            "[DNSimple]\n",
            "email: {0}\n".format(os.getenv('DNSIMPLE_EMAIL')),
            "api_token: {0}\n".format(os.getenv('DNSIMPLE_API_TOKEN'))
        ])
        file.close()

        client = DNSimple(sandbox = True)

        client.domains()

    @pytest.mark.skip (reason = "Domain tokens require intervention in the web app")
    def test_domain_token_auth(self):
        dns = DNSimple(domain_token='DOMAIN_TOKEN', sandbox=True)
        with self.assertRaises(DNSimpleException):
            self.assertTrue(type(dns.domains()) is list)
        self.assertTrue(type(dns.records('DOMAIN')) is list)
