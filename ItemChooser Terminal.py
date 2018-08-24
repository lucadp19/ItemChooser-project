import sys
from tabulate import tabulate
import ICAnalyzer
import ItemChooser

login_file = 'login_data.txt'

choices_text = {
    0: ('Insert new table', 'insert_new_table'),
    1: ('Remove a table', 'remove_table'),
    2: ('Insert new item', 'insert_new_item'),
    3: ('Remove an item', 'remove_item'),
    4: ('Choose an item', 'choose_item'),
    5: ('Update a item (date)', 'update_item_date'),
    6: ('Update an item (priority)', 'update_priority'),
    7: ('Print all the items', 'print_tables'),
    8: ('Run data-analysis tool', 'data_analysis'),
    'E': ('Exit', 'exit_app'),
}

user = ItemChooser.username
passw = ItemChooser.password
db_name = ItemChooser.database_name
algorithm = ItemChooser.default_algorithm

def main():
    with open(login_file, 'r+') as f:
        data = f.read()
        if not data:
            print('> Input the login data for your database: ')
            user = input('> username:\n\t')
            passw = input('> password:\n\t')
            db_name = input('> database name:\n\t')
            f.write('{}\n{}\n{}'.format(user, passw, db_name))
        else:
            user, passw, db_name = data.split('\n')     

    try:
        ic_db = ItemChooser.ItemChooser(user=user, passw=passw, db_name=db_name, algorithm=algorithm)
    except Exception as e:
        print(str(e))
        sys.exit()

    while True:
        print(print_options() + '\n')
        choice = input('> Insert your choice: ')

        # Add new table
        if choice == '0':
            table_name = input('> Insert the name of the database table to add to the database:\n\t')
            try:
                ic_db.add_new_table(table_name)
            except ItemChooser.DatabaseException as e:
                print(str(e))

        # Remove a table
        elif choice == '1':
            table_name = input(
                '> Insert the name of the table to remove from the database:\n\t')
            try:
                ic_db.remove_table(table_name)
            except ItemChooser.DatabaseException as e:
                print(str(e))

        # Insert new item
        elif choice == '2':
            table_name = input('> Insert the name of the database table:\n\t')
            item_name = input('> Insert the name of the item:\n\t')
            item_priority = float(input('Insert the priority for the item, or else write 1:\n\t'))
            try:
                # Insert item into the database
                ic_db.insert_new_item(table_name=table_name,
                                    item_name=item_name,
                                    item_priority=item_priority
                                    )
            except ItemChooser.TableNameException as e:
                print('ERROR!: ' + e.value)

        # Remove an item
        elif choice == '3':
            table_name = input('> Insert the name of the database table:\n\t')
            item_name = input('> Insert the name of the item:\n\t')

            try:
                item = ic_db.search_for_item(table_name, item_name)[0]
                print('\n' + tabulate([list(item)], ['ITEM','DATE','PRIORITY']))
            except ItemChooser.DatabaseException as e:
                print(e)
                continue
            
            yn = input('> Are you sure you want to delete this item? Y/N for yes/no:\n\t')
            if yn in ('y', 'Y', 'yes'):
                try:
                    ic_db.remove_item(table_name, item_name)
                    print('> Item removed!')
                except Exception as e:
                    print('ERROR!: ' + str(e))
            elif yn in ('n', 'N', 'no'):
                continue

        # Choose a random item
        elif choice == '4':
            table_name = input('> Insert the name of the database table:\n\t')
            try:
                df = ic_db.get_dataframe(table_name)
                # infinite while so that the user can keep refusing until they either accept or exit
                # this way the dataframe has to be loaded only once
                while True:
                    item_choice = ic_db.choose_item(table_name=table_name, dataframe=df)
                    result = input(
                        '> Do you want to accept this choice: "{}"? Write Y/N/E for yes/no/exit\n\t'.format(item_choice.lower()))
                    if result in ('y', 'Y', 'yes'):
                        # if result is yes, print accepted choice, 
                        # update the item's date and break the procedure
                        print('> You have accepted "{}"'.format(item_choice))
                        ic_db.update_item_date(table_name, item_choice)
                        break
                    elif result in ('e', 'E', 'exit'):
                        # if result is exit, break the procedure
                        break
                    else:
                        # if result is no, continue
                        pass
            except ItemChooser.TableNameException as e:
                print('ERROR!: ' + e.value)

        # Update the date of an item
        elif choice == '5':
            table_name = input('> Insert the name of the database table:\n\t')
            item_name = input('> Insert the name of the item:\n\t')
            try:
                ic_db.update_item_date(table_name=table_name, item_name=item_name)
            except ItemChooser.TableNameException as e:
                print('ERROR!: ' + e.value)

        # Update the priority of an item
        elif choice == '6':
            table_name = input('> Insert the name of the database table:\n\t')
            item_name = input('> Insert the name of the item:\n\t')
            item_priority = float(input('Insert the new priority for the item:\n\t'))
            try:
                ic_db.update_priority(table_name=table_name, item_name=item_name, new_priority=item_priority)
            except ItemChooser.TableNameException as e:
                print('ERROR!: ' + e.value)
            except ItemChooser.DatabaseException as e:
                print('ERROR!: ' + str(e))

        # Print all the tables
        elif choice == '7':
            yn = input('> Do you want the output to be sorted by date? Y/N:\n\t')
            if yn in ('y', 'Y', 'yes'):
                print('\n')
                for table in ic_db.print_database(sorted_by_date=True, tabulate=True):
                    print(table + '\n')
            else:
                yn = input('> Do you want the output to be sorted by priority? Y/N:\n\t')
                if yn in ('y', 'Y', 'yes'):
                    print('\n')
                    for table in ic_db.print_database(sorted_by_priority=True, tabulate=True):
                        print(table + '\n')
                else:
                    print('\n')
                    for table in ic_db.print_database(tabulate=True):
                        print(table + '\n')

        # Data Analysis
        elif choice == '8':
            analyzer = ICAnalyzer.ItemChooserAnalyzer(ic_db)
            rep_limit = int(input('> What is the repetition limit?\n\t'))
            table_name = input('> What is the table name?\n\t')
            print(analyzer.run(table_name, rep_limit=rep_limit, tabulate=False))
        

        # Exit
        elif choice in ('e', 'E', 'exit'):
            break

        else:
            print('Choice not allowed')
        print()


def print_options():
    return tabulate(
        [[key, value[0]] for key, value in choices_text.items()],
        ['N', 'Choices']
    )

if __name__ == "__main__":
    main()
