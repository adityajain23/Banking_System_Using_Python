import sqlite3
import random

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""
CREATE TABLE if not exists card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
)""")
conn.commit()

count = 1


def starting_page():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    print("> ", end = "")


def login_page():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    print("> ", end = "")


def creating_pin_and_card_number():
    a = random.randint(0, 9999999999)
    card_number = 4000000000000000 + a
    card_number = str(card_number)
    sum_of_numbers = 0
    for i in range(0,15):
        integer_value = int(card_number[i])
        if i%2==0:
            if 2*integer_value > 9:
                sum_of_numbers += 2*integer_value - 9
            else:
                sum_of_numbers += 2*integer_value
        else:
            sum_of_numbers += integer_value
    check_sum = (10 - sum_of_numbers % 10) % 10
    card_number = card_number[:-1] + str(check_sum)
    pin_number = random.randint(1000, 9999)
    return str(card_number), str(pin_number)


def show_balance(account):
    print("Your Balance is: ", account[3])


def add_income(account):
    while(True):
        try:
            print("Enter Income:")
            print("> ",end="")
            added_income = int(input())
            break
        except:
            print("\nYou have Entered the value in wrong format!!")
            print("Please try again!!\n")

    cur.execute("DELETE FROM card WHERE number = %s" % account[1])
    account[3] += added_income
    cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (%d, %s, %s, %d)'
                % (account[0], account[1], account[2], account[3]))
    conn.commit()

    print("Income was added!")


def do_transfer(account):
    print("Transfer")
    print("Enter card number:")
    print("> ",end="")
    card_number = input()
    if len(card_number) != 16:
        print("You have entered a wrong card number!!")
        print("PLease try again!!")
        return 
    try:
        card_number = int(card_number)
        card_number = str(card_number)
    except:
        print("\nYou have entered a value with wrong format!!\n")
        return 
            
    sum_of_numbers = 0
    for i in range(0,16):
        integer_value = int(card_number[i])
        if i%2==0:
            if 2*integer_value > 9:
                sum_of_numbers += 2*integer_value - 9
            else:
                sum_of_numbers += 2*integer_value
        else:
            sum_of_numbers += integer_value
    if (sum_of_numbers % 10 !=0):
        print("Probably you made a mistake in the card number. Please try again!")
        return
    else:
        cur.execute("SELECT id, number, pin, balance FROM card WHERE number = %s" % card_number)
        check_for_existence = cur.fetchall()
        if (len(check_for_existence)):
            if (account[1] == card_number):
                print("You can't transfer money to the same account!")
            else:
                while(True):
                    try:
                        print("Enter how much money you want to transfer:")
                        print("> ",end = "")
                        transfer_amount = int(input())
                        break
                    except:
                        print("\nYou have Entered the value in wrong format!!")
                        print("Please try again!!\n")
                        
                if transfer_amount > account[3]:
                    print("Not enough money!")
                else:
                    account[3] -= transfer_amount
                    cur.execute("DELETE FROM card WHERE number = %s" % account[1])
                    cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (%d, %s, %s, %d)'
                                % (account[0], account[1], account[2], account[3]))

                    transferAmount_AccountHolder = list(check_for_existence[0])
                    transferAmount_AccountHolder[3] += transfer_amount
                    cur.execute("DELETE FROM card WHERE number = %s" % transferAmount_AccountHolder[1])
                    cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (%d, %s, %s, %d)'
                                % (transferAmount_AccountHolder[0], transferAmount_AccountHolder[1], transferAmount_AccountHolder[2], transferAmount_AccountHolder[3]))
                    conn.commit()

                    print("Success!")
        else:
            print("Such a card does not exist.")
            return

while(True):
    try:
        starting_page()
        user_input = int(input())
        print()
        break
    except:
        print("\nYou have entered a value with wrong format!!")
        print("Please try again!!\n")

while user_input:
    if user_input == 1:
        print("Your card has been created")
        card_number, pin_number = creating_pin_and_card_number()
        print("Your card number: \n{}".format(card_number))
        print("Your card PIN: \n{}".format(pin_number))

        cur.execute('INSERT INTO card (id, number, pin) VALUES (%d, %s, %s)' % (count, card_number, pin_number))
        count += 1
        conn.commit()
        print()
        while(True):
            try:
                starting_page()
                user_input = int(input())
                print()
                break
            except:
                print("\nYou have entered a value with wrong format!!")
                print("Please try again!!\n")
                
    elif user_input == 2:
        print("Enter your card number:")
        user_card = input()
        if len(user_card) != 16:
            print("You have entered a wrong card number!!")
            print("PLease try again!!")
            print()
            while(True):
                try:
                    starting_page()
                    user_input = int(input())
                    print()
                    break
                except:
                    print("\nYou have entered a value with wrong format!!")
                    print("Please try again!!\n")
            continue
        else:
            try:
                user_card = int(user_card)
                user_card = str(user_card)
            except:
                print("\nYou have entered a value with wrong format!!\n")
                starting_page()
                user_input = int(input())
                print()
                continue

        print("Enter your PIN:")
        user_pin = input()
        if len(user_pin) != 4:
            print("You have entered a wrong pin number!!")
            print("Please try again!!")
            print()
            while(True):
                try:
                    starting_page()
                    user_input = int(input())
                    print()
                    break
                except:
                    print("\nYou have entered a value with wrong format!!")
                    print("Please try again!!\n")
            continue
        else:
            try:
                user_pin = int(user_pin)
                user_pin = str(user_pin)
            except:
                print("\nYou have entered a value with wrong format!!\n")
                starting_page()
                user_input = int(input())
                print()
                continue
                
        print()
        cur.execute("""
            SELECT 
                id,
                number,
                pin,
                balance
            FROM 
                card 
            WHERE 
                number = %s and pin = %s """ % (user_card, user_pin))

        information = cur.fetchall()

        if len(information):

            print("You have successfully logged in!")
            while(True):
                try:
                    login_page()
                    inner_user_input = int(input())
                    print()
                    break
                except:
                    print("\nYou have entered a value with wrong format!!")
                    print("Please try again!!\n")
                    
            while inner_user_input:
                cur.execute("""
                    SELECT 
                        id,
                        number,
                        pin,
                        balance
                    FROM 
                        card 
                    WHERE 
                        number = %s and pin = %s """ % (user_card, user_pin))

                information = cur.fetchall()
                if inner_user_input == 1:
                    show_balance(list(information[0]))
                    print()
                    while(True):
                        try:
                            login_page()
                            inner_user_input = int(input())
                            print()
                            break
                        except:
                            print("\nYou have entered a value with wrong format!!")
                            print("Please try again!!\n")
                            
                elif inner_user_input == 2:
                    add_income(list(information[0]))
                    print()
                    while(True):
                        try:
                            login_page()
                            inner_user_input = int(input())
                            print()
                            break
                        except:
                            print()
                            print("You have entered a value with wrong format")
                            
                elif inner_user_input == 3:
                    do_transfer(list(information[0]))
                    print()
                    while(True):
                        try:
                            login_page()
                            inner_user_input = int(input())
                            print()
                            break
                        except:
                            print("\nYou have entered a value with wrong format!!")
                            print("Please try again!!\n")
                            
                elif inner_user_input == 4:
                    while(True):
                        try:
                            print("Do you really want to delete your account!!\n")
                            print("1. Yes")
                            print("0. No")
                            print("> ",end="")
                            confirm_input = int(input())
                            break
                        except:
                            print("\nYou have entered a value with wrong format!!")
                            print("Please try again!!\n")
                            
                    if confirm_input != 1:
                        print()
                        while(True):
                            try:
                                login_page()
                                inner_user_input = int(input())
                                print()
                                break
                            except:
                                print("\nYou have entered a value with wrong format!!")
                                print("Please try again!!\n")
                    else:
                        cur.execute("DELETE FROM card WHERE number = %s" % user_card)
                        conn.commit()
                        print()
                        print("The account has been closed!")
                        print()
                        while(True):
                            try:
                                starting_page()
                                user_input = int(input())
                                print()
                                break
                            except:
                                print("\nYou have entered a value with wrong format!!")
                                print("Please try again!!\n")
                        break
                    
                elif inner_user_input == 5:
                    print("You have successfully logged out!")
                    print()
                    while(True):
                        try:
                            starting_page()
                            user_input = int(input())
                            print()
                            break
                        except:
                            print("\nYou have entered a value with wrong format!!")
                            print("Please try again!!\n")
                    break
                    
                else:
                    print("You have given a wrong input!!")
                    print("Please try again!!")
                    print()
                    while(True):
                        try:
                            login_page()
                            inner_user_input = int(input())
                            print()
                            break
                        except:
                            print("\nYou have entered a value with wrong format!!")
                            print("Please try again!!\n")
        
            if inner_user_input == 0:
                user_input = 0

        else:
            print("Wrong card number or PIN!")
            print()
            while(True):
                try:
                    starting_page()
                    user_input = int(input())
                    print()
                    break
                except:
                    print("\nYou have entered a value with wrong format!!")
                    print("Please try again!!\n")

    else:
        print("You have given a wrong input!!")
        print("Please try again!!")
        print()
        while(True):
            try:
                starting_page()
                user_input = int(input())
                print()
                break
            except:
                print("\nYou have entered a value with wrong format!!")
                print("Please try again!!\n")

print("Bye!")