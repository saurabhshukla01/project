from rest_framework import serializers
from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ('ename','eemail','econtact','url')		




class EmployeeSerializers(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('first_name','last_name','url')

		