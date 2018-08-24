import pymysql
from datetime import datetime, date, timedelta
from random import choices
from tabulate import tabulate

username = 'root'
password = 'gnvH4DXxWf5GBQXgQEdu'
database_name = 'database_cibo'


class DatabaseException(Exception):
    """Exception for a database related error.
    
    value is the string that contains the error message.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


class NoMethodException(Exception):
    """Exception for when a method isn't defined.
    
    value is the string that contains the error message.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


class TableNameException(Exception):
    """Exception for a nonexistant table in the database.
    
    value is the string that contains the error message.
    """
    def __init__(self, table_name):
        self.value = 'Table name {} is not a valid table name.'.format(table_name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


def default_algorithm(date, priority):
    """Default algorithm for ItemChooser().
    Calculates the difference in days between the last day the item was chosen and today,
    then it adds one (so that no item has weight = 0),
    lastly it multiplies this number by the priority of that item.
    
    Arguments:
        date {datetime()} -- last time the item was chosen
        priority {int} -- multiplicative priority of the item
    """
    today = datetime.now()
    # calculates the difference in days between the last day the item was chosen and today,
    # adds 1 so that no item has weight = 0,
    # then multiplies it by the priority of that item
    return (abs(today - date).days+1) * priority


class ItemChooser():
    """
    ItemChooser inserts, updates and retrieves information from a given database.
    Its purpose is to choose a random item from the database, following a certain algorithm.

    user {string} -- username of the database
    passw {string} -- password of the database
    db_name {string} -- name of the database
    algorithm {function} -- function that organizes the priority list 
                            based on date and priority 
                            (default: {default_algorithm})
    """

    def __init__(self, user=username, passw=password, db_name=database_name, algorithm=default_algorithm):
        """Inizialises the class, opening the MySQL database and defining the valid tables.

        
        Keyword Arguments: 
            user {string} -- username of the database (default: {username})
            passw {string} -- password of the database (default: {password})
            db_name {string} -- name of the database (default: {database_name})
            algorithm {function} -- function that organizes the priority list 
                based on date and priority (default: {default_algorithm})
        """

        # db is a database with fields:
        #   - name {varchar(25)} -- name of the item
        #   - date {datetime} -- last time the item was eaten
        #   - priority {int} -- multiplicative chance that the item gets chosen
        #                       by self.choose_item()
        self.db = pymysql.connect('localhost', user, passw, db_name)
        self.db_name = database_name
        self.algorithm = algorithm

        cursor = self.db.cursor()
        try:
            cursor.execute('SHOW TABLES')
            self._TABLE_NAMES_LIST = [table_name for (table_name,) in cursor]
        except Exception as e:
            raise DatabaseException(str(e))
    
    def check_table_name_validity(self, table_name):
        """Checks if the name of a table is actually present in the database.
        
        Arguments:
            table_name {string} -- name of the table to check
        """
        if table_name not in self._TABLE_NAMES_LIST:
            raise TableNameException(table_name)
    
    def check_if_table_empty(self, table_name):
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()
            num_rows = cursor.execute('SELECT * FROM {}'.format(table_name))
            if num_rows == 0:
                raise DatabaseException(
                    '"{}" table is empty. Insert some items before trying to perform this action.'.format(table_name))
        
    def return_tabulate(self, lists, headers):
        """Returns a tabulate version of the list of all the information contained in the database.
        
        Arguments:
            lists {list of lists} -- list of lists with 3 elements: name, date, priority of a single item
            headers {list of strings} -- list of the headers for the table
        """
        return tabulate(lists, headers)


    def search_for_item(self, table_name, item_name):
        """Function that returns the database data about a item.
        
        Arguments:
            table_name {string} -- name of the table that contains the information
            item_name {string} -- name of the item to search
        """

        # try if the table exists <=> is contained in self._TABLE_NAMES_LIST
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()
            search_item = 'SELECT name, date, priority FROM {} WHERE name=%s'.format(table_name)
            try:
                cursor.execute(search_item, [item_name])
                if cursor.rowcount == 0:
                    raise DatabaseException(
                        'No item called "{}".'.format(item_name))
            except Exception as e:
                raise DatabaseException(str(e))

            # result contains all of the item's data: name, date and priority
            result = [(item_name, item_date, item_priority) for item_name, item_date, item_priority in cursor]
            cursor.close()
            return result
    
    def get_itemes(self, table_name):
        """Returns a dataframe containing all the itemes in the database
        
        Arguments:
            table_name {string} -- name of the db's table containing the information
        """
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()
            return_itemes = 'SELECT name, date, priority from {}'.format(table_name)
            try:
                cursor.execute(return_itemes)
            except Exception as e:
                raise DatabaseException(str(e))
            df = self.create_item_list(cursor)
            cursor.close()
            return df
    
    def create_item_list(self, cursor):
        """Creates a dataframe containing name, date and priority of all itemes
        starting from a database cursor from self.get_itemes()
        
        Arguments:
            cursor {Cursor} -- db cursor containing all data from a table
        """
        item_names = []
        item_dates = []
        item_priorities = []
        for name, date, priority in cursor:
            item_names.append(name)
            item_dates.append(date)
            item_priorities.append(priority)
        return (item_names, item_dates, item_priorities)

    def get_dataframe(self, table_name):
        """Takes the data from self.get_items(), creates a new dataframe containing:
            - name of the item
            - weight <=> chance that the item gets chosen by self.choose_item()
        
        Arguments:
            table_name {string} -- name of the db's table containing the information
        """
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            # table[0]: name of the item
            # table[1]: last day the item was eaten
            # table[2]: priority/weight of the item
            table = self.get_itemes(table_name)

            # calculates the difference in days between the last day the item was eaten and today,
            # adds 1 so that no item has weight = 0,
            # then multiplies it by the weight of that item
            df = (table[0], [self.algorithm(table[1][i], table[2][i])
                             for i in range(len(table[0]))])

        return df


    def add_new_table(self, table_name):
        """Adds a new table to the database.
        
        Arguments:
            table_name {string} -- name of the table that is going to be added to the database
        """
        cursor = self.db.cursor()
        add_table = (
            "CREATE TABLE `{0}`.`{1}` (`id{1}` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(45) NOT NULL,`date` DATETIME NOT NULL, `priority` INT NOT NULL, PRIMARY KEY(`id{1}`))"
        ).format(self.db_name, table_name)
        try:
            cursor.execute(add_table)
            self._TABLE_NAMES_LIST.append(table_name)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseException('Couldn\'t add the new table.' + str(e))
        cursor.close()

    def remove_table(self, table_name):
        """Removes a table from the database.
        
        Arguments:
            table_name {string} -- name of the table that is going to be removed from the database
        """
        cursor = self.db.cursor()
        add_table = (
            "DROP TABLE IF EXISTS `{0}`.`{1}`"
        ).format(self.db_name, table_name)
        try:
            cursor.execute(add_table)
            self._TABLE_NAMES_LIST.remove(table_name)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseException('Couldn\'t add the new table.' + str(e))
        cursor.close()


    def insert_new_item(self, table_name, item_name, item_date=datetime.now(),  item_priority=1):
        """Function that adds a new item to the database, with the date 
            defaulting to datetime.now() and including the item chance 
            multiplier.

        
        Arguments:
            table_name {string} -- name of the database table that contains the information
            item_name {string} -- name of the item to be added in the database
        
        Keyword Arguments:
            item_date {datetime} -- last time the item was eaten (default: {datetime.now()})
            item_priority {int} -- multiplicative chance that the item gets chosen 
                                    by the self.choose_item() function (default: {1})
        """
        # try if the table exists <=> is contained in self._TABLE_NAMES_LIST
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()
            
            insert_item = 'INSERT INTO {} (name, date, priority) VALUES (%s, %s, %s)'.format(table_name)
            data_item = (item_name.upper(), item_date, item_priority)

            try:
                cursor.execute(insert_item, data_item)
                self.db.commit()
            except:
                self.db.rollback()
                raise DatabaseException('Database insertion operation failed.')

            cursor.close()
    
    def remove_item(self, table_name, item_name):
        # try if the table exists <=> is contained in self._TABLE_NAMES_LIST
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()

            remove_item = 'DELETE FROM {} WHERE name = %s'.format(table_name)

            try:
                cursor.execute(remove_item, item_name)
                if cursor.rowcount == 0:
                    raise DatabaseException(
                        'No item called "{}".'.format(item_name))
                self.db.commit()
            except DatabaseException as e:
                self.db.rollback()
                raise e
            except:
                self.db.rollback()
                raise DatabaseException('Item couldn\'t be removed.')

            cursor.close()


    def random_choice(self, dataframe):
        """Chooses a random item in the dataframe.
        
        Arguments:
            dataframe {([string], [datatime], [int])} -- dataframe containing 3 lists, 
                                                each one containing all the itemes relative information
        """
        return choices(population=dataframe[0], weights=dataframe[1])[0]
    
    def choose_item(self, table_name, dataframe=None):
        """Gets the dataframe and chooses a random item. 
        The chance depends on the list of priorities returned by self.algorithm.
        
        Arguments:
            table_name {string} -- name of the df's table containing the information
        
        Keyword Arguments:
            dataframe {([string], [int])} -- names and weights of the itemes (default: {None})
        """
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            # if no dataframe has been passed to the function
            if dataframe is None:
                # gets one from self.get_dataframe()
                dataframe = self.get_dataframe(table_name)
            choice = self.random_choice(dataframe)
            return choice

    def update_item_date(self, table_name, item_name, new_date=datetime.now()):
        """Updates the date of a item to a new date.
        
        Arguments:
            table_name {string} -- name of the db's table containing the data
            item_name {string} -- name of the item to update
            new_date {datatime} -- date to update the item to (default: {datetime.now()})
        """
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()
            update_item = 'UPDATE {} SET date=%s WHERE name=%s'.format(table_name)
            try:
                cursor.execute(update_item, (new_date, item_name))
                if cursor.rowcount == 0:
                    raise DatabaseException('No item called "{}".'.format(item_name))
                self.db.commit()
            except DatabaseException as e:
                self.db.rollback()
                raise DatabaseException(str(e))
            except:
                self.db.rollback()
                raise DatabaseException('Cannot update {} date'.format(item_name))
            cursor.close()

    def update_priority(self, table_name, item_name, new_priority):
        """Updates a item to a new priority level.
        
        Arguments:
            table_name {string} -- db's table containing the information
            item_name {string} -- name of the item to update
            new_priority {int} -- new priority
        """
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            cursor = self.db.cursor()
            update_prio = 'UPDATE {} SET priority=%s WHERE name=%s'.format(
                table_name)
            try:
                cursor.execute(update_prio, (new_priority, item_name))
                if cursor.rowcount == 0:
                    raise DatabaseException(
                        'No item called "{}".'.format(item_name))
                self.db.commit()
            except DatabaseException as e:
                self.db.rollback()
                raise DatabaseException(str(e))
            except:
                self.db.rollback()
                raise DatabaseException(
                    'Cannot update "{}"\'s priority to {}.'.format(item_name, new_priority))
            cursor.close()


    def print_table(self, table_name, sorted_by_date=False, sorted_by_priority=False, tabulate=False):
        """
        For TERMINAL:
        Returns a string containing all of the information contained in a table of the database.
        For GUI:
        Returns a list of all the information contained in a table of the database.

        Arguments:
            table_name {string} -- name of the db's table
        
        Keyword Arguments:
            sorted_by_date {bool} -- asks if the data has to be sorted by date (default: {False})
            sorted_by_priority {bool} -- asks if the data has to be sorted by priority (default: {False})
            tabulate {bool} -- asks if the data has to be put in tabular form with tabulate
                for better viewing when using the terminal (default: {False})
        """
        try:
            self.check_table_name_validity(table_name)
        except TableNameException as e:
            raise e
        else:
            # table = ([names], dates[], priorities[])
            table = self.get_itemes(table_name)
            
            # transforming the tuple of lists into lists of lists
            # each list has 3 elements: the attributes of a single item
            lists = [[table[0][i], table[1][i], table[2][i]] for i in range(len(table[0]))]
            if sorted_by_date:
                lists.sort(key=lambda table: table[1])
            elif sorted_by_priority:
                lists.sort(key=lambda table: table[2])

            # returns a fancy table-ish formatted string if tabulate == True
            if tabulate:
                return '> ' + table_name.upper() + '\n' + self.return_tabulate(lists, ['ITEMS', 'DATE', 'PRIORITY'])
            else:
                return lists
    
    def print_database(self, sorted_by_date=False, sorted_by_priority=False, tabulate=False):
        """Returns self.print_table() for all tables in the database <=> all the tables in self._TABLE_NAMES_LIST
        
        Keyword Arguments:
            sorted_by_date {bool} -- asks if the data has to be sorted by date (default: {False})
            sorted_by_priority {bool} -- asks if the data has to be sorted by priority (default: {False})
        """
        tables = [self.print_table(table_name, sorted_by_date=sorted_by_date, 
                                   sorted_by_priority=sorted_by_priority,
                                   tabulate=tabulate) for table_name in self._TABLE_NAMES_LIST]
        return tables
    
