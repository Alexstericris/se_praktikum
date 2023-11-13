from functools import wraps
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response


def required_roles(*roles):

    def decorator(function):

        @wraps(function)
        def wrap(request, *args, **kwargs):

            roles_functions = {"admin": request.user.is_admin,
                               "data_analyst": request.user.is_data_analyst,
                               "simulation_engineer": request.user.is_simulation_engineer,
                               "data_owner": request.user.is_data_owner}

            if any([roles_functions[role] for role in roles]):
                return function(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return wrap

    return decorator
