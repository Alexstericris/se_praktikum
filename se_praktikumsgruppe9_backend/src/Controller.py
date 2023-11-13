from enum import Enum
from typing import List, Union, Dict, Any

import pandas as pd
from io import StringIO


import database_manager as datamanager
from FilterManager import FilterManager

from datetime import datetime


filtermanager = FilterManager()


class Controller:

    def __init__(self, user_id):
        self.user_ID = user_id

    def get_all_metadata(self, all: bool):
        """
        returns all metadata
        :param all: if all is true, returns all user_metadata, else only of the current user
        :return: dict of user_id and list of dict of (id, name, time_recorded, creator_is, base_id)
        """
        user_id = None if all else self.user_ID

        result = datamanager.get_all_metadata(user_id)

        self.write_log_data("get_all_meta_data")

        if all:
            DataRespose = []
            for k, v in result.items():
                DataRespose.append({"username": datamanager.get_user_name_by_id(k), "filenames": v})
            return {"userdata": DataRespose}
        else:
            fileMetadata = result[user_id]
            return {"username": datamanager.get_user_name_by_id(user_id), "filenames": fileMetadata}

    def write_data(self, unique_name: str, schema: str, delimiter: str, csv: str) -> int:
        """
        writes raw data into the databank
        :param unique_name: name of the table
        :param schema: time_schema
        :param delimiter: the delimiter used in the data
        :param csv: data to write
        :return: metadata id
        """
        csvStringIO = StringIO(csv)
        csvStringIO.seek(0)
        df = pd.read_csv(csvStringIO, sep=delimiter, comment="#", skipinitialspace=True, engine='python')
        result = datamanager.write_raw_data(unique_name, self.user_ID, df, schema)
        self.write_log_data("write_data")
        return result


    def is_owner(self, meta_data_id: int, user_id: int) -> bool:
        """
        checks whether user is owner of the data
        :param meta_data_id: id of metadata
        :param user_id: ID of user
        :return: true if owner, else false
        """
        return datamanager.is_owner(meta_data_id, user_id)

    def read_data(self, column_id: int) -> pd.DataFrame:
        """
        reads the data of the meta_data
        :param column_id: id of data
        :return: the read data
        """
        result, meta_id = datamanager.read_data_for_filtering(column_id)
        self.write_log_data("read_data")
        return result

    def filter_data(self, x_and_y_values: pd.DataFrame, filter_functions: List, params: list[list]) -> pd.DataFrame:
        """
        filters the data with given filter functions
        :params x_and_y_values: contains data to be filtered as int or float values
        :params filter_functions: List of filter functions numbers
        :params params: parameters for filter functions
        :return: filtered data
        """
        result = filtermanager.filterFunctions(x_and_y_values, filter_functions, params)
        self.write_log_data(f"filter_data with functions: {filter_functions}")
        return result

    def write_filter_data(self, unique_name: str, df: pd.DataFrame, base_id: int, functions: List[int]) -> int:
        """
        writes filtered data into the databank
        :param unique_name: name of the table
        :param df: data to write
        :param base_id: id of the user who created the original data
        :param functions: list of applied functions
        :return: metadata id
        """
        result = datamanager.write_filter_data(unique_name, self.user_ID, df, base_id, functions)
        self.write_log_data("write_filter_data")
        return result

    def delete_data(self, meta_data_id: int) -> bool:
        """
        deletes data of the given meta data id
        :param meta_data_id: id of meta data
        :return: true if successful, else false
        """
        result = datamanager.delete_data(meta_data_id, self.user_ID)
        self.write_log_data(f"delete_data of {meta_data_id}")
        return result

    def get_all_userdata(self) -> list[dict[str, Any]]:
        """
        returns all user data
        :return: List[dict[user_id, name, is_Admin, is_DataAnalyst, is_DataOwner, is_Simulationsengineer]]
        """
        result = datamanager.get_all_userdata()

        result = [{"username": result[i]["username"], "userid": result[i]["id"], "isAdmin": result[i]["is_admin"],
                   "isDataOwner": result[i]["is_data_owner"],
                   "isSimulationEngineer": result[i]["is_simulation_engineer"],
                   "isDataAnalyst": result[i]["is_data_analyst"]}
                  for i in range(len(result))]

        self.write_log_data("get_all_user_data")
        return result

    def read_user_data(self, user_id: int) -> dict[str, Any]:
        """
        returns user data of one user
        :param user_id: ID of one user
        :return: dict[user_id, name,  is_Admin, is_DataAnalyst, is_DataOwner, is_Simulationsengineer]
        """
        result = datamanager.read_user_data(user_id)

        result = {"username": result["username"], "userid": result["id"], "isAdmin": result["is_admin"],
                   "isDataOwner": result["is_data_owner"],
                   "isSimulationEngineer": result["is_simulation_engineer"],
                   "isDataAnalyst": result["is_data_analyst"]}

        self.write_log_data("read_user_data")
        return result

    def delete_userdata(self, user_id: int) -> bool:
        """
        deletes user data of one user
        :param user_id: ID of one user
        :return: true if successful, else false
        """
        result = datamanager.delete_data_of_user(user_id)
        self.write_log_data(f"delete_user_data of {user_id}")
        return result

    def write_log_data(self, action: str) -> bool:
        """
        logs performed action
        :param action: performed action
        :return: true if successful, else false
        """
        return datamanager.write_logdata(action, self.user_ID)

                                                                                # log_id, user_id, time, action
    def read_all_log_data(self, user_ids=[], start_time=None, end_time=None) -> list[dict[str:Union[str, int]]]:
        """
        returns whole log
        :return: List[Dict[Time, Action, Name]]
        """
        result = datamanager.read_all_logdata(user_ids, start_time, end_time)
        res = []
        for dict in result:
            res.append({"timestamp": dict["timestamp"], "action": dict["action"], "userName": self.get_user_by_id(dict["initiator"])})
        self.write_log_data("read_all_log_data")
        return res

    def is_filename_available(self, filename: str) -> bool:
        """
        returns True if filename is available, else False
        """
        return datamanager.name_is_available(filename)

    def get_user_by_id(self, user_id: int) -> str:
        """
        returns the name of der given user_id
        """
        return datamanager.get_user_name_by_id(user_id)

    def get_userid_by_name(self, name: str) -> int:
        """
        returns the UserID of the given name
        """
        return datamanager.get_user_id_by_name(name)

    def column_id_to_meta_data_id(self, column_id) -> int:
        """
        retruns the metadata ID which corresponds to the given column ID
        """
        return datamanager.column_id_to_meta_data_id(column_id)
