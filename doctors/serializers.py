from rest_framework import serializers
from users.models import User
from doctors.models import Doctor, Schedule
from users.serializers import UserSerializer, BasicUserSerializer 

class DoctorSerializer(serializers.ModelSerializer):
       class Meta:
        model = Doctor
        fields = ("__all__")

       def to_representation(self, instance):
              response = super().to_representation(instance)
              response['user'] = UserSerializer(instance.user).data
              return response

class BasicDoctorSerializer(serializers.ModelSerializer):
       class Meta:
           model = Doctor
           fields = ['id', 'speciality']

       def to_representation(self, instance):
              response = super().to_representation(instance)
              response['user'] = BasicUserSerializer(instance.user).data
              return response 

class ScheduleListSerializer(serializers.ListSerializer):
       def create(self, validated_data):
              schedules = [Schedule(**item) for item in validated_data]
              return Schedule.objects.bulk_create(schedules)

       def update(self, instance, validated_data):
              schedule_mapping = {Schedule.id: schedule for schedule in instance}
              data_mapping = {item['id']: item for item in validated_data}

              ret = []
              for schedule_id, data in data_mapping.items():
                     schedule = schedule_mapping.get(schedule_id, None)
                     if schedule is None:
                            ret.append(self.child.create(data))
                     else:
                            ret.append(self.child.update(schedule, data))

              for schedule_id, schedule in schedule_mapping.items():
                     if schedule_id not in data_mapping:
                            schedule.delete()
              return ret

class ScheduleSerializer(serializers.ModelSerializer):
       id = serializers.IntegerField(read_only=False)

       class Meta:
              model = Schedule
              fields = '__all__'
              list_serializer_class = ScheduleListSerializer