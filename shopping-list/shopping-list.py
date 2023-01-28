import os
import json
import logging
import pandas as pd
import logging.config
from enum import Enum
from getpass import getpass
from dataclasses import dataclass
from helper.exceptions import NameISNotStringException
from helper.decorators import separator


# logging config files
logging.config.fileConfig(fname='Log/config.toml', disable_existing_loggers=False)  # noqa E501
logger = logging.getLogger(__name__)
logging = logging.getLogger('admin')
grocery_items: dict = dict()
cosmetics_items: dict = dict()
vegetable_items: dict = dict()
cosmetics_bill: list = list()
vegetable_bill: list = list()
grocery_bill: list = list()
register_information: dict = dict()


class ExitCommand(Enum):
    q = 'q'


@dataclass
class EnterUserName:
    first_name: str
    last_name: str

    def __str__(self):
        return f'{self.first_name}{self.last_name}'


def buy_categories(
    categories,
    category_bill: list[int],
    bill_name: str,
    account_balance: int,
) -> int:
    """ iterate in specific items in to the list and iterate in users items
    to access into number of products and prices.
    Parameters
    ----------
    var1 : categories
            categories is a variable which we open json file with it.
    var2 : category_bill
            is category bill parameter like grocery bill.
    var3 : bill_name
            as show as it is a variable for bill name.
    var4 : account_balance
            it's  account balance of user .
    """
    category: dict = json.load(categories)
    lines: list = [line for line in category]
    with open('database/shopping-list.json') as files:
        data: dict = json.load(files)
        for line in lines:
            for key, value in data.items():
                if line == key:
                    price: list = data[line]['price']
                    product_number: int = int(category.get(line))
                    total_sum: int = price * product_number
                    category_bill.append(total_sum)
                    bill: int = sum(category_bill)
                    if bill > account_balance:
                        print("OOoops, sorry ! you don't have enough money to buy your list.")  # noqa E501
                    else:
                        balance: int = account_balance - bill
                        print('The purchase was made successfully!!')
                        print(f"your account balance is : {balance}")
        print(f" your {bill_name} bill is : {bill} dollars.")


def grocery_price():
    """ function for display grocery prices and items in one simple table """
    data = {
        '': [90000, 1000, 80000]
    }
    grocery = pd.DataFrame(data, index=['walnut', 'rice', 'sugar'])
    print(grocery)


def vegetable_price():
    """ function for display vegetable prices and items in one simple table """
    data = {
        '': [4000, 40000, 1000]
    }
    vegetable = pd.DataFrame(data, index=['cucumber', 'carrot', 'lettuce'])
    print(vegetable)


def cosmetics_price():
    """ function for display cosmetics prices and items in one simple table """
    data = {
        '': [3400000, 1200, 340000]
    }
    cosmetics = pd.DataFrame(data, index=['lipstick', 'cream', 'spray'])
    print(cosmetics)


def register_user(user_name: str, password: any):
    """ write user name and password in json file and register . # noqa E501    
    Parameters
    ----------
    var1 : user_name
            username which received from user .
    var2 : password
            password which received from user .

    """
    if len(password) <= 3:
        print('your password is too short.')
    else:
        with open('database/register.json', 'w') as register:
            register_information[user_name] = password
            json.dump(register_information, register)
            print('register successfully done !')
            logging.info(f"{user_name} registered successfully.")


def login_user(user_name: str, password: any):
    """ read user name and password in json file and login . # noqa E501    
    Parameters
    ----------
    var1 : user_name
            username which received from user .
    var2 : password
            password which received from user .

    """
    with open('database/register.json') as login_user:
        login = json.load(login_user)
        if user_name in login:
            print('you logged in successfully!')
            logging.info(f'{user_name} logged in successfully')
        else:
            print('user name or password does not exist in to the shopping list.')  # noqa E501
            print('we are trying register you with current username which you tried login.')  # noqa E501
            print('**********************************************************************')  # noqa E501
            register_user(user_name, password)


