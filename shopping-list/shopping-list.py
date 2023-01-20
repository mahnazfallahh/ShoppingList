import os
import json
import toml
import typing
import logging
import pandas as pd
import logging.config
from enum import Enum
from dataclasses import dataclass
from exceptiontest import NameISNotStringException



logging.config.fileConfig(fname = 'Log/config.toml', disable_existing_loggers= False)
logger = logging.getLogger(__name__)
logging = logging.getLogger('admin')



grocery_items:dict = dict()
cosmetics_items:dict = dict()
vegetable_items:dict = dict()
cosmetics_bill:list = list()
vegetable_bill:list = list()
grocery_bill:list = list()
register_information:dict = dict()


class ExitCommand(Enum):
    q = 'q'


@dataclass
class EnterUserName:
    first_name : str
    last_name : str

    def __str__(self):
        return f'{self.first_name}{self.last_name}'



def buy_categories(categories,
category_bill:list[int],
bill_name:str,
account_balance:int,) ->int:
    category = json.load(categories)
    lines = [line for line in category]
    with open('shopping-list.json') as files:
        data = json.load(files)
        for line in lines:
            for key, value in data.items():
                if line == key:
                    price = data[line]['price']
                    product_number = int(category.get(line))
                    total_sum = price * product_number
                    category_bill.append(total_sum)
                    bill = sum(category_bill)
                    if bill > account_balance:
                        print("OOoops, sorry ! you don't have enough money to buy your list.")
                    else:
                        balance = account_balance - bill
                        print('The purchase was made successfully!!')
                        print(f"your account balance is : {balance}")
        print(f" your {bill_name} bill is : {bill} dollars.")


def grocery_price():
    data = {
        '': [90000, 1000, 80000]
    }
    grocery = pd.DataFrame(data, index=['walnut', 'rice', 'sugar'])
    print(grocery)



def vegetable_price():
    data = {
        '': [4000, 40000, 1000]
    }
    vegetable = pd.DataFrame(data, index=['cucumber', 'carrot', 'lettuce'])
    print(vegetable)



def cosmetics_price():
    data = {
        '': [3400000, 1200, 340000]
    }
    cosmetics = pd.DataFrame(data, index=['lipstick', 'cream', 'spray'])
    print(cosmetics)


def register_user(user_name:str, password:any):
        if len(password) <= 3:
            print('your password is too short.')
        else:
            with open('register.json', 'w') as register:
                register_information[user_name] = password
                json.dump(register_information, register)
                print('register successfully done !')
                logging.info(f"{user_name} registered successfully.")


def login_user(user_name:str, password:any):
    with open('register.json') as login_user:
        login = json.load(login_user)
        if user_name in login:
                print('you logged in successfully!')
                logging.info(f'{user_name} logged in successfully')
        else:
            print('user name or password does not exist please register .')


def show_category(files):
    data = json.load(files)
    for key in data.keys():
        print(key)


def display_help():
    """ func to display help commands """
    with open('help.txt') as files:
        data = files.read()
        print(data)



def add_stars(func):
    def stars():
        print('************************************************')
        func()
        print('************************************************')
    return stars()

@add_stars
def show_help():
    """ func to display help commands"""
    print('there is 3 category in shopping list')
    print('to buy multiple lists if you want buy one list enter ---> ONE')
    print('to buy multiple lists if you want buy two lists enter ---> TWO')
    print('to buy multiple lists if you want buy all lists enter ---> ALL')
    print('to access in categories enter the number of lists below')
    print('1) Grocery')
    print('2) Cosmetics')
    print('3) Vegetable')
    



def clear_screen():
    """ func to clear screen"""
    # Clear the terminal screen
    return os.system('cls')
# call func display help
display_help()
# first_name = input('please enter your firstname:')
# last_name = input('please enter your lastname:')
# try:
#     if first_name.isnumeric():
#         raise NameISNotStringException
# except NameISNotStringException as e:
#     print(e)
# else:
#     information = EnterUserName(first_name, last_name)
#     print(f"Hi {information} . welcome to shopping list. ")
#     logger.info('hi')
    
os.system ('pause')



option = input("do you want to login or register ?")
# condition if option equal to login
if option == 'login':
    user_name = input('please enter your user name :')
    password = input('please enter your password:')
# call login func
    login_user(user_name, password)
# condition if option equal to register
elif option == 'register':
    user_name = input('please enter your user name :')
    password = input('please enter your password:')
    register_user(user_name, password)
    print("to continue please login.")
    user_name = input('please enter your user name :')
    password = input('please enter your password:')
# call login func
    login_user(user_name, password)
else:
    print('enter valid option !!')


