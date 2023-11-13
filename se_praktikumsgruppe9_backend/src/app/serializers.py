from rest_framework import serializers

from .models import Log, DataTupel


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Log
        fields=('id','recorded_time','action','initiator_id')

class DataTupelSerializer(serializers.ModelSerializer):
    class Meta:
        model=DataTupel
        fields=('relative_time','bool_value','float_value','string_value','column_id')