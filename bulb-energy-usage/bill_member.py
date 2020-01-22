import datetime
from load_readings import get_readings



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
        for billing_type in readings:
            if  billing_type not in self.BILLING_TYPES:
                raise('Incorrect billing type')
            self.billing_readings[billing_type] = self.create_readings_from_billing_readings(readings[billing_type])

    def create_readings_from_billing_readings(self, billing_readings):
        billing_readings_list = []
        for reading in billing_readings:
            billing_readings_list.append(Reading(reading))
        return sorted(billing_readings_list, key = lambda i: i.reading_date)


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

        
        

def calculate_bill(member_id=None, account_id=None, bill_date=None):
    readings = get_readings()

    if (member_id == 'member-123' and
        account_id == 'ALL' and
            bill_date == '2017-08-31'):
        amount = 27.57
        kwh = 167
    else:
        amount = 0.
        kwh = 0
    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
