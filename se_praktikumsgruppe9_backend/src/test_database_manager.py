from django.test import TestCase

from database_manager import *


class UserFunctionsTestCase(TestCase):
    """
        Tests the functions of the database manager which correspond to users
    """

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass1234')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass1234')
        self.user3 = User.objects.create_user('user3', 'user3@test.com', 'pass1234')
        self.user4 = User.objects.create_user('user4', 'user4@test.com', 'pass1234')

    def test_read_user_data(self):
        """
        tests if the expected UserData for a specific user is correct
        """
        user = read_user_data(1)
        self.assertEqual(user, {'id': 1, 'last_login': None, 'is_superuser': False,
                                'username': 'user1', 'email': 'user1@test.com',
                                'is_active': True, 'is_admin': False,
                                'is_data_analyst': False, 'is_simulation_engineer': False, 'is_data_owner': False,
                                'is_staff': False, 'groups': [], 'user_permissions': []})

    def test_read_user_data2(self):
        """
        tests if the expected UserData for a specific user is correct
        """
        user = read_user_data(4)
        self.assertEqual(user, {'id': 4, 'last_login': None, 'is_superuser': False, 'username': 'user4',
                                'email': 'user4@test.com', 'is_active': True, 'is_admin': False,
                                'is_data_analyst': False, 'is_simulation_engineer': False, 'is_data_owner': False,
                                'is_staff': False, 'groups': [], 'user_permissions': []})

    def test_read_nonexisting_user(self):
        """
        tests if the specific user exists
        """
        try:
            read_user_data(10)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_get_all_userdata(self):
        """
        test if all expected userdata is returned
        """
        data = get_all_userdata()
        self.assertEqual(data, [
            {'id': 1, 'last_login': None, 'is_superuser': False, 'username': 'user1', 'email': 'user1@test.com',
             'is_active': True, 'is_admin': False, 'is_data_analyst': False, 'is_simulation_engineer': False,
             'is_data_owner': False, 'is_staff': False, 'groups': [], 'user_permissions': []},
            {'id': 2, 'last_login': None, 'is_superuser': False, 'username': 'user2', 'email': 'user2@test.com',
             'is_active': True, 'is_admin': False, 'is_data_analyst': False, 'is_simulation_engineer': False,
             'is_data_owner': False, 'is_staff': False, 'groups': [], 'user_permissions': []},
            {'id': 3, 'last_login': None, 'is_superuser': False, 'username': 'user3', 'email': 'user3@test.com',
             'is_active': True, 'is_admin': False, 'is_data_analyst': False, 'is_simulation_engineer': False,
             'is_data_owner': False, 'is_staff': False, 'groups': [], 'user_permissions': []},
            {'id': 4, 'last_login': None, 'is_superuser': False, 'username': 'user4', 'email': 'user4@test.com',
             'is_active': True, 'is_admin': False, 'is_data_analyst': False, 'is_simulation_engineer': False,
             'is_data_owner': False, 'is_staff': False, 'groups': [], 'user_permissions': []}])

    def test_is_owner(self):
        """
            tests if the user is the creator of the written metadata
        """
        testCsv = pd.read_csv('src/testCsvData/testCsv.csv')
        weirdCsv = pd.read_csv('src/testCsvData/smallWeirdTestCsv1.csv')
        write_raw_data('user1data', 1, testCsv, 'time_first_single')
        write_raw_data('user1data2', 3, weirdCsv, 'time_alternating')

        self.assertTrue(is_owner(1, 1))
        self.assertFalse(is_owner(1, 4))
        self.assertTrue(is_owner(2, 3))

    def test_get_user_name_by_id(self):
        """
        tests if the function correctly returns the username related to the given userID
        """
        self.assertEqual(get_user_name_by_id(3), 'user3')

    def test_get_user_name_by_id2(self):
        """
        tests if the function correctly returns the username related to the given userID
        """
        self.assertNotEqual(get_user_name_by_id(1), 'user3')

    def test_get_user_name_by_id_error(self):
        """
        tests if the function throws an error if the user doesn't exist
        """
        try:
            self.assertEqual(get_user_name_by_id(9), 'non existing')
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_get_user_id_by_name(self):
        """
        tests if the function correctly returns the id related to the given username
        """
        self.assertEqual(get_user_id_by_name('user2'), 2)

    def test_get_user_id_by_name2(self):
        """
        tests if the function correctly returns the id related to the given username
        """
        self.assertNotEqual(get_user_id_by_name('user4'), 2)

    def test_get_user_id_by_name_error(self):
        """
        tests if the function throws an error if the user doesn't exist
        """
        try:
            self.assertEqual(get_user_id_by_name('non existing'), 9)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

