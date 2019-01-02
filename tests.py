import unittest  # built-ins, python standard library
import datetime

from peewee import *  # third-party

import main # custom script, package, module

test_db = SqliteDatabase('dummy.db')

class TestDatabase(unittest.TestCase):
    DB_MODELS = [main.Employee, main.Task]

    @classmethod
    def setUpClass(cls):
        test_db.connect(reuse_if_open=True)
        test_db.bind(cls.DB_MODELS)

        if all(test_db.table_exists(db_model) for db_model in cls.DB_MODELS):
            test_db.drop_tables()
        test_db.create_tables(cls.DB_MODELS)

    def setUp(self):
        self.employee_info = main.Database.get_employee_data()

    def test_employee_in_db(self):
        pass

      
       
        


if __name__ == '__main__':
    unittest.main()

