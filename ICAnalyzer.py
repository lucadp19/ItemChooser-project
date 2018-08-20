import ItemChooser
from tabulate import tabulate
from collections import defaultdict


class ItemChooserAnalyzer():
    """Performs data-analysis on an instance of ItemChooser().
    In particular, given a table and a repetition counter, it calls the 
    choose_item() function rep_limit times, then returns a table containing
    the general data of every item and how many times it got chosen.
    It may be useful to check if your custom algorithm for choose_item() is
    working properly or not.
    
    ic_db is an instance of ItemChooser(). It represents the database on which
    the actions will be performed.
    """
    def __init__(self, ic_db):
        """Inizialises the ItemChooser database.
        
        Arguments:
            ic_db {ItemChooser()} -- database that will be analysed
        """
        self.ic_db = ic_db
    
    def return_tabulate(self, lists, headers):
        """Returns a tabulate version of the list of all the information contained in the database.
        
        Arguments:
            lists {list of lists} -- list of lists with 3 elements: name, date, priority of a single item
            headers {list of strings} -- list of the headers for the table
        """
        return tabulate(lists, headers)

    def run(self, table_name, rep_limit=1000, tabulate=False):
        """Calls the choose_item() function rep_limit times on the database.
        
        Arguments:
            table_name {str} -- name of the database table that will be analysed
        
        Keyword Arguments:
            rep_limit {int} -- number of times the choose_item() function will
                                be called (default: {1000})
            tabulate {bool} -- if true, the function returns a nice table-ish 
                                formatted string (default: {False})
        """ 
        data_analysis_dict = defaultdict(int)

        # check that the table isn't empty
        try:
            self.ic_db.check_if_table_empty(table_name)
        except ItemChooser.DatabaseException as e:
            raise e

        try:
            # gets the dataframe
            df = self.ic_db.get_dataframe(table_name)
        except ItemChooser.TableNameException as e:
            raise e

        # call choose_item() rep_limit times
        for _ in range(rep_limit):
            choice = self.ic_db.choose_item(table_name, df)
            data_analysis_dict[choice] += 1
        
        return self.print_list(table_name, data_analysis_dict, tabulate=tabulate)
    
    def print_list(self, table_name, data_analysis_dict, tabulate=False):
        """Transforms the resulting list from a self.run() call into a table
        (in list or string form) that can be printed or displayed in other
        ways.
        
        Arguments:
            table_name {string} -- name of the table of the database
            data_analysis_dict {list of lists} -- contains the results of self.run()
                in particular data_analyisis_dict is made by:
                    key {string} -- represents the name of the chosen item
                    value {int} -- represents how many time the key got chosen
        
        Keyword Arguments:
            tabulate {bool} -- if true, the function returns a nice table-ish 
                                formatted string (default: {False})
        """
        lists = []
        all_items = self.ic_db.get_itemes(table_name) # all items in the table

        # for every item add them to the list, with the relative information
        for i in range(len(all_items[0])):
            name, date, priority = all_items[0][i], all_items[1][i], all_items[2][i]
            lists.append([name, data_analysis_dict[name], date.date(), priority])
        
        if not tabulate:
            return sorted(lists, key=lambda col: col[1])
        else:
            tabulated_list = self.return_tabulate(
                sorted(lists, key=lambda col: col[1]),
                ['NAME', 'REPETITIONS', 'DATE', 'PRIORITY']
            )
            return tabulated_list
    

def main():
    # get login data
    with open("login_data.txt", 'r+') as f:
        data = f.read()
        if not data:
            print('> Input the login data for your database: ')
            user = input('> username:\n\t')
            passw = input('> password:\n\t')
            db_name = input('> database name:\n\t')
            f.write('{}\n{}\n{}'.format(user, passw, db_name))
        else:
            user, passw, db_name = data.split('\n')

    # defines itemchooser database
    ic_db = ItemChooser.ItemChooser(
        user=user, passw=passw, db_name=db_name, 
        algorithm=ItemChooser.default_algorithm
    )
    analyzer = ItemChooserAnalyzer(ic_db)

    while True:
        rep_limit = int(input('> What is the repetition limit?\n\t'))
        table_name = input('> What is the table name?\n\t')

        try:
            result = analyzer.run(table_name, rep_limit=rep_limit, tabulate=True)
            print(result)
        # if table is empty
        except ItemChooser.DatabaseException as e:
            print('> ERROR: ' + str(e) + '\n\t')
        # if table doesn't exist
        except ItemChooser.TableNameException as e:
            print('> ERROR: ' + str(e) + '\n\t')

        while True:
            cond = input('> Do you want to try again? Y/N\n\t')
            if cond in ('y', 'Y', 'yes'):
                break
            elif cond in ('n', 'N', 'no'):
                return None
            else:
                print('> Choice not allowed.')


if __name__ == '__main__':
    main()
