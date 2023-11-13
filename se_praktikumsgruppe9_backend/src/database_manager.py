from datetime import datetime
from typing import Dict, List, Union

import pandas as pd
from django.forms.models import model_to_dict

from app.Functions import *
from app.models import Column, MetaData, DataTupel, Log
from user.models import User

ID = int


# User-Funktionalitäten #################################################
def read_user_data(user_id: ID):
    """
    :return: dict of the data of the user with the given id, but without the password
    """
    try:
        user_data = model_to_dict(User.objects.get(id=user_id))
        user_data.pop('password', None)
        return user_data
    except:
        raise ValueError(f"The given UserID: {user_id} does not exist in the database!")


def get_all_userdata():
    """
    :return: list with all user data as dictionaries (without the password and session data)
    """
    all_user_objects = User.objects.all()
    result = []
    for user in all_user_objects:
        dict_user = model_to_dict(user)
        dict_user.pop('password', None)
        dict_user.pop('session_data', None)
        result.append(dict_user)
    return result


def is_owner(metadata_id: ID, user_id: ID):
    """
    :return: returns if the user is the creator of the data
    """
    try:
        return MetaData.objects.get(id=metadata_id).creator == User.objects.get(id=user_id)
    except Exception:
        raise ValueError(f"The given MetaDataID: {metadata_id} and/ or UserID: {user_id} do not exist!")


def get_user_name_by_id(user_id: ID) -> str:
    """
    :return: returns the name of the user with the given id
    """
    try:
        return User.objects.get(id=user_id).username
    except Exception:
        raise ValueError(f"The given UserID: {user_id} does not exist!")


def get_user_id_by_name(user_name: str) -> ID:
    """
    :return: returns the ID of the user with the given name
    """
    try:
        return User.objects.get(username=user_name).id
    except Exception:
        raise ValueError(f"The given UserName: {user_name} is not recognizable!")


# Daten-Funktionalitäten ####################################

def name_is_available(table_name: str) -> bool:
    """
    :param table_name: the name thats supposed to be checked
    :return: returns if the given table_name is still available
    """
    all_metadata = MetaData.objects.all()
    for metadata in all_metadata:
        if table_name == metadata.name:
            return False
    return True


def get_all_metadata(user_id=None) -> Dict[ID, List]:
    """
    :param user_id: UserID
    :return: returns a Dictionary with UserID as Keys and Lists of Dictionary's of MetaData
    these Dictionary's contain the row of the MetaData-Table in our Database with a List of Columns
    """

    def get_userspecified_data():
        """
        :return: returns the UserID's
        """
        if user_id is not None:
            existing_user = User.objects.filter(id=user_id).exists()
            if existing_user:
                user_ids = [user_id]
            else:
                raise ValueError("User does not exist!")
        else:
            user_ids = []
            user = User.objects.all()
            for u in user:
                user_ids.append(u.id)
        return user_ids

    ids = get_userspecified_data()
    user_dict = {}
    for id in ids:
        all_metadata_objects = MetaData.objects.select_related().filter(creator_id=id).all()
        metadata_list = [model_to_dict(user) for user in all_metadata_objects]
        for metadata in metadata_list:
            cols = Column.objects.select_related().filter(meta_data=metadata['id'])
            columns = []
            for col in cols:
                columns.append({"name": col.name, "id": col.id})
            metadata['columns'] = columns
            metadata.update({"timeRecorded": metadata["time_recorded"].strftime("%Y-%m-%d %H:%M:%S")})
            metadata.pop("time_recorded")
            metadata.update({"baseId": metadata["base"]})
            metadata.pop("base")
            metadata.update({"creator": get_user_name_by_id(metadata["creator"])})

        user_dict[User.objects.get(id=id).id] = metadata_list
    return user_dict


