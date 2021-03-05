#
# Program to display account information for testing the ATM program
#
# The main data structure is a dictionary with account numbers
# (represented by strings) as keys, and account details as values.
#
# Details of an account are stored in a dictionary with the following
# keys and values:
#
# "pin" : the PIN, as a string
# "balance" : the account balance, as a floating point number
# "transactions" : a list of the last 6 transactions
#
# One transaction is stored as a dictionary with the following
# keys and values:
#
# "date" : the date and time, as a string
# "nature" : a string, "w" for withdrawal, "d" for deposit
# "amount" : the amount of withdrawal or deposit, as a floating point number
#
# This program loads a pickled dictionary and displays the information.

import pickle

filename = input("Enter the file name: ")

with open(filename,"rb") as f:
    bank = pickle.load(f)


for account in bank:
    details = bank[account]
    print("Account: ", account)
    pin = details["pin"]
    balance = details["balance"]
    transactions = details["transactions"]
    print("PIN: ", pin)
    print("Balance: ", "%.2f" % balance)
    print("Recent transactions:")
    for trans in transactions:
        print(trans["date"], trans["nature"], "%.2f" % trans["amount"])
    print()

