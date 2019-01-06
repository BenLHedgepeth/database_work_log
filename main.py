import datetime
import re
import readchar
import sys

import formats  
import task_functions

from collections import OrderedDict


db = SqliteDatabase('task_logger.db', pragmas={'foreign_keys': 1})

class Database:

    def __init__(self):
        try:
            db.connect(reuse_if_open="True")
        except:
            print("Not Working")
            sys.exit()
        db.create_tables([Employee, Task])
        self.main_menu()
            

    def main_menu(self):
        '''Display the main menu to the user'''

        menu_options = {
            'A' : self.add_entry,
            'D' : self.delete_entry,
            'S' : self.search_entries,
            'E' : self.edit_entry
        }

        menu_ids = menu_options.keys()

        show_menu = ''.join(['[ {key} ] - {option}\n'.format(key=key, option=value.__doc__) # string of `menu_options`
                     for key, value in menu_options.items()])

        while True:
            formats.clear_screen()
            print(show_menu + "\nSelect from one of the above options")
            option = readchar.readkey().upper()

            while option not in menu_ids:
                print(f'Cannot perform selection -> ID entered: [{option}]')
                user_input = readchar.readkey().upper()

            search_again = menu_options[option]()
            if not search_again:
                continue
            sys.exit()

    def delete_entry(self):
        '''Remove an employee from the database'''
        while True:

            emp_data = self.get_employee_data()
            db_emp = Employee.get_or_none(Employee.ssn==emp_data['ssn'])

            if not db_emp:
                print("That employee is not in the system.")
            else:
                while True:
                    print("\nTo delete this record, enter [Y]es/[N]o...\n")
                    delete_record = readchar.readkey().upper()
                    if delete_record not in ['Y', 'N']:
                        print('Invalid input.')
                        continue
                    break
                if delete_record == 'Y':
                    db_emp.delete_instance()
                    print("Deleted: {first_name} {last_name} - SSN# {ssn}".format(**emp_data))
                else:
                    print("Database record not deleted.")
                
                # while True:
                #     print("To delete a different employee...press [Y]es/[N]o")
                #     delete_attempt = readchar.readkey().upper()
                #     if delete_attempt not in ['Y', 'N']:
                #         print("Cannot interpret desired action.")
                #         continue
                #     break

                # if delete_attempt == 'Y':
                #     continue
                # break


    def edit_entry(self):

        get_emp = get_employee_data()
        edit_employee = Employee.get_or_none(Employee.ssn == get_emp['ssn'])

        if not edit_employee:
            print("No entries by that employee exist.")
        else:
            edit_db_task = Employee.select().join(Task).get
        all_fields = db.get_columns('Employee') + db.get_columns('Task')


        record_fields = OrderedDict.fromkeys([data[0] 
                            for data in all_fields if 'id' not in data[0]]) # model attributes
       
        edit_options = ''.join(f'- {model_attr}\n'.replace('_', ' ').title() 
                            for model_attr in enumerate(record_fields))
   

        edit_task_item = {'task' : self.store_category,
                        'task_date' : self.store_date,
                        'time_duration' : self.store_time,
                        'note' : self.store_note}
        
        while True:
            edit_choice = input("Which field would you like to change?\n>>> ").upper().strip()
            if edit_choice not in record_fields:
                print("Cannot edit field...")
                continue
            break

        if edit_choice in ['first_name', 'last_name', 'SSN']:
            updated_attr = self.get_employee_data()
        else:
            updated_attr = edit_task_item[edit_choice]()



            print('Edit a record by the following:\n\n' + edit_options)

        modify_field = {'edit employee' : get_employee_data}


    def verify_employee(self, person):
                                
        in_database = Employee.get_or_none(Employee.ssn == person['ssn'])

        if in_database:
            return in_database # if record exists with that ssn
        name_results = Employee.select().where(Employee.first_name == person['first_name'], # if record doesn't exist with that ssn
                                                   Employee.last_name == person['last_name'])
        if name_results:
            official_name = '{first_name} {last_name}'.format(**person)
            print(f'There are {len(name_results)} employees with the name: {official_name}')
            while True:
                print('To review other matches: [Y]es / [N]o')
                lookup = readchar.readkey().upper()
                if lookup not in ['Y', 'N']:
                    print('Cannot process request...')
                    continue
                break
            if lookup == 'N':
                print('A new {official_name} is added to the database...')
                return Employee.create(**person)
            print('Selected -->> Employee Name: {first_name} {last_name} - SSN#: {ssn}'.format(**person))
            ids = []
            menu_results =  '*' * 20
            for n in name_results:
                ids.append(str(n.id))
                menu_results += f'\nID#: {n.id}\nEmployee Name: {str(n)}\nSSN#: {n.ssn}\n' 
            menu_results += '*' * 20 + '\nPress [N] to not modify the employee record and EXIT menu.'
            print(menu_results)                            
             
            while True:
                id_employee = readchar.readkey().upper()
                if id_employee == 'N':
                    print("Exited out of employee records...no change occured.")
                    print("{first_name} {last_name} - SSN#: {ssn} is added to the database.".format(**person))
                    return Employee.create(**person)
                elif id_employee not in ids:
                    print("Select only from these Employee ID#: + ''.join(f' [{n}] ' for n in ids[key_selection) to switch employees...")
                    continue
                elif id_employee in ids:
                    print(f'{official_name} - ID#: {id_employee} has now been selected...')
                    return Employee.get_by_id(int(id_employee))                       
            return in_database


    def get_employee_data(self):
        formats.clear_screen()

        print("Please provide the following information: first_name, last_name, and SSN:")
                
        employee_query = input("\nEnter the employee's name:\n>>> ").title().strip()
        emp_full_name = formats.name(employee_query)
        first_name, last_name = emp_full_name.split()
       

        ssn_pattern = re.compile(r'\d{3}-\d{2}-\d{4}')
            
        while True:
            ssn_number = input('\nEnter {staff_employee}\'s social security number:\n>>> '.format(staff_employee=f'{first_name} {last_name}')).strip()

            if not re.match(ssn_pattern, ssn_number):
                print("The social security number doesn't match the character format required '111-11-1111'")
                continue
            break

        return dict(zip(['first_name', 'last_name', 'ssn'], [first_name, last_name, ssn_number]))


    def add_entry(self): 
        '''Add data to the database'''

        while True:
            query_person = self.get_employee_data()
            work_employee = self.verify_employee(query_person)
            
            task_data = {
                'task' : task_functions.store_category(),
                'task_date' : task_functions.store_date(),
                'time_duration' : task_functions.store_duration(),
                'note' : task_functions.store_note(),
                'employee' : work_employee
            }

            print("Task Stored...")
            Task.create(**task_data)
            
            print('''Please select from the following:
[ N ] - Add another entry
[ B ] - Back to the previous menu
'''
)
            while True:
                prompt_new_entry = readchar.readkey().upper() # invokes program flow via keystroke

                if prompt_new_entry not in ['N', 'B']:
                    print("Invalid option. Please enter [N]ew entry; [B]ack to the previous menu:")
                    continue
                break
            if prompt_new_entry == 'N':
                continue
            break


    def search_entries(self):
        '''Search database'''
        while True:
            search_options = {'1' : self.search_employee,
                              '2' : self.search_dates,
                              '3' : self.search_minutes,
                              '4' : self.search_notes}

            
            print("Specify how you want to search the database")
            search_menu_str = ''.join(f'{key} - {value.__doc__}\n' for key, value in search_options.items())    
            print(search_menu_str)  

            while True:
                search_input = readchar.readkey() 
                if search_input not in search_options:
                    print("That functionality does not exist. Please select only from the options listed above.")
                    search_input= readchar.readchar()
                break

            search_options[search_input]()
            print("\nWould you like to perform another search...\n[N]ew search\n[P]revious Menu")

            while True:
                control_flow = readchar.readkey().upper()
                if control_flow not in ['N', 'P']:
                    print('Command unknown...please press [N] or [P]')
                    continue
                break
            if control_flow == 'N':
                continue
            return False

    def search_employee(self):
        """Find database entries by employee"""
        while True:

            task_dict = {}

            stored_employees = Employee.select()
            employee_menu = ''

            for emp in stored_employees:
                employee_menu_id = f'{emp.id}-{emp.ssn[-4:]}'
                employee_menu += employee_menu_id + f') {str(emp)}\n'

                task_dict.setdefault(employee_menu_id, [])
                task_dict[employee_menu_id].append(emp)
            print(employee_menu)

            while True:
                select_emp = input('Please enter an employee\'s id followed by the last four of their SSN# [X-XXXX]:\n>>> ').strip()
                if select_emp not in task_dict:
                    print("An invalid reference was entered...")
                    continue
                break

            real_id = int(select_emp[:1])   
            all_emp_tasks = Task.select().where(Task.employee == real_id)

            repeat_search_employee = formats.display_tasks(all_emp_tasks)

            if not repeat_search_employee:
                break
            else:
                continue


    def search_dates(self):
        """Find database entries by date"""
        while True:
            provided_date = formats.date(input("Provide a base date to begin searching entries\n>>>"))

            while True:
                try:
                    day_range = int(input(f"Establish how many days to look before and after {provided_date}:\n>>>"))
                except TypeError:
                    print("Could not compute the day range search...to gather dates within a range only provide numerical values...")
                    continue
                else:
                    if not day_range:
                        print('A minimum of 1 day must be provided to initiate a date search...')
                        continue
                    break
            try:
                search_start = provided_date - datetime.timedelta(days=day_range)
            except OverflowError:
                this_year = provided_date.year
                search_start = datetime.date(year=this_year, month=1, days=1)
            else:
                try:
                    search_end = provided_date + datetime.timedelta(days=day_range)
                except OverflowError:
                    this_year = provided_date.year
                    search_end = datetime.date(year=this_year, month=12, day=31)

                collect_date_range = Task.select().join(Employee).where(Task.task_date >= search_start, 
                                                                        Task.task_date <= search_end).order_by(search_start) # list of tasks within date range

                if not collect_date_range:
                    print("There are no dates within the given range.\nWould you like to search under a larger range [Y]es / [N]o?").upper().strip()
                    while True:
                        date_query_option = readchar.readkey().upper()
                        if date_query_option not in ['Y', 'N']:
                            print("Invalid option...Please press [Y]es or [N]o")
                            continue
                        break
                    if date_query_option == 'Y':
                        continue
                    else:
                        break
                else:
                    repeat_date_search = formats.display_tasks(collect_date_range)
                    if not repeat_date_search:
                        break
                    else:
                        continue

    def search_minutes(self):
            """Find database entries by time spent"""
            pass

    def search_notes(self):
        """Find database entries by string matches"""
        while True:
            formats.clear_screen()

            while True:
                phrase = input("Search tasks by a given phrase:\n>>>").title().strip()
                if not phrase:
                    print("Empty strings cannot be used to search tasks...")
                    continue
                break

            tasks_by_phrase = Task.select().where((Task.task.contains(phrase)) | (Task.note.contains(phrase))).order_by(Task.task_date)

            repeat_search_notes = formats.display_tasks(tasks_by_phrase)

            if not repeat_search_notes:
                break
            continue



class BaseModel(Model):
    class Meta:
        database = db


class Employee(BaseModel):
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=15)
    ssn = CharField(max_length=12, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
        

class Task(BaseModel):
    task = CharField(max_length=15)
    task_date = DateField(formats=['%Y-%m-%d'])
    time_duration = TimeField(formats=['%H:%M'])
    note = CharField(max_length=15)
    employee = ForeignKeyField(model=Employee, on_delete="CASCADE")


if __name__ == '__main__':
    Database()





