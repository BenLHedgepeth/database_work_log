import datetime
import re
import readchar
import collections
import os
import main
import pdb;


def date(emp_date):
    while True:
        try:
            format_check = datetime.datetime.strptime(emp_date, '%Y-%m-%d').date()
        except ValueError:
            emp_date = input("Dates of the following format are only accepted: [yyyy-mm-dd]\n>>>")
        else:
            return format_check

    print(format_check)

def timeclock(time_worked):

    time_pattern = re.compile(r'\d{2}:\d{2}')

    while True:
        time_format = time_pattern.fullmatch(time_worked)

        while not time_format:
            time_worked = input("Cannot register the time entered. Please enter your time by the [HH:MM] format:\n>>>")
            time_format = time_pattern.fullmatch(time_worked)
        

        hours, minutes = time_worked.split(':')

        try:
            time_clocked = datetime.timedelta(minutes=int(minutes), hours=int(hours))
        except ValueError as e:
            print(e)
        else:
            return time_clocked


def filter_name(person_name):
    '''Removes excessive/unnecessary characters from a provided name'''

    name_length = person_name.split()

    if person_name.upper().endswith(('JR', 'SR', 'JR.', "SR.")): 
        del name_length[-1]
    if len(name_length) > 2:
        del name_length[1:-1]
    return ' '.join(name_length)

def verify_ssn(ssn_number):
    ssn_pattern = re.compile(r'\d{3}-\d{2}-\d{4}')
                
    while True:
        if not re.match(ssn_pattern, ssn_number):
            ssn_number = input("The SSN provided doesn't match the format required '111-11-1111'")
            continue
        break
    return ssn_number 



def display_tasks(task_objects):

    indexed_tasks = collections.deque(zip(task_objects, range(1, len(task_objects) + 1))) #provides a count of each task in `task_objects`
    
    while True:
        i = indexed_tasks[0][1] # Task #__ of len(task_objects)
        show_task = indexed_tasks[0][0]
        by_employee = str(main.Employee.get(main.Employee.id == show_task.employee.id)).upper() # Employee of task

        print(f'***Task #{i} of {len(task_objects)}****')
        print(f'''
Employee: {by_employee}
Task: {show_task.task}
Task Date: {show_task.task_date}
Details : {show_task.note}\n''')
        print('*' * 20)

        print('[C] - Next Task Entry\n[P] - Previous Task Entry\n[B] - Back To Previous Menu')

        while True:
            print("Please select one of the above options...")
            user_choice = readchar.readkey().upper()
            if user_choice not in ['C', 'P', 'B']:
                print("Invalid selection...")
                continue
            break
        if user_choice == 'C':
            indexed_tasks.rotate(-1)
            continue
        elif user_choice == 'P':
            indexed_tasks.rotate(1)
            continue
        break # exit loop if user input is `B`


def clear_screen():
    return os.system('cls' if os.name=='nt' else 'clear')

        
if __name__ == '__main__':
    print(filter_name ('George Herber Walker Bush JR.'))