import datetime
import unittest

from unittest.mock import patch

from bill_member import calculate_bill, MemberAccounts
from test_readings import TEST_READINGS


class TestMemberAccounts(unittest.TestCase):

    def test_accounts_types(self):
        assert MemberAccounts.ACCOUNTS_INITIAL == {'electricity': None, 'gas': None}

    def test_init_member_id(self):
        member_accounts = MemberAccounts('member-123', TEST_READINGS)
        assert member_accounts.member_id == 'member-123'

    def test_init_id_not_in_readings(self):
        try:    
            member_accounts = MemberAccounts('member-123', {})
            exception = False
        except:
            exception = True
        assert exception

    def test_init_incorrect_accounts(self):
        try:
           member_accounts = MemberAccounts('member-123', {'member-123': [{'coal': []}]}) 
           exception = False
        except:
            exception = True
        assert exception
        
        


class TestBillMember(unittest.TestCase):

    @patch('bill_member.get_readings')
    def test_calculate_bill_load_readings(self, mock_get_readings):
        _,_ = calculate_bill()
        assert mock_get_readings.called



    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)


if __name__ == '__main__':
    unittest.main()
