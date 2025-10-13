import datetime

import pandas as pd

from notion_api.lease import get_lease, lease_change_next_payment_date
from notion_api.payment import add_payment_row
from utility.bill_date_calculation import get_next_bill_date


def main():
    '''
    1. get all active lease
    2. find all leases that the today - 'Next Payment Date' == 7 days
    3. create payments for those lease
    4. update the 'Next Payment Date'
    :return:
    '''
    # get all active lease
    active_lease = get_lease()
    today = datetime.date.today()
    target_date = today + datetime.timedelta(days=1)  # 2025-10-17

    # Ensure 'Next Payment Date' is in datetime format (adjust column name if needed)
    active_lease['Next Payment Date'] = pd.to_datetime(active_lease['Next Payment Date'],
                                                       errors='coerce')  # Use 'Due Date' if applicable
    active_lease['Start Date'] = pd.to_datetime(active_lease['Start Date'],
                                                errors='coerce')  # Use 'Due Date' if applicable
    # Filter rows where Next Payment Date is 7 days from today
    filtered_df = active_lease[active_lease['Next Payment Date'].dt.date == target_date]
    print(filtered_df)

    # 3. create payments for those lease
    for index, row in filtered_df.iterrows():
        dict_payment = {
            "Payment Name": str(row['Room/Unit']) + ' ' + str(row['Next Payment Date'].strftime("%Y-%m")),
            "lease": [row['Page ID']],  # get the lease page id
            'Due Date': row['Next Payment Date'].strftime("%Y-%m-%d"),  # get the next due day from lease database
            'Rent Amount': row['Monthly Rent'],  # get the rent Amount
            'Status': 'Unpaid',
            'Payment Method': 'Cash',
        }
        print(dict_payment)
        add_payment_row(payment=[dict_payment])

        # get start date
        start_day = row['Start Date'].strftime("%d")

        next_bill_date = get_next_bill_date(row['Next Payment Date'].strftime("%Y-%m-%d"), int(start_day))
        print(next_bill_date)
        lease_id = row['Page ID']
        lease_change_next_payment_date(lease_id, next_bill_date)
        pass

    pass


if __name__ == '__main__':
    main()
