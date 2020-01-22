import datetime
import unittest

from unittest.mock import patch

from bill_member import calculate_bill, Member, Account, Reading
from test_readings import TEST_READINGS


class TestReading(unittest.TestCase):

    CORRECT_READING1 = {
          "cumulative": 17580,
          "readingDate": "2017-03-28T00:00:00.000Z",
          "unit": "kWh"
    }

    INVALID_READING1 = {
          "cumulative": 17580,
          "readingDate": "2017-03-28T00:00:00.000Z",
          "unit": "Calorie"
    }

    def test_init_read_date(self):
        reading = Reading(self.CORRECT_READING1)
        assert reading.reading_date == datetime.datetime(2017, 3, 28, 0, 0)

    def test_init_cumulative(self):
        reading = Reading(self.CORRECT_READING1)
        assert reading.cumulative == 17580

    def test_init_unit(self):
        reading = Reading(self.CORRECT_READING1)
        assert reading.unit == 'kWh'

    def test_init_invalid_unit(self):
        with self.assertRaises(Exception) as context:
            reading = Reading(self.INVALID_READING1)

class TestAccount(unittest.TestCase):

    READINGS1 =  {
        "electricity": [
            {
                "cumulative": 17580,
                "readingDate": "2017-03-28T00:00:00.000Z",
                "unit": "kWh"
            }
        ]
    }

    def test_init

class TestMember(unittest.TestCase):

    '''
    def test_accounts_types(self):
        assert Member.ACCOUNTS_INITIAL == {'electricity': None, 'gas': None}
    '''


    def test_init_member_id(self):
        member = Member('member-123', TEST_READINGS)
        assert member.member_id == 'member-123'

    def test_init_id_not_in_readings(self):
        with self.assertRaises(Exception) as context:
            _ = Member('member-123', {})

    def test_init_member_accounts(self):
        member = Member('member-123', {'member-123': [{'account-abc': []}]})
        assert 'account-abc' in member.accounts

    '''
    def test_init_incorrect_accounts(self):

        with self.assertRaises(Exception) as context:
            member_accounts = MemberAccounts('member-123', {'member-123': [{'coal': []}]})
    '''    
        
        


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
