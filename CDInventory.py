#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# aaleshin, 2022-Aug-13, Modified File to move code into functions under classes
# aaleshin, 2022-Aug-14, Modified File to include docstrings
# aaleshin, 2022-Aug-21, Modified File to use Binary Files and Structured Error Handling
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    # TODone add functions for processing here
    """Manipulating the data in memory"""
    
    @staticmethod
    def delete_CD(table):
        """Deletes CD from in memory table
        
        Args:
            table (list of dict): In memory 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

    @staticmethod
    def add_CD(table, ID, Title, Artist):
        """Adds CD information to in memory table
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            ID (String): String containing CD ID.
            Title (String): String containing CD Title.
            Artist (String): String containing CD Artist.
        
        Returns:
            None.
        """
        intID = int(ID)
        dicRow = {'ID': intID, 'Title': Title, 'Artist': Artist}
        table.append(dicRow)
        IO.show_inventory(table)

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from binary file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of binary file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'rb')
        lst = []
        while True:
            try:
                lst.append(pickle.load(objFile))
            except (EOFError):
                break
        #data = pickle.load(objFile)
        for line in lst:
            line = line.strip().split(',')
            dicRow = {'ID': int(line[0]), 'Title': line[1], 'Artist': line[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        # TODone Add code here
        """Function to manage writing data from table to file
        
        Writes data from 2D table (list of dicts) to binary file one row at a time.
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
            Returns:
                None.
        """            
        objFile = open(file_name, 'wb')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            pickle.dump(','.join(lstValues) + '\n', objFile)
        objFile.close()

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TODone add I/O functions as needed
    
    
    @staticmethod
    def get_CD():
        """Gets user input for CD ID, Title and Artist.
        
        Args:
            None.
            
        Returns:
            Returns the CD ID as a string.
            Returns the CD Title as a string.
            Returns the CD Artist as as string.
        """
        ID = input('Enter ID: ').strip()
        Title = input('What is the CD\'s title? ').strip()
        Artist = input('What is the Artist\'s name? ').strip()

        return ID, Title, Artist

# 1. When program starts, read in the currently saved Inventory
try:
    FileProcessor.read_file(strFileName, lstTbl)
except FileNotFoundError as e:
    print('Binary file does not exist!')
    print('Build in error info:')
    print(type(e), e, e.__doc__, sep = '\n')
except EOFError as e:
    print('The file is empty!')
    print('Build in error info:')
    print(type(e), e, e.__doc__, sep = '\n')
    

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            try:
                FileProcessor.read_file(strFileName, lstTbl)
                IO.show_inventory(lstTbl)
            except FileNotFoundError as e:
                print('Binary file does not exist!')
                print('Build in error info:')
                print(type(e), e, e.__doc__, sep = '\n')
            except EOFError as e:
                print('The file is empty!')
                print('Build in error info:')
                print(type(e), e, e.__doc__, sep = '\n')
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.get_CD()
        # 3.3.2 Add item to the table
        # ToDone move processing code into function
        try:
            DataProcessor.add_CD(lstTbl, strID, strTitle, strArtist)
        except ValueError as e:
            print('ID is not an integer!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep = '\n')        
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            # TODone move processing code into function
            DataProcessor.delete_CD(lstTbl)
            IO.show_inventory(lstTbl)
        except ValueError as e:
            print('ID is not an integer!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep = '\n')   
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODone move processing code into function
            try:
                FileProcessor.write_file(strFileName, lstTbl)
            except Exception as e:
                print('There was a general error!')
                print('Build in error info:')
                print(type(e), e, e.__doc__, sep = '\n')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')