# define a loop
while True:
    # question from user
    user_input = input('please enter one options in menu:').casefold()
    for command in ExitCommand:
        value = command.value
    if user_input == value:
        print('you exit from SHOPPING LIST !')
        print('HOPE TO SEE YOU SOON !')
        logger.info('user exited from shop !!!!')
        # exit from condition
        break
    # condition if user input equal to add
    elif user_input == 'add':
        # question from user
        
        question = input('which category do you want to add ?').casefold()
        # call clearscreen fnc()
        clear_screen()
        # condition if question equal to 1
        if question == '1':
            with open('grocery-items.json' , 'r+') as user_list:
                with open('shopping-list.json') as groceries:
                    grocery = json.load(groceries)
                    # question from user
                    items_number = int(input('how many items do you want add ?'))
                    # loop to iterate in items
                    for item in range(items_number):
                        # question from user
                        items = input('please enter your grocery items: ')
                        number_items = input('how many do you want from this item ?')
                        if items not in grocery:
                            print('no such item is in shopping list.')
                        else:
                            grocery_items[items] = number_items
                            print('item added successfully!!!')
                            logger.info('user add item into grocery list')
                    json.dump(grocery_items, user_list )
        elif question == '2':
            with open('cosmetics-items.json' , 'r+') as user_list:
                with open('shopping-list.json') as cosmetics:
                    cosmetic = json.load(cosmetics)
                    # question from user
                    items_number = int(input('how many items do you want add ?'))
                    # loop to iterate in items
                    for item in range(items_number):
                        # question from user
                        items = input('please enter your cosmetics items: ')
                        number_items = input('how many do you want from this item ?')
                        if items not in cosmetic:
                            print('no such item is in shopping list.')
                        else:
                            cosmetics_items[items] = number_items
                            print('item added successfully!!!')
                            logger.info('user add item into grocery list')
                    json.dump(cosmetics_items, user_list )
        elif question == '3':
            with open('vegetable-items.json' , 'r+') as user_list:
                with open('shopping-list.json') as vegetables:
                    vegetable = json.load(vegetables)
                    # question from user
                    items_number = int(input('how many items do you want add ?'))
                    # loop to iterate in items
                    for item in range(items_number):
                        # question from user
                        items = input('please enter your vegetable items: ')
                        number_items = input('how many do you want from this item ?')
                        if items not in vegetable:
                            print('no such item is in shopping list.')
                        else:
                            vegetable_items[items] = number_items
                            print('item added successfully!!!')
                            logger.info('user add item into grocery list')
                    json.dump(vegetable_items, user_list )
        else:
            print('please enter valid number of category.')

    elif user_input == 'price':
        # show_help()
        question = input('which category do you want to see items prices?')
        clear_screen()
        if question == '1':
            print("********GROCERY PRICES **********")
            grocery_price()
        elif question == '2':
            print("********COSMETICS PRICES **********")
            cosmetics_price()
        elif question == '3':
            print("********VEGETABLE PRICES **********")
            vegetable_price()
        else:
            print('please enter valid category.')
    
        
    elif user_input == 'buy':
        # show_help()
        account_balance =int(input('please enter your account balance :'))
        clear_screen()
        question = input('which category do you want to buy ?')
        if question == '1':
            grocery = 'grocery'
            with open('grocery-items.json') as groceries:
                buy_categories(groceries, grocery_bill, grocery, account_balance)
        elif question == '2':
            cosmetic = 'cosmetic'
            with open('cosmetics-items.json') as cosmetics:
                buy_categories(cosmetics, cosmetics_bill, cosmetic, account_balance)
        elif question == '3':
            vegetable = 'vegetable'
            with open('vegetable-items.json') as vegetables:
                buy_categories(vegetables, vegetable_bill, vegetable, account_balance )
        else:
            print('invalid category .')
            
    elif user_input == 'show':
        # show_help()
        question = input('which category do you want to see ?')
        clear_screen()
        if question == '2':
            with open('cosmetics-items.json', 'r') as files:
                show_category(files)
                logger.info('user watched items into grocery list')
        elif question == '3':
            with open('vegetable-items.json', 'r') as files:
                show_category(files)
                logger.info('user watched items into grocery list')
        elif question == '1':
            with open('grocery-items.json', 'r') as files:
                show_category(files)
                logger.info('user watched items into grocery list')
        else:
            print('invalid category.')

    elif user_input == 'remove':
        # show_help()
        question = input('which category do you want to remove?')
        clear_screen()
        if question == '1':
            with open('grocery-items.json') as grocery:
                data = json.load(grocery)
                item = input('which item do you want to remove ?')
                if item in data:
                    data.pop(item)
                    with open('grocery-items.json', 'w') as files:
                        json.dump(data, files)
                        print(f'{item} removes from grocery list.')
                        logger.info(f'user removed {item} into grocery list')
                else:
                    print('no such item is in shopping list.')
        if question == '2':
            with open('cosmetics-items.json') as cosmetics:
                data = json.load(cosmetics)
                item = input('which item do you want to remove ?')
                if item in data:
                    data.pop(item)
                    with open('cosmetics-items.json', 'w') as files:
                        json.dump(data, files)
                        print(f'{item} removes from cosmetics list.')
                        logger.info(f'user removed {item} into grocery list')
                else:
                    print('no such item is in shopping list.')
        if question == '3':
            with open('vegetable-items.json') as vegetable:
                data = json.load(vegetable)
                item = input('which item do you want to remove ?')
                if item in data:
                    data.pop(item)
                    with open('vegetable-items.json', 'w') as files:
                        json.dump(data, files)
                        print(f'{item} removes from vegetable list.')
                        logger.info(f'user removed {item} into grocery list')
                else:
                    print('no such item is in shopping list.')
        else:
            print('invalid category.')
            
    elif user_input == 'edit':
        # show_help()
        edit_question = input('which category do you want to edit ? ')
        clear_screen()
        if edit_question == '1':
            with open('shopping-list.json') as files:
                data = json.load(files)
                with open('grocery-items.json') as groceries:
                    grocery = json.load(groceries)
                    edit_item = input('enter which item do you want edit it ?')
                    item_edit_with = input('enter which item do you want edit it with?')
                    if edit_item in grocery:
                        if item_edit_with in data:
                            grocery[item_edit_with] = grocery.pop(edit_item)
                            with open('grocery-items.json', 'w') as files:
                                json.dump(grocery, files)
                                print(f'{edit_item} modified into {item_edit_with} in your grocery list.')
                                logger.info(f'{edit_item} modified into {item_edit_with} in your grocery list.')
                        else:
                            print('no such item is in shopping list.')
                    else:
                        print('no such item is in shopping list.')
        if edit_question == '2':
            with open('shopping-list.json') as files:
                data = json.load(files)
                with open('cosmetics-items.json') as cosmetics:
                    cosmetic = json.load(cosmetics)
                    edit_item = input('enter which item do you want edit it ?')
                    item_edit_with = input('enter which item do you want edit it with?')
                    if edit_item in cosmetic:
                        if item_edit_with in data:
                            cosmetic[item_edit_with] = cosmetic.pop(edit_item)
                            with open('cosmetics-items.json', 'w') as files:
                                json.dump(cosmetic, files)
                                print(f'{edit_item} modified into {item_edit_with} in your cosmetics list.')
                                logger.info(f'{edit_item} modified into {item_edit_with} in your grocery list.')
                        else:
                            print('no such item is in shopping list.')
                    else:
                        print('no such item is in shopping list.')
        if edit_question == '3':
            with open('shopping-list.json') as files:
                data = json.load(files)
                with open('vegetable-items.json') as vegetables:
                    vegetable = json.load(vegetables)
                    edit_item = input('enter which item do you want edit it ?')
                    item_edit_with = input('enter which item do you want edit it with?')
                    if edit_item in vegetable:
                        if item_edit_with in data:
                            vegetable[item_edit_with] = vegetable.pop(edit_item)
                            with open('vegetable-items.json', 'w') as files:
                                json.dump(vegetable, files)
                                print(f'{edit_item} modified into {item_edit_with} in your vegetable list.')
                                logger.info(f'{edit_item} modified into {item_edit_with} in your grocery list.')
                        else:
                            print('no such item is in shopping list.')
                    else:
                        print('no such item is in shopping list.')
        else:
            print('invalid category.')

                    
    elif user_input == 'search':
        # show_help()
        search_question = input('which category do you want to search ?')
        clear_screen()
        if search_question == '1':
            search_item = input('please enter your intended item :')
            with open('grocery-items.json')  as files:
                data = json.load(files)
                if search_item in data:
                    print(f'item you searched is : {search_item}')
                    logger.info(f" user searched {search_item} in grocery list .")
                else:
                    print('item is not into the list')
        elif search_question == '2':
            search_item = input('please enter your intended item :')
            with open('cosmetics-items.json')  as files:
                data = json.load(files)
                if search_item in data:
                    print(f'item you searched is : {search_item}')
                    logger.info(f" user searched {search_item} in grocery list .")
                else:
                    print('item is not into the list')
        elif search_question == '3':
            search_item = input('please enter your intended item :')
            with open('vegetable-items.json')  as files:
                data = json.load(files)
                if search_item in data:
                    print(f'item you searched is : {search_item}')
                    logger.info(f" user searched {search_item} in grocery list .")
                else:
                    print('item is not into the list')
        else:
            print('invalid category.')
    else:
        print('invalid option.')