class DataTestCase(TestCase):
    """
        Tests the data-functions of the database manager
    """

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass1234')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass1234')
        self.user3 = User.objects.create_user('user3', 'user3@test.com', 'pass1234')
        self.user4 = User.objects.create_user('user4', 'user4@test.com', 'pass1234')

        self.testCsv = pd.read_csv('src/testCsvData/testCsv.csv')
        self.weirdTestCsv = pd.read_csv('src/testCsvData/weirdTestCsv.csv')

    def test_metadata_name_to_id(self):
        """
        tests if the correct metadata name is returned
        """
        write_raw_data('user1data', 1, self.testCsv, 'time_first_single')
        write_raw_data('user2data', 2, self.weirdTestCsv, 'time_alternating')
        self.assertEqual(metadata_name_to_id("user1data"), 1)
        self.assertEqual(metadata_name_to_id("user2data"), 2)

    def test_metadata_name_to_id_error(self):
        write_raw_data('user1data', 1, self.testCsv, 'time_first_single')
        try:
            metadata_name_to_id("non existing")
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_name_is_available(self):
        """
        tests if the given data name is already taken or still available
        """
        write_raw_data('user1data', 1, self.testCsv, 'time_first_single')
        assert not (name_is_available('user1data'))
        assert name_is_available('user2data')

    def test_get_all_metadata(self):
        """
        tests if the metadata returned is correct
        """
        write_raw_data('user1data1', 1, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', 1, self.testCsv, 'time_first_single')
        write_raw_data('user2data1', 2, self.testCsv, 'time_first_single')

        assert get_all_metadata()[1][0]['id'] == 1
        assert get_all_metadata()[1][0]['name'] == 'user1data1'
        assert get_all_metadata()[1][0]['creator'] == get_user_name_by_id(1)
        assert get_all_metadata()[2][0]['id'] == 3
        assert get_all_metadata()[2][0]['name'] == 'user2data1'
        assert get_all_metadata()[2][0]['creator'] == get_user_name_by_id(2)

    def test_get_all_metadata_for_specific_user(self):
        """
        tests if the returned metadata for a specific user is correct
        """
        write_raw_data('user1data1', 1, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', 1, self.testCsv, 'time_first_single')
        write_raw_data('user2data1', 2, self.testCsv, 'time_first_single')

        assert get_all_metadata(2)[2][0]['id'] == 3
        assert get_all_metadata(2)[2][0]['name'] == 'user2data1'
        assert get_all_metadata(2)[2][0]['id'] != 1

    def test_dropped_duplicates_in_time_column(self):
        """
        tests if duplicate columns are dropped
        """
        write_raw_data('user1data1', 1, self.testCsv, 'time_first_single')

        df_good_to_filter, metadata = read_data_for_filtering(1)
        df_to_test = pd.read_csv('src/testCsvData/smallResultCsv.csv', skipinitialspace=True)
        assert df_good_to_filter.equals(df_to_test)

    def test_weirdCsvColumn_not_dropped(self):
        """
        tests if single duplicate columns are not dropped when time_schema is 'time_alternating'
        """
        write_raw_data('user2data1', 2, self.weirdTestCsv, 'time_alternating')

        df_weird_to_test2 = pd.read_csv('src/testCsvData/smallWeirdTestCsv2.csv', skipinitialspace=True)
        df_weird_to_filter2, metadata = read_data_for_filtering(3)
        assert df_weird_to_filter2.equals(df_weird_to_test2)

    def test_read_data_for_filtering(self):
        """
        tests if the data for filtering returned is correct
        """
        write_raw_data('user1data1', 1, self.testCsv, 'time_first_single')
        df_good_to_filter, metadata = read_data_for_filtering(1)
        df_to_test = pd.read_csv('src/testCsvData/smallResultCsv.csv', skipinitialspace=True)
        assert df_good_to_filter.equals(df_to_test)

        write_raw_data('user2data1', 2, self.weirdTestCsv, 'time_alternating')
        df_weird_to_test1 = pd.read_csv('src/testCsvData/smallWeirdTestCsv1.csv', skipinitialspace=True)
        df_weird_to_filter, metadata = read_data_for_filtering(6)
        assert df_weird_to_filter.equals(df_weird_to_test1)

        df_weird_to_test2 = pd.read_csv('src/testCsvData/smallWeirdTestCsv2.csv', skipinitialspace=True)
        df_weird_to_filter2, metadata = read_data_for_filtering(7)
        assert df_weird_to_filter2.equals(df_weird_to_test2)

    def tests_exist_data(self):
        """
        tests if the metadata exists after writing
        """
        meta_id = 1
        user_id = 1
        write_raw_data('user1data1', user_id, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', user_id, self.testCsv, 'time_first_single')
        assert MetaData.objects.filter(id=meta_id).exists()

    def test_delete_data(self):
        """
        tests if the metadata got deleted correctly, depending on metadataID and userID
        tests if the cascading effect took place
        """
        meta_id = 1
        user_id = 1
        write_raw_data('user1data1', user_id, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', user_id, self.testCsv, 'time_first_single')
        delete_data(meta_id, user_id)
        assert not MetaData.objects.filter(id=meta_id).exists()
        assert not Column.objects.filter(meta_data=meta_id).exists()

    def test_delete_data_username(self):
        """
        tests if the metadata got deleted correctly, depending on metadataID and username
        tests if the cascading effect took place
        """
        meta_id = 1
        user_name = 'user1'
        user_id = 1
        write_raw_data('user1data1', user_id, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', user_id, self.testCsv, 'time_first_single')
        delete_data_username(meta_id, user_name)
        assert not MetaData.objects.filter(id=meta_id).exists()
        assert not Column.objects.filter(meta_data=meta_id).exists()
        assert MetaData.objects.filter(id=2).exists()

    def test_delete_data_of_user(self):
        """
        tests if the metadata got deleted correctly, depending and userID
        tests if the cascading effect took place
        """
        meta_id = 1
        user_id = 1
        write_raw_data('user1data1', user_id, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', user_id, self.testCsv, 'time_first_single')
        write_raw_data('user2data1', 2, self.testCsv, 'time_first_single')
        delete_data_of_user(user_id)
        assert not MetaData.objects.filter(id=meta_id).exists()
        assert not Column.objects.filter(meta_data=meta_id).exists()
        assert not MetaData.objects.filter(id=2).exists()
        assert MetaData.objects.filter(creator=2).exists()

    def test_column_id_to_meta_data_id(self):
        """
        tests if the given columnID corresponds to the correct metadataID
        """
        write_raw_data('user1data1', 1, self.testCsv, 'time_first_single')
        write_raw_data('user1data2', 1, self.testCsv, 'time_first_single')
        assert column_id_to_meta_data_id(1) == 1
        assert column_id_to_meta_data_id(2) == 1
        assert column_id_to_meta_data_id(3) == 1
        assert column_id_to_meta_data_id(4) == 1
        assert not column_id_to_meta_data_id(1) == 2
        assert column_id_to_meta_data_id(5) == 2

    def test_dataypes(self):
        write_raw_data('user1data1', 1, self.weirdTestCsv, 'time_alternating')
        value_column = Column.objects.get(id=1)
        bigbool_column = Column.objects.get(id=2)
        strings_column = Column.objects.get(id=3)

        self.assertIn(str(value_column.value_data_type), ["float", "Float64", "float64", "int64", "Int64"])
        self.assertIn(str(bigbool_column.value_data_type), ["bool", "boolean"])
        self.assertIn(str(strings_column.value_data_type), ["string", "str"])


class LogTestCase(TestCase):
    """
    Tests the Log-functions

    Anmerkung: Wenn Daten dabei sind, bei denen das Datum beim Erstellen des Tests hinzugefügt wird, können die
    Ergebnisse des Tests nicht hardgecodet werden
    """

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass1234')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'pass1234')
        self.user3 = User.objects.create_user('user3', 'user3@test.com', 'pass1234')
        self.user4 = User.objects.create_user('user4', 'user4@test.com', 'pass1234')
        write_logdata("Added a logdata", 1, datetime(2022, 12, 24, 4, 13, 21))
        write_logdata("Another logdata", 1, datetime(2023, 3, 10, 5, 2, 32))
        write_logdata("Someone else did something", 2)
        write_logdata("Dude 1 was productive again", 1, datetime(2023, 3, 19, 1, 10, 45))
        write_logdata("Dude 4 joined the chaos", 4, datetime(2023, 3, 25, 11, 11, 11))
        # der folgende Eintrag ist eigentlich vorher entstanden, aber hat größere ID
        write_logdata("Started everything", 2, datetime(2018, 3, 2, 6, 4, 6))

    def test_read_all_logdata(self):
        """
        Checks, if the function returns every entry
        """
        all_logdata = read_all_logdata()
        # prüft, dass wirklich Daten gesammelt wurden
        self.assertIs(len(all_logdata), 6)

    def test_read_logdata_of_user(self):
        """
        Checks, if the restrictions regarding users are fullfilled
        """
        filtered_logdata = read_all_logdata([1])
        # prüft, dass wirklich Daten gesammelt wurden
        self.assertTrue(filtered_logdata)
        # prüft, dass auch wirklich nur die Daten des Initiator 1 ausgelesen werden
        self.assertEqual(filtered_logdata,
                         [{'id': 4, 'initiator': 1, 'timestamp': '2023-03-19 01:10:45',
                           'action': 'Dude 1 was productive again'},
                          {'id': 2, 'initiator': 1, 'timestamp': '2023-03-10 05:02:32',
                           'action': 'Another logdata'},
                          {'id': 1, 'initiator': 1, 'timestamp': '2022-12-24 04:13:21',
                           'action': 'Added a logdata'}])

    def test_read_logdata_of_user2(self):
        """
        Checks, if the restrictions regarding users are fullfilled
        """
        filtered_logdata = read_all_logdata([1, 3, 4])
        # prüft, dass wirklich Daten gesammelt wurden
        self.assertEqual(filtered_logdata, [{'id': 5, 'initiator': 4, 'timestamp': '2023-03-25 11:11:11',
                                             'action': 'Dude 4 joined the chaos'},
                                            {'id': 4, 'initiator': 1, 'timestamp': '2023-03-19 01:10:45',
                                             'action': 'Dude 1 was productive again'},
                                            {'id': 2, 'initiator': 1, 'timestamp': '2023-03-10 05:02:32',
                                             'action': 'Another logdata'},
                                            {'id': 1, 'initiator': 1, 'timestamp': '2022-12-24 04:13:21',
                                             'action': 'Added a logdata'}])

    def test_read_logdata_of_nonexistent_user(self):
        """
        Checks, if no logdata is returned if the user doesn't exist
        """
        logdata = read_all_logdata(user_ids=[10])
        # prüft, dass wirklich keine Daten gesammelt wurden
        self.assertFalse(logdata)

    def test_read_time_filtered_data(self):
        """
        Checks, if the restrictions regarding start time are fullfilled
        """
        start_time = datetime(2023, 3, 10)
        logdata = read_all_logdata(start_time=start_time)
        self.assertIs(len(logdata), 4)

    def test_read_time_filtered_data2(self):
        """
        Checks, if the restrictions regarding start- and end-time are fullfilled
        """
        start_time = datetime(2020, 9, 12)
        end_time = datetime(2023, 3, 13)
        logdata = read_all_logdata(start_time=start_time, end_time=end_time)
        self.assertEqual(logdata, [{'id': 2, 'initiator': 1, 'timestamp': '2023-03-10 05:02:32',
                                    'action': 'Another logdata'},
                                   {'id': 1, 'initiator': 1, 'timestamp': '2022-12-24 04:13:21',
                                    'action': 'Added a logdata'}])

    def test_read_logdata_of_user_and_time_filtered(self):
        """
        Checks, if the restrictions regarding users and start- and end-time are fullfilled
        """
        start_time = datetime(2020, 9, 12)
        end_time = datetime(2023, 3, 13)
        logdata = read_all_logdata([2], start_time=start_time, end_time=end_time)
        self.assertFalse(logdata)

    def test_read_logdata_of_user_and_time_filtered2(self):
        """
        Checks, if the restrictions regarding users and end-time are fullfilled
        """
        end_time = datetime(2023, 3, 13)
        logdata1 = read_all_logdata(end_time=end_time)
        logdata2 = read_all_logdata([2], end_time=end_time)
        self.assertEqual(logdata1, [{'id': 2, 'initiator': 1, 'timestamp': '2023-03-10 05:02:32',
                                     'action': 'Another logdata'},
                                    {'id': 1, 'initiator': 1, 'timestamp': '2022-12-24 04:13:21',
                                     'action': 'Added a logdata'},
                                    {'id': 6, 'initiator': 2, 'timestamp': '2018-03-02 06:04:06',
                                     'action': 'Started everything'}])
        self.assertNotEqual(logdata1, logdata2)
