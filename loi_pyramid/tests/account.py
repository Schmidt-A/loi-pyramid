# flake8: noqa
import copy

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid import testing

from .base_test import BaseTest
from ..views.account import AccountViews
from ..views.account import AccountsViews


class TestAccountViews(BaseTest):

    #Initial setup for these tests
    #Needs to be broken up
    def setUp(self):
        super(TestAccountViews, self).setUp()
        self.init_database()

        from ..models import Account

        self.host = 'http://localhost:6543'

        fixture = []
        self.tweek = Account(
                username    = 'Tweek',
                password    = 'dragon4ever',
                cdkey       = 'efgh5678',
                role        = 3,
                approved    = 1,
                banned      = 0)
        fixture.append(self.tweek)
        self.aez = Account(
                username    = 'Aez',
                password    = 'eldath4ever',
                cdkey       = 'abcd1234',
                role        = 3,
                approved    = 1,
                banned      = 0)
        fixture.append(self.aez)
        self.naia = Account(
                username    = 'Naiatis',
                password    = 'faggot4ever',
                cdkey       = 'mnop6969',
                role        = 2,
                approved    = 1,
                banned      = 0)
        fixture.append(self.naia)
        self.noob = Account(
                username    = 'DrizztFan',
                password    = 'sinfar4ever',
                cdkey       = 'ijkl0000',
                role        = 1,
                approved    = 0,
                banned      = 0)
        fixture.append(self.noob)
        self.maka = Account(
                username    = 'Makazasky',
                password    = 'maka4ever',
                cdkey       = 'qrst8888',
                role        = 1,
                approved    = 1,
                banned      = 1)
        fixture.append(self.maka)
        self.abiscuit = Account(
                username    = 'abiscuit',
                password    = 'ville4ever',
                cdkey       = 'uvwx4321',
                role        = 1,
                approved    = 1,
                banned      = 0)
        fixture.append(self.abiscuit)

        self.session.add_all(fixture)
        self.session.flush()

        #non existent account, to be used for negative testing
        self.tam = Account(
                username    = 'TamTamTamTam',
                password    = 'dicks4ever',
                cdkey       = 'yzyz8008',
                role        = 1,
                approved    = 0,
                banned      = 0)
        fixture.append(self.abiscuit)

    #Helper method for get calls to /account/{username}
    def account_get(self, account):
        resource = '/account/{}'.format(account.username)
        url_params = {'username': account.username}
        request = self.dummy_request(self.session, (self.host+resource))

        account_view = AccountViews(testing.DummyResource(), request)
        account_view.url = url_params

        account_result = account_view.get().__json__(request)
        return account_result

    #Helper method for get all calls to /accounts
    def accounts_get_all(self):
        resource = '/accounts'
        request = self.dummy_request(self.session, (self.host+resource))

        account_view = AccountsViews(testing.DummyResource(), request)

        accounts_get = []
        for account in account_view.get():
            accounts_get.append(account.__json__(request))

        return accounts_get

    #Test that we can get Siobhan via get call
    def test_tweek_get(self):
        account_result = self.account_get(self.tweek)

        self.assertEqual(account_result['username'], self.tweek.username)
        self.assertEqual(account_result['password'], self.tweek.password)
        self.assertEqual(account_result['cdkey'], self.tweek.cdkey)
        self.assertEqual(account_result['role'], self.tweek.role)
        self.assertEqual(account_result['approved'], self.tweek.approved)
        self.assertEqual(account_result['banned'], self.tweek.banned)

    #Test that we cannot get Tam via get call
    #Because he'll never nut up and log on
    def test_tam_get_not_found(self):
        with self.assertRaises(HTTPNotFound):
            self.account_get(self.tam)

    #Test that we can get all six accounts via get all call
    #As those are the only created accounts
    def test_all_six_accounts_get(self):
        accounts_result = self.accounts_get_all()

        self.assertEqual(len(accounts_result), 6)
        tweek = accounts_result[0]
        aez = accounts_result[1]
        naia = accounts_result[2]
        noob = accounts_result[3]
        maka = accounts_result[4]
        abiscuit = accounts_result[5]

        self.assertEqual(tweek['username'], self.tweek.username)
        self.assertEqual(tweek['password'], self.tweek.password)
        self.assertEqual(tweek['cdkey'], self.tweek.cdkey)
        self.assertEqual(tweek['role'], self.tweek.role)
        self.assertEqual(tweek['approved'], self.tweek.approved)
        self.assertEqual(tweek['banned'], self.tweek.banned)

        self.assertEqual(aez['username'], self.aez.username)
        self.assertEqual(aez['password'], self.aez.password)
        self.assertEqual(aez['cdkey'], self.aez.cdkey)
        self.assertEqual(aez['role'], self.aez.role)
        self.assertEqual(aez['approved'], self.aez.approved)
        self.assertEqual(aez['banned'], self.aez.banned)

        self.assertEqual(naia['username'], self.naia.username)
        self.assertEqual(naia['password'], self.naia.password)
        self.assertEqual(naia['cdkey'], self.naia.cdkey)
        self.assertEqual(naia['role'], self.naia.role)
        self.assertEqual(naia['approved'], self.naia.approved)
        self.assertEqual(naia['banned'], self.naia.banned)

        self.assertEqual(noob['username'], self.noob.username)
        self.assertEqual(noob['password'], self.noob.password)
        self.assertEqual(noob['cdkey'], self.noob.cdkey)
        self.assertEqual(noob['role'], self.noob.role)
        self.assertEqual(noob['approved'], self.noob.approved)
        self.assertEqual(noob['banned'], self.noob.banned)

        self.assertEqual(maka['username'], self.maka.username)
        self.assertEqual(maka['password'], self.maka.password)
        self.assertEqual(maka['cdkey'], self.maka.cdkey)
        self.assertEqual(maka['role'], self.maka.role)
        self.assertEqual(maka['approved'], self.maka.approved)
        self.assertEqual(maka['banned'], self.maka.banned)

        self.assertEqual(abiscuit['username'], self.abiscuit.username)
        self.assertEqual(abiscuit['password'], self.abiscuit.password)
        self.assertEqual(abiscuit['cdkey'], self.abiscuit.cdkey)
        self.assertEqual(abiscuit['role'], self.abiscuit.role)
        self.assertEqual(abiscuit['approved'], self.abiscuit.approved)
        self.assertEqual(abiscuit['banned'], self.abiscuit.banned)