def write_raw_data(data_name: str, user_id: ID, dataframe: pd.DataFrame, time_schema: str, base=None,
                   applied_filters=None):
    """
    A Function to write (raw) Data into the Database - modified to also accept filtered Data
    :param data_name: The name of the to be written data
    :param user_id: The UserID of the DataOwner
    :param dataframe: The given DataFrame
    :param time_schema: The given TimeSchema (time_first_single || time_alternating)
    :param base: The Base-MetaData if filtered Data is given
    :param applied_filters: The applied Filters if filtered Data is given
    :return: returns the MetaData-Object
    """
    if applied_filters is None:
        applied_filters = []

    def save_metadata(user, base):
        """
        A Function to save the MetaData into our Database
        :param user: Creator
        :param base: Base-MetaData if filtered Data is given
        :return: returns the written MetaData
        """
        # mok_current_time = datetime(2015, 10, 9, 23, 55, 59, 342380)
        current_time = datetime.now()
        if base is not None:
            try:
                metabase = MetaData.objects.get(id=base)
            except Exception:
                raise ValueError(f"The given Base: {base} does not exists!")
            new_metadata = MetaData(name=data_name, time_recorded=current_time, creator=user, base=metabase)
            new_metadata.save()
        else:
            new_metadata = MetaData(name=data_name, time_recorded=current_time, creator=user, base=None)
            new_metadata.save()
        return new_metadata

    dataframe = dataframe.drop_duplicates()
    if time_schema == 'time_first_single':
        dataframe = dataframe.drop_duplicates(subset=[dataframe.columns[0]])
    # pd.read_csv(csv, comment='#', skipinitialspace=True, delimiter=delim, low_memory=False)
    column_names = dataframe.columns

    if time_schema == 'time_alternating':
        for i in range(0, len(column_names), 2):
            time_column = dataframe[column_names[i]]
            value_list = []
            for value in dataframe[time_column.name]:
                if type(value) == float or type(value) == bool or type(value) == int:
                    value_list.append(value)
                else:
                    value = value.replace('.', '', value.count('.') - 1)
                    value_list.append(float(value))
            dataframe[time_column.name] = value_list
        for i in range(1, len(column_names) - 1, 2):
            value_column = dataframe[column_names[i]]
            if isinstance(dataframe[value_column.name][0], str):
                dataframe[value_column.name] = dataframe[value_column.name].astype('|S')

    def save_columns(metadata: MetaData):
        """
        A Function to save all columns given by the DataFrame
        :param metadata: the given MetaData written in save_metadata
        :return: return the newly written column information
        """
        new_column_information = []
        if time_schema == "time_first_single":
            schema = list(zip(dataframe.columns, dataframe.dtypes))
            correct_schema = schema[1:]
            for column, datatype in correct_schema:
                new_column = Column(name=column, unit=None, value_data_type=datatype, applied_filters=applied_filters,
                                    meta_data=metadata)
                new_column.save()
                new_column_information.append((new_column.name, new_column.id, new_column.value_data_type))
        elif time_schema == "time_alternating":
            for index in range(0, len(dataframe.columns), 2):
                dataframe_subset = dataframe[[column_names[index], column_names[index + 1]]].dropna(
                    how='all').convert_dtypes()
                schema = list(zip(dataframe_subset.columns, dataframe_subset.dtypes))
                correct_schema = schema[1:]
                for column, datatype in correct_schema:
                    new_column = Column(name=column, unit=None, value_data_type=datatype,
                                        applied_filters=applied_filters,
                                        meta_data=metadata)
                    new_column.save()
                    new_column_information.append((new_column.name, new_column.id, new_column.value_data_type))

        else:
            raise ValueError("A correct time schema has to be given!")
        return new_column_information

    def save_datatupels(column: Column, column_type: any, time_values: List[float], column_data_values):
        """
        A Function to save the DataTupel for every Column into the Databank
        :param column: The specific Column to save the DataTupel in
        :param column_type: The ColumnType (float || string || bool)
        :param time_values: The values for the TimeColumn
        :param column_data_values: The values for the DataValuesColumn
        :return: nothing, but writes the DataTupel into the Databank
        """
        datatupel_list = []
        if str(column_type) in ["bool", "boolean"]:
            for time, data in zip(time_values, column_data_values):
                if time is None:
                    break
                new_datatupel = DataTupel(relative_time=time, bool_value=data, float_value=None, string_value=None,
                                          column=column)
                datatupel_list.append(new_datatupel)
            DataTupel.objects.bulk_create(datatupel_list)
        elif str(column_type) in ["float", "int64", "float64", "Float64", "Int64"]:
            for time, data in zip(time_values, column_data_values):
                if time is None:
                    break
                new_datatupel = DataTupel(relative_time=time, bool_value=None, float_value=data, string_value=None,
                                          column=column)
                datatupel_list.append(new_datatupel)
            DataTupel.objects.bulk_create(datatupel_list)
        elif str(column_type) in ["string", "str"]:
            for time, data in zip(time_values, column_data_values):
                if time is None:
                    break
                new_datatupel = DataTupel(relative_time=time, bool_value=None, float_value=None, string_value=data,
                                          column=column)
                datatupel_list.append(new_datatupel)
            DataTupel.objects.bulk_create(datatupel_list)
        else:
            raise ValueError(f"{column_type} is a wrong columntype")

    try:
        user = User.objects.get(id=user_id)
    except Exception:
        raise ValueError(f"The given UserID: {user_id} does not exists!")

    new_metadata = save_metadata(user, base)
    new_column_information = save_columns(new_metadata)

    if time_schema == "time_first_single":
        schema = list(zip(dataframe.columns, dataframe.dtypes))
        time = schema[0][0]
        for column_name, column_id, column_type in new_column_information:
            column_obj = Column.objects.get(id=column_id)
            time_data = dataframe[time]
            column_values = dataframe[column_name]
            save_datatupels(column_obj, column_type, time_data, column_values)

    # wir gehen davon aus, dass die columns immer in der richtigen Reihenfolge bleiben!!!
    elif time_schema == "time_alternating":
        for index in range(0, len(dataframe.columns), 2):
            dataframe_subset = dataframe[[column_names[index], column_names[index + 1]]].dropna(
                how='all').convert_dtypes()
            schema = list(zip(dataframe_subset.columns, dataframe_subset.dtypes))
            time = schema[0][0]

            column_name, column_id, column_type = new_column_information[index // 2]
            column_obj = Column.objects.get(id=column_id)
            time_data = dataframe_subset[time]
            column_values = dataframe_subset[column_name]
            save_datatupels(column_obj, column_type, time_data, column_values)
    else:
        raise ValueError(f"Given TimeSchema: {time_schema} is not recognizable.")

    metadata = MetaData.objects.get(name=data_name).id
    return metadata


def write_filter_data(data_name: str, user_id: ID, dataframe: pd.DataFrame, raw_metaddata_id: ID,
                      applied_filters: List[int]):
    """
    :param data_name: The
    :param user_id:
    :param dataframe:
    :param raw_metaddata_id:
    :param applied_filters:
    :return:
    """
    time_schema = "time_first_single"
    return write_raw_data(data_name=data_name, user_id=user_id, dataframe=dataframe, time_schema=time_schema,
                          base=raw_metaddata_id, applied_filters=applied_filters)


def read_data_for_filtering(column_id: ID):
    """
    :param column_id: The specific ColumnID to be filtered
    :return: returns a Dataframe consisting of the selected Value Column together with its specific Time Column
    """
    try:
        df = pd \
            .DataFrame(list(DataTupel.objects.select_related().filter(column_id=column_id).values())) \
            .dropna(axis=1, how='all') \
            .drop(['id', 'column_id'], axis=1)
    except Exception:
        raise ValueError(f"The given Column ID: {column_id} doesnt exist!")
    df.columns = ['Time (sec)', Column.objects.get(id=column_id).name]
    metadata_id = Column.objects.select_related().get(id=column_id).meta_data.id
    return df, metadata_id


def delete_data(metadata_id: ID, user_id: ID):
    """
    Deletes the demanded metadata
    :param metadata_id: the metadata ID of the data which should be deleted
    :param user_id: the creator_id of the data which should be deleted
    :return: None
    """
    try:
        MetaData.objects.get(id=metadata_id, creator=user_id).delete()
        return True
    except Exception:
        raise ValueError(f"The given MetaDataID: {metadata_id} and/ or UserID: {user_id} do not exist!")


# Delete (User-)Data
def delete_data_username(metadata_id: ID, user_name):
    """
    Deletes the demanded metadata
    :param metadata_id: the metadata ID of the data which should be deleted
    :param user_name: the name of the creator whose data should be deleted
    :return: None
    """
    try:
        user_id = User.objects.get(username=user_name).id
    except Exception:
        raise ValueError(f"The given Username: {user_name} does not exist!")
    try:
        MetaData.objects.get(id=metadata_id, creator=user_id).delete()
        return True
    except Exception:
        raise ValueError(f"The given MetaDataID: {metadata_id} does not exist!")


def delete_data_of_user(user_id: ID):
    """
    Deletes all data entries of this user
    """
    try:
        metadata_to_delete = MetaData.objects.filter(creator=user_id)
    except Exception:
        raise ValueError(f"The given UserID: {user_id} does not exist!")
    for metadata in metadata_to_delete:
        metadata.delete()
    return True


# Find ID's by other ID's/ Names
def column_id_to_meta_data_id(column_id):
    """
    :param column_id: the column whose metadata ID is demanded
    :return: the metadata ID which corresponds to the given column ID
    """
    try:
        return Column.objects.get(id=column_id).meta_data.id
    except Exception:
        raise ValueError(f"The given ColumnID: {column_id} does not exist!")


def metadata_name_to_id(metadata_name):
    """
    Returns the ID to the metadata name
    """
    try:
        return MetaData.objects.get(name=metadata_name).id
    except Exception:
        raise ValueError(f"The given MetaData-Name: {metadata_name} does not exist!")


def metadata_id_to_name(metadata_id):
    """
    Returns the name of the given metadata id
    """
    try:
        return MetaData.objects.get(id=metadata_id).name
    except Exception:
        raise ValueError(f"The given MetaData-ID: {metadata_id} does not exist!")


# Log-Funktionalitäten ####################################
def write_logdata(action: str, user_id: ID, time: datetime = datetime.now()):
    """
    Saves the given logdata information in the database
    :param action: Description of the action that was executed
    :param user_id: the ID of the user who executed the action
    :param time: the time the action was executed, per default the current time
    :return: the saved logdata-record
    """
    try:
        user = User.objects.get(id=user_id)
    except Exception:
        raise ValueError(f"The given UserID: {user_id} does not exist!")
    new_logdata = Log(initiator=user, recorded_time=time, action=action)
    new_logdata.save()
    return new_logdata


def read_all_logdata(user_ids=None, start_time:datetime=None, end_time:datetime=None, newest_first=True) -> list[
    dict[str:Union[str, int]]]:
    """
    Gets the logdata-entries with certain optional restrictions
    :param user_ids: list of the IDs of the users whose log-entries should be returned, per default empty
    :param start_time: only entries with recorded_time >= start_time are going to be returned, per default None
    :param end_time:  only entries with recorded_time <= end_time are going to be returned, per default None
    :param newest_first: sorted descending by the entry with the newest recorded_time
    :return: the demanded logdata-entries
    """
    if user_ids is None:
        user_ids = []
    if not user_ids:
        all_logdata_objects = Log.objects.all()
    else:
        all_logdata_objects = Log.objects.filter(initiator_id__in=user_ids).all()

    if start_time:
        all_logdata_objects = all_logdata_objects.filter(recorded_time__gte=start_time)
    if end_time:
        all_logdata_objects = all_logdata_objects.filter(recorded_time__lte=end_time)

    logdata_list = [model_to_dict(logdata) for logdata in all_logdata_objects]
    logdata_list_res = sorted(logdata_list, key=lambda d: d["recorded_time"], reverse=newest_first)
    for d in logdata_list_res:
        d.update({"timestamp": d["recorded_time"].strftime("%Y-%m-%d %H:%M:%S")})
        d.pop("recorded_time")
    return logdata_list_res
