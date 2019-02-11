from django.urls import path
from .views import *

urlpatterns = [
	path('add',index,name='add'),
	path('show/',show,name='show'),
	path('delete/<int:id>',delete,name='delete'),
	path('update/<int:id>',update,name='update'),
	path('search/',search,name='search'),
	path('registration/',register,name='register'),
	path('login/',loginuser,name='login'),
	path('logout/',logoutuser,name='logout'),
	path('changepassword/',changepassword,name='password'),
	path('home/',HomeView.as_view(),name='home'),
	path('show2/',EmployeeListView.as_view(),name='show2'),
	path('show3/<int:id>/',EmployeeDetail.as_view(),name='detail'),
	path('employeeadd/',EmployeeAdd.as_view(),name='emp_add'),
	path('employeeupdate/<int:pk>',Employeeupdate.as_view(),name='emp_update'),
	path('employeedelete/<int:id>',Employeedelete.as_view(),name='emp_delete'),
]