from django.db import IntegrityError

from user.models import User
from django.test import TestCase
from Controller import *
from core.settings import BASE_DIR

import numpy as np
import pandas as pd

CSV_TESTFILE = str(BASE_DIR / "testCsvData" / "CSVLog_20171014_144445.csv")

class UserFunctionsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass1234')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass1234')
        self.user3 = User.objects.create_user('user3', 'user3@test.com', 'pass1234')
        self.user4 = User.objects.create_user('user4', 'user4@test.com', 'pass1234')

        self.csv_string = """time(sec),value 
                0,0
                1,1
                2,4
                3,9
                4,16
                5,25"""

        self.test_csv = open('src/testCsvData/testCsv.csv', 'r').read()

    # def test_something(self):
    #     self.assertNotEqual(True, False)  # add assertion here
    #
    # def test_something2(self):
    #     self.assertEqual(True, True)  # add assertion here

    def test_write_data(self):
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")
        self.assertEqual(met_id, 1)

    def test_write_data_2(self):
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        data = contr.read_data(1)

        self.assertListEqual(data["Time (sec)"].to_list(), [0, 1, 2, 3, 4, 5])
        self.assertListEqual(data["value "].to_list(), [0,1,4,9,16,25])

    def test_write_data_error(self):
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")
        self.assertEqual(met_id, 1)

        self.assertRaises(IntegrityError, lambda: contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=","))

    def test_read_data(self):
        #write Sample Data
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        #read Data
        df = contr.read_data(1)
        self.assertIsNotNone(df)

        self.assertListEqual(df["Time (sec)"].to_list(), [0, 1, 2, 3, 4, 5])
        self.assertListEqual(df["value "].to_list(), [0, 1, 4, 9, 16, 25])

    def test_read_data_error(self):
        #write Sample Data
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        #read Data
        self.assertRaises(ValueError, lambda: contr.read_data(1000))

    def test_get_all_metadata(self):
        # write Sample Data
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        res = contr.get_all_metadata(all=True)
        userdata = res["userdata"]
        self.assertEqual(4, len(userdata))
        user0_files = userdata[0]["filenames"]
        self.assertIsNotNone(user0_files)



    def test_delete_data(self):
        # write Sample Data
        time_schema = "time_first_single"
        contr = Controller(user_id=self.user1.id)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")
        met_id2 = contr.write_data(unique_name="Testdataname2", csv=self.test_csv, schema=time_schema, delimiter=",")

        # delete Sample Data
        res1 = contr.delete_data(met_id)
        res2 = contr.delete_data(met_id2)

        self.assertEqual(res1, True)
        self.assertEqual(res2, True)


    def test_filter_data_1(self):
        # eine Filter-Funktion (die 7.) benutzen
        x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
        y = np.array([1, 2, 3, 4, 5, 6])
        x_and_y_values = pd.DataFrame({"X": x, "Y": y})

        x_to_interpolate = np.array([1, 2, 3, 4, 5, 6])
        filter_functions = [6]
        params = [[x_to_interpolate]]

        contr = Controller(user_id=1)

        result = contr.filter_data(x_and_y_values, filter_functions, params)

        self.assertListEqual(result["Y"].to_list(), [1, 1, 2, 3, 4, 5])

    def test_filter_data_2(self):
        # zwei Filter Funktionen hintereinander anwenden (erst 2 dann 7)
        x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
        y = np.array([1, 2, 3, np.NAN, 5, 6])
        x_and_y_values = pd.DataFrame({"X": x, "Y": y})

        x_to_interpolate = np.array([1, 2, 3, 4, 5, 6])
        filter_functions = [1, 6]
        params = [[],[x_to_interpolate]]

        contr = Controller(user_id=1)

        result = contr.filter_data(x_and_y_values, filter_functions, params)

        self.assertListEqual(result["Y"].to_list(), [1, 1, 2, 3, 4, 5])

    def test_filter_data_error(self):
        x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
        y = np.array([1, 2, 3, 4, 5, 6])
        x_and_y_values = pd.DataFrame({"X": x, "Y": y})

        x_to_interpolate = np.array([1, 2, 3, 4, 5, 6])
        filter_functions = [6]
        params = [[x_to_interpolate]]

        contr = Controller(user_id=1)

        self.assertRaises(KeyError, lambda: contr.filter_data(x_and_y_values, [1000], params))
        self.assertRaises(ValueError, lambda: contr.filter_data(x_and_y_values, filter_functions, []))

    def test_is_owner(self):
        # user 1 writes Data
        time_schema = "time_first_single"
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        # check if the user is now owner
        is_true_owner = contr.is_owner(met_id, 1)
        self.assertTrue(is_true_owner)

        #check that another user is not owner
        is_not_owner = contr.is_owner(met_id, 2)
        self.assertFalse(is_not_owner)

    def test_write_filter_data(self):
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema="time_first_single", delimiter=",")

        string = "Time (sec),Y\n1.0,2.0\n3.0,4.0"
        csv = StringIO(string)
        # csv.seek(0)
        df = pd.read_csv(csv, sep=",", comment="#", skipinitialspace=True)

        new_met_id = contr.write_filter_data("baum", df, met_id, [1])
        stored_data = contr.read_data(new_met_id)
        self.assertTrue(df.equals(stored_data))
        self.assertIsInstance(new_met_id, int)
        self.assertNotEqual(met_id, new_met_id)



    def test_get_all_userdata_1(self):
        contr = Controller(user_id=1)
        result = contr.get_all_userdata()

        expected_result = [{"username": 'user1', "userid": 1, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False,"isDataAnalyst": False},
                           {"username": 'user2', "userid": 2, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False,"isDataAnalyst": False},
                           {"username": 'user3', "userid": 3, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False},
                           {"username": 'user4', "userid": 4, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False}]

        self.assertListEqual(result, expected_result)


    def test_get_all_userdata_2(self):
        contr = Controller(user_id=1)
        # noch einen User hinzufügen
        self.user4 = User.objects.create_user('user5', 'user5@test.com', 'pass1234', is_admin=True)

        result = contr.get_all_userdata()

        expected_result = [{"username": 'user1', "userid": 1, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False,"isDataAnalyst": False},
                           {"username": 'user2', "userid": 2, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False,"isDataAnalyst": False},
                           {"username": 'user3', "userid": 3, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False},
                           {"username": 'user4', "userid": 4, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False},
                           {"username": 'user5', "userid": 5, "isAdmin": True, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False}]

        self.assertListEqual(result, expected_result)


    def test_delete_userdata(self):
        contr = Controller(user_id=1)
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema="time_first_single", delimiter=",")

        user_files = contr.get_all_metadata(False)["filenames"]
        self.assertIsNotNone(user_files[0]["name"])

        contr.delete_userdata(1)

        user_files = contr.get_all_metadata(False)["filenames"]
        self.assertEqual([], user_files)


    def test_read_user_data_1(self):
        contr = Controller(user_id=1)
        result = contr.read_user_data(1)

        expected_result = {"username": 'user1', "userid": 1, "isAdmin": False, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False}

        self.assertDictEqual(result, expected_result)

    def test_read_user_data_2(self):
        contr = Controller(user_id=5)

        # noch einen User hinzufügen
        self.user5 = User.objects.create_user('user5', 'user5@test.com', 'pass1234', is_admin=True)
        result = contr.read_user_data(5)

        expected_result = {"username": 'user5', "userid": 5, "isAdmin": True, "isDataOwner": False, "isSimulationEngineer": False, "isDataAnalyst": False}

        self.assertDictEqual(result, expected_result)

    def test_write_log_data_1(self):
        contr = Controller(user_id=1)
        result = contr.write_log_data("HelloWorld")

        self.assertTrue(result)

        # print(contr.read_all_log_data([1]))
        # [{'id': 1, 'initiator': 1, 'recorded_time': '2023-03-15 10:57:22', 'action': 'HelloWorld'}]
        # Da Zeit immer variiert unten nicht überprüft

        read_result = contr.read_all_log_data([1])

        self.assertEqual(len(read_result), 1)
        self.assertEqual(read_result[0]["id"], 1)
        self.assertEqual(read_result[0]["initiator"], 1)
        self.assertEqual(read_result[0]["action"], "HelloWorld")

    def test_write_log_data_2(self):
        # Test mit mehreren Usern
        contr = Controller(user_id=1)
        result = contr.write_log_data("HelloWorld")
        self.assertTrue(result)
        contr = Controller(user_id=2)
        result = contr.write_log_data("HelloWorld")
        self.assertTrue(result)

        read_result = contr.read_all_log_data([1,2])

        self.assertEqual(len(read_result), 2)
        self.assertEqual(read_result[0]["id"], 1)
        self.assertEqual(read_result[0]["initiator"], 1)
        self.assertEqual(read_result[0]["action"], "HelloWorld")

    def test_read_all_log_data_1(self):
        # Test, ob nur Log der übergebenen ID zurückgegeben werden
        contr = Controller(user_id=1)
        result = contr.write_log_data("HelloWorld")
        self.assertTrue(result)
        contr = Controller(user_id=2)
        result = contr.write_log_data("HelloWorld")
        self.assertTrue(result)

        read_result = contr.read_all_log_data([1])

        self.assertEqual(len(read_result), 1)
        self.assertEqual(read_result[0]["id"], 1)
        self.assertEqual(read_result[0]["initiator"], 1)
        self.assertEqual(read_result[0]["action"], "HelloWorld")

    def test_read_all_log_data_2(self):
        # Test, Log von mehreren IDs zurückgeben
        contr = Controller(user_id=1)
        result = contr.write_log_data("HelloWorld")
        self.assertTrue(result)
        contr = Controller(user_id=2)
        result = contr.write_log_data("HelloWorld2")
        self.assertTrue(result)

        read_result = contr.read_all_log_data([1,2])

        self.assertEqual(len(read_result), 2)
        self.assertEqual(read_result[0]["id"], 1)
        self.assertEqual(read_result[0]["initiator"], 1)
        self.assertEqual(read_result[0]["action"], "HelloWorld")
        self.assertEqual(read_result[1]["id"], 2)
        self.assertEqual(read_result[1]["initiator"], 2)
        self.assertEqual(read_result[1]["action"], "HelloWorld2")


    def test_is_filename_available(self):
        contr = Controller(user_id=1)
        time_schema = "time_first_single"

        # Name noch nicht in Gebrauch -> ist verfügbar
        result = contr.is_filename_available("Testdataname")
        self.assertTrue(result)

        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        # Name schon in Gebrauch -> ist nicht mehr verfügbar
        result = contr.is_filename_available("Testdataname")
        self.assertFalse(result)

    def test_get_user_by_id(self):
        contr = Controller(user_id=1)

        # der angemeldete User
        result = contr.get_user_by_id(1)
        self.assertEqual(result, "user1")

        # ein nicht angemeldeter User
        result = contr.get_user_by_id(2)
        self.assertEqual(result, "user2")

    def test_get_userid_by_name(self):
        contr = Controller(user_id=1)

        # der angemeldete User
        result = contr.get_userid_by_name("user1")
        self.assertEqual(result, 1)

        # ein nicht angemeldeter User
        result = contr.get_userid_by_name("user2")
        self.assertEqual(result, 2)

    def test_column_id_to_meta_data_id(self):
        contr = Controller(user_id=1)

        time_schema = "time_first_single"
        met_id = contr.write_data(unique_name="Testdataname", csv=self.csv_string, schema=time_schema, delimiter=",")

        result = contr.column_id_to_meta_data_id(met_id)
        self.assertEqual(result, 1)

