from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import *
from .models import Employee
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from project import settings
from django.core.paginator import Paginator
from django.views.generic import (
	TemplateView, 
	ListView, 
	CreateView,
	DetailView,
	UpdateView,
	DeleteView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


from rest_framework import viewsets
from .serializers import EmployeeSerializers


class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializers




def employees_data(request):
    a=Employee.objects.order_by('-ename')[:]
    num_visit = request.session.get('num_visit',1)
    print(num_visit)
    request.session['num_visit']=num_visit+1
    return render(request,'employees_data.html',{'record':a,'nv':num_visit})



class Employeedelete(DeleteView):
	pass

class EmployeeDetail(DetailView):
	template_name = 'employee_list.html'
	#queryset = Employee.objects.all()
	    
	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Employee,id=id_)		

class EmployeeAdd(CreateView):
	template_name = 'employeeadd.html'
	form_class = NameForm
#	success_url = '/myapp/show'


class Employeeupdate(SuccessMessageMixin, UpdateView):
	model = Employee
	fields = ['ename','econtact']

	# def test_func(self):
	# 	employee = self.get_object()
	# 	return employee.id==self.user.id
	success_message = 'Thank You'	
'''		
	template_name = 'employeeadd.html'
	form_class = NameForm
	success_url = '/myapp/show'

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(Employee,id=id_)	

'''
@login_required()
def index(request):
	if request.method=='POST':
		form=NameForm(request.POST,request.FILES)	
		if form.is_valid():
			form.save() 
			return redirect('/myapp')
		else:
			return HttpResponse("<h1>Sorry</h1>")		
	else:
		form=NameForm()
	context={'form':form}
	return render(request,'index.html',context)

def show(request):
	profile_list = Employee.objects.get_queryset().filter(eid__gte=2).order_by('-eid')
	paginator = Paginator(profile_list, 2)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	#?page = 2
	context={"employees":posts}
	print(paginator.page_range)
	return render(request,'show.html',context)

@login_required()
def delete(request,id):
	data=Employee.objects.get(id=id)
	data.delete()
	messages.warning(request,f'Employee {id} has been deleted.')
	return redirect('/myapp/show')

@login_required()
def update(request,id):
	data=Employee.objects.get(id=id)
	emp=NameForm(instance=data)
	context={'form':emp}
	return render(request,'index.html',context)

def search(request):
	search_box=request.POST['searchbox']
	data=Employee.objects.filter(ename__icontains=search_box)
	context={'employees':data}
	return render(request,'show.html',context)

def register(request):
	if request.method=='POST':
		form1=userform(request.POST)
		if form1.is_valid():
			username=form1.cleaned_data['username']
			first_name = form1.cleaned_data['first_name']
			last_name = form1.cleaned_data['last_name']
			email = form1.cleaned_data['email']
			password = form1.cleaned_data['password']
			User.objects.create_user(username=username,
			first_name=first_name,last_name=last_name,
			email=email,password=password)
			subject="Confirmation Mail"
			msg="Dear Sir/Ma'am,thank YOU "
			send_mail(subject,msg,settings.EMAIL_HOST_USER,[email])
			return HttpResponse('Thank YOu')
	else:
		form1=userform()	
	context = {'form':form1}
	return render(request,'registration.html',context)

def loginuser(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return request
		else:
			return HttpResponse('<h1>invalid</h1>')   
	return render(request,'login.html')	
	

def logoutuser(request):
	logout(request)
	return render(request,'login.html')   	

def changepassword(request):
    user=request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            return redirect('login')
    else:
        form = ChangePasswordForm()
    return render(request,'password.html',{'form':form}) 

class HomeView(TemplateView):
	template_name='home.html' 		

class EmployeeListView(ListView):
	template_name = 'show2.html'
	model = Employee

	# def get_queryset(self):
	# 	qs1 = Employee.objects.all() #your first qs
	# 	qs2 = User.objects.all() #your second qs
 #        #you can add as many qs as you want
	# 	queryset = dict(zip(qs1,qs2))
	# 	return qs1,qs2	
	
	def get_context_data(self, **kwargs):
		context = super(EmployeeListView,self).get_context_data(**kwargs)
		qs1 = User.objects.all()
		qs2 = Employee.objects.all()
		context.update({
			'users' : qs1,
			'employees' : qs2
			})
		return context

'''	
class MyFormView(View):
    form_class = NameForm()
    initial = {'key': form_class}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
class MyFormView(View):
	form_class = NameForm()
	intial = {'key' : form}
	template_name = 'website/index.html'
	
	def get(self,request,*args,**kwargs):
		form=self.form_class(initial=self.intial)
		return render(request, self.template_name, {'form': form_class})	

'''		

# from .serializers import UserSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status



# class UserViewSet(APIView):

#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
