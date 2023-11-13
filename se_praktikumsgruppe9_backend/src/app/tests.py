import pandas as pd
from core.settings import BASE_DIR
from database_manager import write_raw_data, metadata_name_to_id, metadata_id_to_name
from django.urls import include, path
from rest_framework.test import APITestCase
# Create your tests here.
from user.models import User

CSV_TESTFILE = BASE_DIR / "testCsvData" / "CSVLog_20171014_144445.csv"


class AppTestCase(APITestCase):
    urlpatterns = [
        path('', include('core.urls')),
    ]

    def setUp(self):
        self.password = "1234"
        self.dummy_user_1 = User.objects.create_user("user1", "bla@bla.de", self.password,
                                                     is_admin=True,
                                                     is_data_analyst=True,
                                                     is_simulation_engineer=True,
                                                     is_data_owner=True)
        response = self.client.post('/api/auth/login/', {
            "username": self.dummy_user_1.username,
            "password": self.password,
        }, format='json')

        self.token = response.data["access"]

        # All User Roles
        # Admin User:
        self.admin_user = User.objects.create_user("admin", "admin@bla.de", self.password, is_admin=True)
        admin_response = self.client.post('/api/auth/login/', {
            "username": self.admin_user.username,
            "password": self.password,
        }, format='json')
        self.admin_user_token = admin_response.data["access"]

        # Data Analyst User:
        self.data_analyst_user = User.objects.create_user("data_analyst", "data_analyst@bla.de", self.password,
                                                          is_data_analyst=True)
        data_analyst_response = self.client.post('/api/auth/login/', {
            "username": self.data_analyst_user.username,
            "password": self.password,
        }, format='json')
        self.data_analyst_token = data_analyst_response.data["access"]

        # Simulation Engineer User:
        self.simulation_engineer_user = User.objects.create_user("simulation_engineer", "simulation_engineer@bla.de",
                                                                 self.password,
                                                                 is_simulation_engineer=True)
        simulation_engineer_response = self.client.post('/api/auth/login/', {
            "username": self.simulation_engineer_user.username,
            "password": self.password,
        }, format='json')
        self.simulation_engineer_token = simulation_engineer_response.data["access"]

        # Data Owner User:
        self.data_owner_user = User.objects.create_user("data_owner", "data_owner@bla.de", self.password,
                                                        is_data_owner=True)
        data_owner_response = self.client.post('/api/auth/login/', {
            "username": self.data_owner_user.username,
            "password": self.password,
        }, format='json')
        self.data_owner_token = data_owner_response.data["access"]

        # Admin + Data Owner User:
        self.admin_data_owner_user = User.objects.create_user("admin_data_owner", "admin_data_owner@bla.de",
                                                              self.password, is_admin=True, is_data_owner=True)
        admin_data_owner_response = self.client.post('/api/auth/login/', {
            "username": self.admin_data_owner_user.username,
            "password": self.password,
        }, format='json')
        self.admin_data_owner_token = admin_data_owner_response.data["access"]

        # creating dummy entry

        self.dataName = "rawdata2"
        self.csvPath = BASE_DIR / 'testCsvData/CSVLog_20171201_113205(fast).csv'
        df = pd.read_csv(self.csvPath, delimiter=",", comment="#", skipinitialspace=True)

        self.timeScheme = "time_first_single"
        write_raw_data(self.dataName, self.dummy_user_1.id, df, self.timeScheme)

    def test_MyFilenames(self):
        response = self.client.get('/getMyFilenames/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_MyFilenames_1(self):
        response = self.client.get('/getMyFilenames/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(response.json()["username"], self.dummy_user_1.username)
        self.assertIsInstance(response.json()["filenames"], list)

    def test_AllUserfilenames(self):
        response = self.client.get('/getAllUserFilenames/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_getMyUserInformation(self):
        response = self.client.get('/getMyUserInformation/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'username': 'user1', 'userid': 1, 'isAdmin': True, 'isDataOwner': True,
                                         'isSimulationEngineer': True, 'isDataAnalyst': True})

    def test_getMyUserInformation_1(self):
        response = self.client.get('/getMyUserInformation/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)

        user_id = self.dummy_user_1.id
        user_name = self.dummy_user_1.username
        user_is_admin = self.dummy_user_1.is_admin
        user_is_data_owner = self.dummy_user_1.is_data_owner
        user_is_simulation_engineer = self.dummy_user_1.is_simulation_engineer
        user_is_data_analyst = self.dummy_user_1.is_data_analyst

        self.assertEqual(response.json()['username'], user_name)
        self.assertEqual(response.json()['userid'], user_id)
        self.assertEqual(response.data.get('isAdmin'), user_is_admin)
        self.assertEqual(response.data.get('isDataOwner'), user_is_data_owner)
        self.assertEqual(response.data.get('isSimulationEngineer'), user_is_simulation_engineer)
        self.assertEqual(response.data.get('isDataAnalyst'), user_is_data_analyst)

    def test_loginUser(self):
        usr_name = "user2"
        dummy_user_2 = User.objects.create_user(usr_name, "blabla@bla.de", self.password, is_data_owner=True)

        response = self.client.post('/api/auth/login/', {'username': usr_name, "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dummy_user_2.is_active, True)
        self.assertIsNotNone(response.data["access"])
        self.assertTrue(response.data["user"]["is_data_owner"])
        self.assertFalse(response.data["user"]["is_admin"])
        self.assertFalse(response.data["user"]["is_data_analyst"])
        self.assertFalse(response.data["user"]["is_simulation_engineer"])


    def test_getLog(self):
        response = self.client.post('/getLog/',
                                    {"from": "0", "to": "3", "wrong Key": ["user1", "data_analyst"]},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/getLog/',
                                    {"from": "0", "to": "3", "userNames": ["user1", "data_analyst"]},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.client.post("/filterApply/", {
            "databaseColumnIdInput": 1,
            "filter": [],
            "parameter": [],
            "from": 1,
            "to": 2
        }, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/getLog/',
                                    {"from": "0", "to": "3", "userNames": ["user1", "data_analyst"]},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["logEntries"])
        self.assertIsNotNone(response.json()["logEntries"][0]["timestamp"])
        self.assertIsNotNone(response.json()["logEntries"][0]["action"])
        self.assertIsNotNone(response.json()["logEntries"][0]["userName"])


    def test_filterApply(self):
        response = self.client.post("/filterApply/", {
            "databaseColumnIdInput": 1,
            "filter": [],
            "parameter": [],
            "from": 1,
            "to": 2
        }, format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json()["data"]["data"],
            [{'timestamp': 1.038, 'value': 0.0}, {'timestamp': 1.144, 'value': 0.0},
             {'timestamp': 1.319, 'value': 0.0}, {'timestamp': 1.442, 'value': 0.0}]
        )

    def test_filterApply2(self):
        response = self.client.post("/filterApply/",
                                    {"databaseColumnIdInput": 1,
                                     "filter": [10, 11],
                                     "parameter": [[1, 2], []],
                                     "from": 1,
                                     "to": 2},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 500)  # Filter existieren nicht

    def test_filterApplySave(self):
        response = self.client.post("/filterApplySave/",
                                    {"databaseColumnIdIn": 1,
                                     "DatabaseIdOutput": "testName2tztztz",
                                     "Filter": [1],
                                     "Parameter": [[]],
                                     "from": 1,
                                     "to": 2},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(metadata_name_to_id("testName2tztztz"))

    def test_isFilenameAvailable_True(self):
        response = self.client.post("/isFilenameAvailiable/",
                                    {"name": "notInDB"},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["available"], True)

    def test_isFilenameAvailable_False(self):
        # check for dataName already in db
        response = self.client.post("/isFilenameAvailiable/",
                                    {"name": self.dataName},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        b = response
        self.assertEqual(response.json()["available"], False)
        self.assertEqual(response.status_code, 200)

    def test_uploadFile(self):
        response = self.client.post("/uploadFile/",
                                    {"name": "", "typeOfSchema": "time_first_single", "delimiter": ",",
                                     "csv": """time,value1,value2,value3\n1,5,2,True\n3,6,4,False\n6,8,4,True"""},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_uploadFile2(self):
        response = self.client.post("/uploadFile/",
                                    {"name": "meinTEst", "typeOfSchema": "time_alternating", "delimiter": ",",
                                     "csv": """time,value1,time2,value2\n1,5,2,True\n3,6,4,False\n6,8,4,True"""},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_upload_file_error(self):
        response = self.client.post("/uploadFile/",
                                    {"name": "", "delimiter": ",",
                                     "csv": """time,value1,value2,value3\n1,5,2,True\n3,6,4,False\n6,8,4,True"""},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 400)

    def test_deleteFile_success(self):
        # successful call
        response = self.client.post("/deleteFile/", {"fileId": 1}, format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
        try:
            metadata_id_to_name(1)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_deleteFile_failure(self):
        # try to delete file not in db
        response = self.client.post("/deleteFile/", {"fileId": 2}, format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 400)

        # try to delete file while not logged in
        response = self.client.post("/deleteFile/", {"fileId": 1}, format='json')
        self.assertEqual(response.status_code, 302)

        # try to deleteFile by FileName:
        response = self.client.post("/deleteFile/", {"fileId": self.dataName}, format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 400)

        self.assertIsNotNone(metadata_id_to_name(1))

    def test_isTokenValid(self):
        response = self.client.get('/isTokenValid/', format='json', HTTP_AUTHORIZATION='Bearer ' + self.token)
        print(response.json())
        self.assertEqual(response.json()["valid"], True)

    def test_isTokenValid2(self):
        response = self.client.get('/isTokenValid/', format='json')
        print(response.json())
        self.assertEqual(response.json()["valid"], False)

    # ROLE TESTING:
    def test_getLog_admin(self):
        response = self.client.post('/getLog/',
                                    {"from": "0", "to": "3", "userNames": ["user1", "data_analyst"]},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.admin_user_token)
        self.assertEqual(response.status_code, 200)

    def test_getLog_admin_and_dataowner(self):
        response = self.client.post('/getLog/',
                                    {"from": "0", "to": "3", "userNames": ["user1", "data_analyst"]},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.admin_data_owner_token)
        self.assertEqual(response.status_code, 200)

    def test_getLog_otherrole(self):
        response = self.client.post('/getLog/',
                                    {"from": "0", "to": "3", "userNames": ["user1", "data_analyst"]},
                                    format='json',
                                    HTTP_AUTHORIZATION='Bearer ' + self.data_analyst_token)
        self.assertEqual(response.status_code, 401)

    def test_AllUserfilenames_required_roles(self):
        response_simulation_engineer = self.client.get('/getAllUserFilenames/',
                                                       format='json',
                                                       HTTP_AUTHORIZATION='Bearer ' + self.simulation_engineer_token)
        self.assertEqual(response_simulation_engineer.status_code, 200)

        response_data_analyst = self.client.get('/getAllUserFilenames/',
                                                format='json',
                                                HTTP_AUTHORIZATION='Bearer ' + self.data_analyst_token)
        self.assertEqual(response_data_analyst.status_code, 200)

        response_admin = self.client.get('/getAllUserFilenames/',
                                         format='json',
                                         HTTP_AUTHORIZATION='Bearer ' + self.admin_user_token)
        self.assertEqual(response_admin.status_code, 200)

    def test_AllUserfilenames_rejected_roles(self):
        response_data_owner = self.client.get('/getAllUserFilenames/',
                                              format='json',
                                              HTTP_AUTHORIZATION='Bearer ' + self.data_owner_token)
        self.assertEqual(response_data_owner.status_code, 401)