def show_category(files):
    """ function for iterate into the json file to display items of categories.
    Parameters
    ----------
    var1 : files
    """
    data: dict = json.load(files)
    for key in data.keys():
        print(key)


def display_help():
    """ function to display help commands """
    with open('database/help.txt') as files:
        data: dict = files.read()
        print(data)


def add_stars(func):
    """ decorator function to add stars."""
    def stars():
        print('************************************************')
        func()
        print('************************************************')
    return stars()


@separator
def show_help():
    """ func to display help commands"""
    print('to access in categories enter the number of lists below')
    print('1) Grocery')
    print('2) Cosmetics')
    print('3) Vegetable')

display_help()


while True:
    first_name = input('please enter your firstname:')
    last_name = input('please enter your lastname:')
    try:
        if first_name.isnumeric():
            raise NameISNotStringException
    except NameISNotStringException as e:
        print(e)
    else:
        information = EnterUserName(first_name, last_name)
        print(f"Hi {information} . welcome to shopping list. ")
        logger.info(f'user {first_name} {last_name} arrived into shopping list.')  # noqa E501
        break
os.system ('pause')


while True:
    option = input("do you want to login or register ?")
    # condition if option equal to login
    if option == 'login':
        while True:
            user_name = input('please enter your user name :')
            if not len(user_name.strip()):
                print('invalid option please try again .')
            else:
                break
        password = getpass('please enter your password:')
    # call login func
        login_user(user_name, password)
    # condition if option equal to register
        break
    elif option == 'register':
        user_name = input('please enter your user name :')
        password = getpass('please enter your password:')
        register_user(user_name, password)
        print("to continue please login.")
        user_name = input('please enter your user name :')
        password = input('please enter your password:')
    # call login func
        login_user(user_name, password)
        break
    else:
        print('enter valid option !!')


def clear_screen():
    """ func to clear screen"""
    # Clear the terminal screen
    return os.system('cls')


# call func display help
display_help()

