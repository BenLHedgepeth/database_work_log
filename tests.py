import unittest  # built-ins, python standard library
import datetime

from peewee import *  # third-party

from main import Employee, Task # custom script, package, module

test_db = SqliteDatabase('dummy.db')

class TestDatabase(unittest.TestCase):
    DB_MODELS = [Employee, Task]

    @classmethod
    def setUpClass(cls):
        print("Setup")
        test_db.connect(reuse_if_open=True)
        test_db.bind(cls.DB_MODELS)
        test_db.drop_tables(cls.DB_MODELS)
        test_db.create_tables(cls.DB_MODELS)

    def setUp(self):

        self.id1_data = {'first_name' : 'A', 'last_name' : 'B', 'ssn': '000-00-0000'}
        self.id2_data = {'first_name' : 'C', 'last_name' : 'D', 'ssn' : '222-22-2222'}

        self.id2_employee_task = [{'task' : 'X',
                                  'task_date' : datetime.datetime.now(),
                                  'time_duration' : datetime.timedelta(minutes=5, hours=1),
                                  'note' : 'Z'
                                }, {'task' : 'M',
                                    'task_date' : datetime.datetime.now(),
                                    'time_duration' : datetime.timedelta(minutes=10, hours=0),
                                    'note' : 'N'
                                }]

 



    def test_duplicates_in_db(self):
        print("One")
        test_emps = [self.id1_data for _ in range(2)]

        with self.assertRaises(IntegrityError):
            self.DB_MODELS[0].insert_many(test_emps).execute()

    # def test_del_employee(self):
    #     pass


    def test_relationships(self):
        print("Two")
        employee_2 = self.DB_MODELS[0].create(**self.id2_data)

        for test_task in self.id2_employee_task:
            test_task['employee'] = employee_2
        self.DB_MODELS[1].insert_many(self.id2_employee_task).execute()
        items = self.DB_MODELS[1].select().where(Task.employee == employee_2)

        self.assertTrue(all(test.employee.ssn == '222-22-2222' for test in items))



    # @classmethod
    # def tearDownClass(cls):
    #     test_db.drop_tables(cls.DB_MODELS)

if __name__ == '__main__':
    unittest.main()

