import datetime

from peewee import * 
import readchar
import sys
import formats  
import task_functions
import re

db = SqliteDatabase('task_logger.db', pragmas={'foreign_keys': 1})


class Database:

    def __init__(self):
        try:
            db.connect(reuse_if_open="True")
        except:
            print("Not Working")
        else:
            db.create_tables([Employee, Task])
            self.main_menu()
            

    def main_menu(self):
        '''Display the main menu to the user'''

        while True:
            formats.clear_screen()

            menu_options = {'A' : self.add_entry,
                            'D' : self.delete_entry,
                            'E' : self.edit_entry,
                            'S' : self.search_entries}

            print('''What action would like to perform on the database:''')
            menu_string = ''.join(['[ {key} ] - {option}\n'.format(key=key, option=value.__doc__) for key, value in menu_options.items()])
            print(menu_string)

            user_input = readchar.readkey().upper()

            while user_input not in menu_options.keys():
                print("Please select only based on the options listed above...")
                user_input = readchar.readkey().upper()

            search_complete = menu_options[user_input]()
            if not search_complete:
                continue
            sys.exit()

    def delete_entry(self):
        '''Remove an employee from the database'''

        emp_data = self.get_employee_data()
        db_emp = Employee.get_or_none(Employee.ssn==emp_data['ssn'])

        if not db_emp:
            print("No employee in the system.")
            print("...you will be reverted back to the Main Menu.")
        else:
            print("Are you sure you want to delete this record?\n")
            while True:
                delete_record = readchar.readkey().upper()
                if delete_record not in ['Y', 'N']:
                    print('Invalid input...To delete a record press [Y]es or [N]o.')
                    continue
                break
            if delete_record == 'Y':
                db_emp.delete_instance()
                print("Deleted: {'first name'} {'last name'} - SSN# {'ssn'}".format(**emp_data))
            else:
                print("Database record not deleted.")

    def edit_entry(self):
        pass

        # record_fields = list(set([data[0] for data in db.get_columns('Employee') + db.get_columns('Task')]))  # model attributes
        
        # while True:
        #     edit_options = ''.join(f'{int(i) + 1} - {model_attr}\n'.replace('_', ' ').title() for i, model_attr in enumerate(record_fields))
        #     print('Edit a record by the following:\n\n' + edit_options)

        #     break
        # modify_field = {'edit employee' : get_employee_data}


    def verify_employee(self, person):
                                
        in_database = Employee.get_or_none(Employee.ssn == person['ssn'])

        if not in_database: # select all employees with the same first and last name if the employee's ssn not in database; line 81
            name_results = Employee.select().where(Employee.first_name == person['first name'],
                                                   Employee.last_name == person['last name'])

            if name_results: 
                print('There are {count} other employees with the name {name}:'.format(count=len(name_results), name=person['first name'] + ' ' + person['last name']))
                while True:
                    print('To review other employee matches: [Y]es / [N]o')
                    lookup = readchar.readkey().upper()
                    if lookup not in ['Y', 'N']:
                        print('Cannot process request...')
                        continue
                    break
                if lookup == 'N':
                    print('A new {first_n} {last_n} is added to the database...'.format(first_n=person['first name'], last_n=person['last name'])) 
                else:
                    official_name = '{first} {last}'.format(first=person['first name'], last=person['last name'])
                    ssn_number = '{ssn}'.format(ssn=person['ssn'])
                    print('Select an employee by employee id:\n')
                    print(f'Selected -->> Employee Name: {official_name} - SSN#: {ssn_number}')

                    ids = []
                    menu_results =  '*' * 20
                    for n in name_results:
                        ids.append(str(n.id))
                        menu_results += f'\nID#: {n.id}\nEmployee Name: {str(n)}\nSSN#: {n.ssn}\n' 
                    menu_results += '*' * 20 + '\nPress [N] to not modify the employee record and EXIT menu.'
                    print(menu_results)                 
                    
                    while True:
                        id_employee = readchar.readkey().upper()
                        key_selection = ids[:len(ids)]
                        if id_employee == 'N':
                            print("Exited out of employee records...no change occured.")
                            print(f"{person['first name']} {person['last name']} - SSN#: {person['ssn']} is added to the database.")
                            return Employee.create(first_name=person['first name'], 
                                                   last_name=person['last name'], 
                                                   ssn=person['ssn'])
                        elif id_employee not in ids:
                            print("Select only from these Employee ID#: + ''.join(f' [{n}] ' for n in ids[key_selection) to switch employees...")
                            continue
                        elif id_employee in ids:
                            print(f'Confirm you want to select: ID: #{id_employee} - {official_name}? [Y]es / [N]o')

                            while True:
                                verify_selection = readchar.readkey().upper()
                                if verify_selection not in ['Y', 'N']:
                                    print("Please choose only [Y]es or [N]o...")
                                    verify_selection = readchar.readkey().upper()
                                break

                            if verify_selection == 'Y':
                                print(f'{official_name} - ID#: {id_employee} has now been selected...')
                                return Employee.get_by_id(int(id_employee))

            return Employee.create(first_name=person['first name'], 
                                   last_name=person['last name'], 
                                   ssn=person['ssn'])           
        else:
            return in_database


    def get_employee_data(self):
        formats.clear_screen()

        print("Please provide the following information: First Name, Last Name, and SSN:")
                
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

        return dict(zip(['first name', 'last name', 'ssn'], [first_name, last_name, ssn_number]))


    def add_entry(self): 
        '''Add data to the database'''

        while True:
            query_person = self.get_employee_data()
            work_employee = self.verify_employee(query_person)
            
            task_data = {
                'task_type' : task_functions.store_category(),
                'task_date' : task_functions.store_date(),
                'task_time' : task_functions.store_duration(),
                'task_detail' : task_functions.store_note()
            }

            print("Task Stored...")
            Task.create(task=task_data['task_type'], task_date=task_data['task_date'], time=task_data['task_time'],
                        note=task_data['task_detail'], employee_id=work_employee)
            
            print('''
Please select from the following:
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
            all_emp_tasks = Task.select().where(Task.employee_id == real_id)

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
                                                                        Task.task_date <= search_end) # list of tasks within date range

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

            tasks_by_phrase = Task.select().where((Task.task.contains(phrase)) | (Task.note.contains(phrase)))

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
    task_date = DateField(formats='%Y-%m-%d')
    note = CharField(max_length=15)
    employee_id = ForeignKeyField(Employee, on_delete="CASCADE")


if __name__ == '__main__':
    Database()





