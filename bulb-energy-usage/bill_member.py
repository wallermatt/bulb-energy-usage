from load_readings import get_readings


class MemberAccounts():
    ACCOUNTS_INITIAL = {'electricity': None, 'gas': None}
    
    def __init__(self, member_id, readings):
        self.member_id = member_id
        if self.member_id not in readings:
            raise('Member ID not in readings')
        account_readings = readings[self.member_id]
        
        

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
