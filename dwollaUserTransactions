import re
from datetime import date
from dwolla import DwollaUser, DwollaClientApp

# User information
token = 'ENTER OAUTH TOKEN HERE'
DwollaUser = DwollaUser(token)


# Print user balance information
balance = DwollaUser.get_balance()
userID = DwollaUser.get_account_info()
print(userID['Name'] + ' (' + userID['Id'] + '), your current Dwolla balance is: $' + str(balance) + '\n')


# Get a list of user transactions
transactions = DwollaUser.get_transaction_list()
if len(transactions) >= 5:
    rVal = range(4,-1, -1)
else:
    rVal = range(len(transactions)-1, 0, -1)

print('Displaying summary data for your last ' + str(len(rVal)) + ' transactions')

# Print out individual transaction records
for val in rVal:
    # Get transaction ID number
    transaction_id = transactions[val]['Id']
    
    # Use ID number to get transaction metadata
    transaction = DwollaUser.get_transaction(transaction_id)
    
    # Format transaction amount to be $DD.CC
    transAmount = str(transaction['Amount'])
    if re.search('\d*.\d\d', transAmount) == None:
        transAmount = transAmount + '0'
    
    # Get date of transaction
    transDate = str(transaction['Date'])
    mm = int(transDate[5:7])
    yy = int(transDate[0:4])
    dd = int(transDate[8:10])
    transStr = date(yy, mm, dd).strftime('%A, %b %d, %Y')
    
    # Get clearance date of future transactions (if any)
    clearDate = str(transaction['ClearingDate'])
    if len(clearDate) > 0:
        mm = int(clearDate[5:7])
        yy = int(clearDate[0:4])
        dd = int(clearDate[8:10])
        clearStr = date(yy, mm, dd).strftime('%A, %b %d, %Y')
    
        print('Transaction #' + str(5-val) + ': ' +  transaction['Source']['Name'] + ' sent $' + transAmount +  
              ' to ' + transaction['Destination']['Name'] + ' on ' + transStr + ' (scheduled to clear on ' +
              clearStr + ')')
    else:
        print('Transaction #' + str(5-val) + ': ' +  transaction['Source']['Name'] + ' sent $' + transAmount +  
          ' to ' + transaction['Destination']['Name'] + ' on ' + transStr)
