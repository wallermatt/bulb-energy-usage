import datetime
import unittest

from unittest.mock import patch

from bill_member import calculate_bill, Member, Account, Reading


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

    READINGS1 =  [{
        "electricity": [
            {
                "cumulative": 17580,
                "readingDate": "2017-03-28T00:00:00.000Z",
                "unit": "kWh"
            },
            {
                "cumulative": 15580,
                "readingDate": "2017-02-28T00:00:00.000Z",
                "unit": "kWh"
            }
        ]
    }]

    def test_init_account_id(self):
        account = Account('account-abc', self.READINGS1)
        self.assertEqual(account.account_id, 'account-abc')

    def test_init_billing_readings_len(self):
        account = Account('account-abc', self.READINGS1)
        self.assertEqual(len(account.billing_readings['electricity']), 2)

    def test_init_billing_readings_instance(self):
        account = Account('account-abc', self.READINGS1)
        self.assertIsInstance(account.billing_readings['electricity'][0], Reading)
        self.assertIsInstance(account.billing_readings['electricity'][1], Reading)

    def test_init_billing_readings_sort(self):
        account = Account('account-abc', self.READINGS1)
        self.assertEqual(account.billing_readings['electricity'][0].reading_date, datetime.datetime(2017, 2, 28, 0, 0))

    def test_get_month_reading_for_datetime(self):
        account = Account('account-abc', self.READINGS1)
        reading = account.get_month_reading_for_datetime('electricity', datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(reading.reading_date, datetime.datetime(2017, 3, 28, 0, 0))

    def test_get_month_reading_for_datetime_exception(self):
        account = Account('account-abc', self.READINGS1)
        with self.assertRaises(Exception) as context:
            reading = account.get_month_reading_for_datetime('electricity', datetime.datetime(2020, 3, 15, 0, 0))

    def test_calculate_monthly_bill_for_billing_type(self):
        account = Account('account-abc', self.READINGS1)
        amount, units = account.calculate_monthly_bill_for_billing_type('electricity', datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(amount, 24659.36)
        self.assertEqual(units, 2000)

    def test_calculate_monthly_bill(self):
        account = Account('account-abc', self.READINGS1)
        amount, units = account.calculate_monthly_bill(datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(amount, 24659.36)
        self.assertEqual(units, 2000)


class TestMember(unittest.TestCase):

    READINGS1 =  {
        'member-123' : [
            {
                'account-abc' : [{
                    "electricity": [
                        {
                            "cumulative": 17580,
                            "readingDate": "2017-03-28T00:00:00.000Z",
                            "unit": "kWh"
                        },
                        {
                            "cumulative": 15580,
                            "readingDate": "2017-02-28T00:00:00.000Z",
                            "unit": "kWh"
                        }
                    ]
                }]
            }
        ]
    }

    def test_init_member_id(self):
        member = Member('member-123', self.READINGS1)
        self.assertEqual(member.member_id, 'member-123')

    def test_init_id_not_in_readings(self):
        with self.assertRaises(Exception) as context:
            _ = Member('member-123', {})

    def test_init_member_accounts(self):
        member = Member('member-123', {'member-123': [{'account-abc': []}]})
        self.assertIn('account-abc', member.accounts)

    def test_init_accounts(self):
        member = Member('member-123', self.READINGS1)
        self.assertIn('account-abc', member.accounts)
        self.assertEqual(len(member.accounts['account-abc'].billing_readings['electricity']), 2)

    def test_calculate_monthly_bill_for_account(self):
        member = Member('member-123', self.READINGS1)
        amount, units = member.calculate_monthly_bill_for_account('account-abc', datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(amount, 24659.36)
        self.assertEqual(units, 2000)

    def test_calculate_monthly_bill(self):
        member = Member('member-123', self.READINGS1)
        amount, units = member.calculate_monthly_bill(datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(amount, 24659.36)
        self.assertEqual(units, 2000)
        
        

class TestBillMember(unittest.TestCase):

    @patch('bill_member.get_readings')
    def test_calculate_bill_load_readings(self, mock_get_readings):
        with self.assertRaises(Exception) as context:
            _,_ = calculate_bill('member-123', '2017-08-31')
        assert mock_get_readings.called

    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(
            'member-123',
            '2017-08-31'
        )
        self.assertEqual(amount, 27.56843)
        self.assertEqual(kwh, 167)


if __name__ == '__main__':
    unittest.main()
