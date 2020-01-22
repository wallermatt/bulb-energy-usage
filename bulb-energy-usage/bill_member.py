import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from load_readings import get_readings
from tariff import BULB_TARIFF


class Reading():

    UNIT_TYPES = ('kWh')

    def __init__(self, reading):
        self.reading_date = datetime.datetime.strptime(reading['readingDate'][0:10], "%Y-%m-%d")
        self.cumulative = reading['cumulative']
        if reading['unit'] not in self.UNIT_TYPES:
            raise('Incorrect unit type')
        self.unit = reading['unit']
        

class Account():

    BILLING_TYPES = ('electricity', 'gas')

    def __init__(self, account_id, readings):
        self.account_id = account_id
        self.billing_readings = {}
        for dict_ in readings:
            for billing_type in dict_:
                if  billing_type not in self.BILLING_TYPES:
                    raise('Incorrect billing type')
                self.billing_readings[billing_type] = self.create_readings_from_billing_readings(dict_[billing_type])

    def create_readings_from_billing_readings(self, billing_readings):
        billing_readings_list = []
        for reading in billing_readings:
            billing_readings_list.append(Reading(reading))
        return sorted(billing_readings_list, key = lambda i: i.reading_date)

    def get_month_reading_for_datetime(self, billing_type, datetime_):
        readings = self.billing_readings[billing_type]
        for reading in readings:
            if reading.reading_date.year == datetime_.year and reading.reading_date.month == datetime_.month:
                return reading
        raise('No matching reading')

    def calculate_monthly_bill_for_billing_type(self, billing_type, billing_date):
        billing_date_reading = self.get_month_reading_for_datetime(billing_type, billing_date)
        previous_month = billing_date - relativedelta(months=1)
        previous_month_reading = self.get_month_reading_for_datetime(billing_type, previous_month)
        units_used = billing_date_reading.cumulative - previous_month_reading.cumulative
        num_days_in_month = monthrange(billing_date.year, billing_date.month)[1]
        amount = num_days_in_month * BULB_TARIFF[billing_type]['standing_charge'] + units_used * BULB_TARIFF[billing_type]['unit_rate']
        return amount, units_used

    def calculate_monthly_bill(self, billing_date):
        total_amount = 0
        total_units = 0
        for billing_type in self.billing_readings:
            amount, units = self.calculate_monthly_bill_for_billing_type(billing_type, billing_date)
            total_amount += amount
            total_units += units
        return total_amount, total_units


class Member():
    
    def __init__(self, member_id, readings):
        self.member_id = member_id
        if self.member_id not in readings:
            raise('Member ID not in readings')
        self.accounts = self.create_accounts_from_readings(readings[self.member_id])

    def create_accounts_from_readings(self, member_readings):
        account_dict = {}
        for account in member_readings:
            account_id = list(account.keys())[0]
            account_dict[account_id] = Account(account_id, account[account_id])
        return account_dict

    def calculate_monthly_bill_for_account(self, account_id, billing_date):
        return self.accounts[account_id].calculate_monthly_bill(billing_date)

    def calculate_monthly_bill(self, billing_date, units_gbp=False):
        total_amount = 0
        total_units = 0
        for account_id in self.accounts:
            amount, units = self.calculate_monthly_bill_for_account(account_id, billing_date)
            total_amount += amount
            total_units += units
        return total_amount, total_units


def calculate_bill(member_id, bill_date, account_id='ALL'):
    billing_date = datetime.datetime.strptime(bill_date, "%Y-%m-%d")
    readings = get_readings()
    member = Member(member_id, readings)
    if account_id == 'ALL':
        amount, units =   member.calculate_monthly_bill(billing_date)
    else:
        amount, units =  member.calculate_monthly_bill_for_account(account_id, billing_date)
    return amount / 100, units


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, bill_date, account)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