# define a loop
while True:
    # question from user
    user_input: str = input('please enter one options in menu:').casefold()
    for command in ExitCommand:
        value: str = command.value
    if user_input == value:
        print('you exit from SHOPPING LIST !')
        print('HOPE TO SEE YOU SOON !')
        logger.info('user exited from shop !!!!')
        # exit from condition
        break
    # condition if user input equal to add
    elif user_input == 'add':
        # question from user
        question: str = input('which category do you want to add ?').casefold() # noqa E501 
        # call clearscreen fnc()
        clear_screen()
        # condition if question equal to 1
        if question == '1':
            with open('database/grocery-items.json', 'r+') as user_list:
                with open('database/shopping-list.json') as groceries:
                    grocery: dict = json.load(groceries)
                    # question from user#noqa:E501
                    items_number: int = int(input('how many items do you want add ?')) # noqa E501
                    # loop to iterate in items
                    for item in range(items_number):
                        # question from user
                        items: str = input('please enter your grocery items: ')
                        number_items: str = input('how many do you want from this item ?') # noqa E501
                        if items not in grocery:
                            print('no such item is in shopping list.')
                        else:
                            grocery_items[items] = number_items
                            products_number: int = len(grocery_items)
                            print(f'{products_number} item added successfully!!!')  # noqa E501
                            logger.info('user add item into grocery list')
                            json.dump(grocery_items, user_list)
        elif question == '2':
            with open('database/cosmetics-items.json', 'r+') as user_list:
                with open('database/shopping-list.json') as cosmetics:
                    cosmetic: dict = json.load(cosmetics)
                    # question from user
                    items_number: str = int(input('how many items do you want add ?'))  # noqa E501
                    # loop to iterate in items
                    for item in range(items_number):
                        # question from user
                        items: str = input('please enter your cosmetics items:') # noqa E501
                        number_items: str = input('how many do you want from this item ?')  # noqa E501
                        if items not in cosmetic:
                            print('no such item is in shopping list.')
                        else:
                            cosmetics_items[items] = number_items
                            products_number: int = len(cosmetics_items)
                            print(f'{products_number} item added successfully!!!')  # noqa E501
                            logger.info('user add item into grocery list')
                    json.dump(cosmetics_items, user_list)
        elif question == '3':
            with open('database/vegetable-items.json', 'r+') as user_list:
                with open('database/shopping-list.json') as vegetables:
                    vegetable: dict = json.load(vegetables)
                    # question from user
                    items_number: int = int(input('how many items do you want add ?'))  # noqa E501
                    # loop to iterate in items
                    for item in range(items_number):
                        # question from user
                        items = input('please enter your vegetable items: ')
                        number_items: str = input('how many do you want from this item ?')  # noqa E501
                        if items not in vegetable:
                            print('no such item is in shopping list.')
                        else:
                            vegetable_items[items] = number_items
                            products_number: int = len(vegetable_items)
                            print(f'{products_number}item added successfully!!!')  # noqaE501
                            logger.info('user add item into grocery list')
                    json.dump(vegetable_items, user_list)
        else:
            print('please enter valid number of category.')

    elif user_input == 'price':
        show_help()
        question: str = input('which category do you want to see items prices?') # noqa E501
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
        show_help()
        account_balance: int = int(input('please enter your account balance :')) # noqa E501
        clear_screen()
        question: str = input('which category do you want to buy ?')
        if question == '1':
            grocery: str = 'grocery'
            with open('database/grocery-items.json') as groceries:
                buy_categories(groceries, grocery_bill, grocery, account_balance)  # noqa E501
        elif question == '2':
            cosmetic: str = 'cosmetic'
            with open('database/cosmetics-items.json') as cosmetics:
                buy_categories(cosmetics, cosmetics_bill, cosmetic, account_balance)  # noqa E501
        elif question == '3':
            vegetable: str = 'vegetable'
            with open('database/vegetable-items.json') as vegetables:
                buy_categories(vegetables, vegetable_bill, vegetable, account_balance)  # noqa E501
        else:
            print('invalid category .')  
    elif user_input == 'show':
        show_help()
        question:str = input('which category do you want to see ?') # noqa E501
        clear_screen()
        if question == '2':
            with open('database/cosmetics-items.json', 'r') as files:
                show_category(files)
                logger.info('user watched items into grocery list')
        elif question == '3':
            with open('database/vegetable-items.json', 'r') as files:
                show_category(files)
                logger.info('user watched items into grocery list')
        elif question == '1':
            with open('database/grocery-items.json', 'r') as files:
                show_category(files)
                logger.info('user watched items into grocery list')
        else:
            print('invalid category.')

    elif user_input == 'remove':
        show_help()
        question = input('which category do you want to remove?')
        clear_screen()
        if question == '1':
            with open('database/grocery-items.json') as grocery:
                data = json.load(grocery)
                item = input('which item do you want to remove ?')
                if item in data:
                    data.pop(item)
                    with open('database/grocery-items.json', 'w') as files:
                        json.dump(data, files)
                        print(f'{item} removes from grocery list.')
                        logger.info(f'user removed {item} into grocery list')
                else:
                    print('no such item is in shopping list.')
        if question == '2':
            with open('database/cosmetics-items.json') as cosmetics:
                data = json.load(cosmetics)
                item = input('which item do you want to remove ?')
                if item in data:
                    data.pop(item)
                    with open('database/cosmetics-items.json', 'w') as files:
                        json.dump(data, files)
                        print(f'{item} removes from cosmetics list.')
                        logger.info(f'user removed {item} into grocery list')
                else:
                    print('no such item is in shopping list.')
        if question == '3':
            with open('database/vegetable-items.json') as vegetable:
                data = json.load(vegetable)
                item = input('which item do you want to remove ?')
                if item in data:
                    data.pop(item)
                    with open('database/vegetable-items.json', 'w') as files:
                        json.dump(data, files)
                        print(f'{item} removes from vegetable list.')
                        logger.info(f'user removed {item} into grocery list')
                else:
                    print('no such item is in shopping list.')
        else:
            print('invalid category.') # noqa E501      
    elif user_input == 'edit':
        show_help()
        edit_question = input('which category do you want to edit ? ')
        clear_screen()
        if edit_question == '1':
            with open('database/shopping-list.json') as files:
                data = json.load(files)
                with open('database/grocery-items.json') as groceries:
                    grocery = json.load(groceries)
                    edit_item = input('enter which item do you want edit it ?')
                    item_edit_with = input('enter which item do you want edit it with?')  # noqa E501
                    if edit_item in grocery:
                        if item_edit_with in data:
                            grocery[item_edit_with] = grocery.pop(edit_item)
                            with open('database/grocery-items.json', 'w') as files: # noqa E501
                                json.dump(grocery, files)
                                print(f'{edit_item} modified into {item_edit_with} in your grocery list.') # noqa E501
                                logger.info(f'{edit_item} modified into {item_edit_with} in your grocery list.') # noqa E501
                        else:
                            print('no such item is in shopping list.')
                    else:
                        print('no such item is in shopping list.')
        if edit_question == '2':
            with open('database/shopping-list.json') as files:
                data = json.load(files)
                with open('database/cosmetics-items.json') as cosmetics:
                    cosmetic = json.load(cosmetics)
                    edit_item = input('enter which item do you want edit it ?')
                    item_edit_with = input('enter which item do you want edit it with?') # noqa E501
                    if edit_item in cosmetic:
                        if item_edit_with in data:
                            cosmetic[item_edit_with] = cosmetic.pop(edit_item)
                            with open('database/cosmetics-items.json', 'w') as files: # noqa E501
                                json.dump(cosmetic, files)
                                print(f'{edit_item} modified into {item_edit_with} in your cosmetics list.')  # noqa E501
                                logger.info(f'{edit_item} modified into {item_edit_with} in your grocery list.')  # noqa E501
                        else:
                            print('no such item is in shopping list.')
                    else:
                        print('no such item is in shopping list.')
        if edit_question == '3':
            with open('database/shopping-list.json') as files:
                data = json.load(files)
                with open('database/vegetable-items.json') as vegetables:
                    vegetable = json.load(vegetables)
                    edit_item = input('enter which item do you want edit it ?')
                    item_edit_with = input('enter which item do you want edit it with?')  # noqa:E501
                    if edit_item in vegetable:
                        if item_edit_with in data:
                            vegetable[item_edit_with] = vegetable.pop(edit_item)  # noqa:E501
                            with open('database/vegetable-items.json', 'w') as files:  # noqa:E501
                                json.dump(vegetable, files)
                                print(f'{edit_item} modified into {item_edit_with} in your vegetable list.')  # noqa:E501
                                logger.info(f'{edit_item} modified into {item_edit_with} in your grocery list.')  # noqa:E501
                        else:
                            print('no such item is in shopping list.')
                    else:
                        print('no such item is in shopping list.')
        else:
            print('invalid category.')
    elif user_input == 'search':
        show_help()
        search_question = input('which category do you want to search ?')
        clear_screen()
        if search_question == '1':
            search_item = input('please enter your intended item :')
            with open('database/grocery-items.json')as files:
                data = json.load(files)
                if search_item in data:
                    print(f'item you searched is : {search_item}')
                    logger.info(f" user searched {search_item} in grocery list.")  # noqa:E501
                else:
                    print('item is not into the list')
        elif search_question == '2':
            search_item = input('please enter your intended item :')
            with open('database/cosmetics-items.json')as files:
                data = json.load(files)
                if search_item in data:
                    print(f'item you searched is : {search_item}')
                    logger.info(f" user searched {search_item} in grocery list.")  # noqa:E501
                else:
                    print('item is not into the list')
        elif search_question == '3':
            search_item = input('please enter your intended item :')
            with open('database/vegetable-items.json')as files:
                data = json.load(files)
                if search_item in data:
                    print(f'item you searched is : {search_item}')
                    logger.info(f" user searched {search_item} in grocery list.")  # noqa:E501
                else:
                    print('item is not into the list')
        else:
            print('invalid category.')
    else:
        print('invalid option.')
