from datetime import datetime

from django.contrib.auth import load_backend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from app.models import Log
from app.serializers import LogSerializer, DataTupelSerializer
from database_manager import write_raw_data

from user.models import User

from Controller import Controller

from app.decorators import required_roles


# Create your views here.
# from src import database_manager


class LogView(APIView):
    def get(self, request, *args, **kwargs):
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DataTupelView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        columnData = request.user.getColumnData(name=request.GET.get('columnName'))
        serializer = DataTupelSerializer(columnData, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def isTokenValid(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return Response({"valid": True}, status=status.HTTP_200_OK)
        else:
            return Response({"valid": False}, status=status.HTTP_200_OK)

"""
@api_view(['POST'])
def loginUser(request):
    response = ""
    return response
"""

@api_view(['POST'])
@login_required()
@required_roles("admin")
def getLog(request):
    if request.method == 'POST':
        user_names = request.data.get("userNames")
        if user_names is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_id = request.user.id
        controller = Controller(user_id)

        # slicing:
        try:
            to = datetime.strptime(request.data.get("to"), "%Y-%m-%d %H:%M:%S")
        except:
            to = None

        try:
            fr = datetime.strptime(request.data.get("from"), "%Y-%m-%d %H:%M:%S")
        except:
            fr = None

        if user_names:
            user_ids = [controller.get_userid_by_name(name) for name in user_names]
        else:
            user_ids = []
        try:
            log_data = controller.read_all_log_data(user_ids=user_ids, start_time=fr, end_time=to)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"logEntries": log_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
@login_required()
@required_roles("simulation_engineer", "data_analyst")
def filterApply(request):
    if request.method == 'POST':
        column_id = request.data.get("databaseColumnIdInput")
        filter_ids = request.data.get("filter")
        parameter = request.data.get("parameter")

        if column_id is None or filter_ids is None or parameter is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        controller = Controller(user_id)
        try:
            data = controller.read_data(column_id)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        keys = data.columns

        # slicing:
        try:
            to = request.data.get("to")
        except:
            to = None

        try:
            fr = request.data.get("from")
        except:
            fr = None

        if not to and not fr:
            data = data
        elif not to:
            data = data[(data[keys[0]] <= to)]
        elif not fr:
            data = data[(fr <= data[keys[0]])]
        else:
            data = data[(fr <= data[keys[0]]) & (data[keys[0]] <= to)]

        # filtering:
        if filter_ids:
            try:
                result = controller.filter_data(data, filter_ids, parameter)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            result = data

        column_entries = []
        for _, row in result.iterrows():
            column_entries.append({"timestamp": row[result.columns[0]], "value": row[result.columns[1]]})

        result = {
            "data": {
                "data": column_entries,
                # todo: replace column header with unit
                "unit": keys[1]
            }
        }

        return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required()
@required_roles("simulation_engineer")
def filterApplySave(request):
    if request.method == 'POST':
        column_id = request.data.get("databaseColumnIdIn")
        filter_ids = request.data.get("Filter")
        parameter = request.data.get("Parameter")
        table_name = request.data.get("DatabaseIdOutput")

        if column_id is None or filter_ids is None or parameter is None or table_name is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        controller = Controller(user_id)
        try:
            data = controller.read_data(column_id)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        keys = data.columns

        # slicing:
        try:
            to = request.data.get("to")
        except:
            to = None

        try:
            fr = request.data.get("from")
        except:
            fr = None

        if to == None and fr == None:
            pass
        elif to == None:
            data = data[(data[keys[0]] <= to)]
        elif fr == None:
            data = data[(fr <= data[keys[0]])]
        else:
            data = data[(fr <= data[keys[0]]) & (data[keys[0]] <= to)]

        if not filter_ids:
            # raise ValueError("no filter functions specified")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            result = controller.filter_data(data, filter_ids, parameter)
            base_id = controller.column_id_to_meta_data_id(column_id)
            controller.write_filter_data(table_name, result, base_id, filter_ids)
        except:
            # TODO: Catch Error of Filterfunctions
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
@login_required()
def isFilenameAvailable(request):
    if request.method == 'POST':
        filename = request.data.get("name")
        if filename is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_id = request.user.id
        controller = Controller(user_id)
        try:
            res = controller.is_filename_available(filename)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"available": res}, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required()
@required_roles("data_owner")
def uploadFile(request):
    if request.method == 'POST':
        name = request.data.get("name")
        schema = request.data.get("typeOfSchema")
        delimiter = request.data.get("delimiter")
        data_string = request.data.get('csv')

        if name is None or schema is None or delimiter is None or data_string is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        controller = Controller(user_id)
        try:
            controller.write_data(name, schema, delimiter, data_string)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required()
@required_roles("admin")
def deleteFile(request):
    if request.method == 'POST':
        data_id = request.data.get("fileId")

        if data_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        user_id = user.id
        controller = Controller(user_id)
        try:
            controller.delete_data(data_id)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required()
@required_roles("data_owner")
def getMyFilenames(request):
    if request.method == 'GET':
        user_id = request.user.id
        controller = Controller(user_id)
        try:
            res = controller.get_all_metadata(False)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res)


@api_view(['GET'])
@login_required()
@required_roles("simulation_engineer", "data_analyst", "admin")
def getAllUserFilenames(request):
    if request.method == 'GET':
        user_id = request.user.id
        controller = Controller(user_id)
        try:
            res = controller.get_all_metadata(True)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res)

@api_view(['GET'])
@login_required()
def getMyUserInformation(request):
    if request.method == "GET":
        user_id = request.user.id
        controller = Controller(user_id)
        try:
            data = controller.read_user_data(user_id)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data)
