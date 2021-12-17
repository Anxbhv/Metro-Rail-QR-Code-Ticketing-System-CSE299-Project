
from django.shortcuts import render,redirect
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView

from .forms import GeneralUserSignUpForm,TrainMasterSignUpForm,OrderForm
from .models import User,GeneralUser,Book,Route





def SignUp(request):
	return render(request,'register.html')


def log(request):
    """
    This method is used to view the login page.
    :param request: it's a HttpResponse from user.
    :type request: HttpResponse.
    :return: this method returns a search page which is a HTML page.
    :rtype: HttpResponse.
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
          if request.method == 'POST':
              username =request.POST.get('guser_name')
              password =request.POST.get('guser_password')
             
              user= authenticate(request, username=username, password=password)

              if user is not None and user.is_guser:
                  login(request, user)
                  return redirect('home')
              elif user is not None and user.is_trainmaster:
                  messages.info(request, 'This  is for general users only, You are a Train Master')
              else:
                 messages.info(request, 'Username or Password is incorrect')
            

    context= {}
    return render(request, 'login.html', context)

def log2(request):
    """
    This method is used to view the login page.
    :param request: it's a HttpResponse from user.
    :type request: HttpResponse.
    :return: this method returns a search page which is a HTML page.
    :rtype: HttpResponse.
    """
    if request.user.is_authenticated:
        return redirect('home')
    else:
          if request.method == 'POST':
              username =request.POST.get('trainmaster_name')
              password =request.POST.get('trainmaster_password')
             
              user= authenticate(request, username=username, password=password)

              if user is not None and user.is_trainmaster:
                  login(request, user)
                  return redirect('home')
              elif user is not None and user.is_guser:
                  messages.info(request, 'This  is for Train Masters only, You are a General User')
              else:
                 messages.info(request, 'Username or Password is incorrect')
            

    context= {}
    return render(request, 'login.html', context)

def log_out(request):
    """
    This method is used to logout the user and redirect them to the login page.
    :param request: it's a HttpResponse from user.
    :type request: HttpResponse.
    :return: this method returns a search page which is a HTML page.
    :rtype: HttpResponse.
    """
    logout(request)
    return redirect('log')

class GeneralUserSignUpView(CreateView):
    model = User
    form_class = GeneralUserSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'guser'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class TrainMasterSignUpView(CreateView):
    model = User
    form_class = TrainMasterSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'trainmaster'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('home')


@login_required(login_url='log')
def search(request):
    context = {}
    if request.method == 'POST':
            p = request.POST.get('source')
            source_r= p.capitalize()
            
            q = request.POST.get('destination')
            dest_r = q.capitalize()
            date_r = request.POST.get('date')
            route_list = Route.objects.filter(source=source_r, dest=dest_r, date=date_r)

            if route_list:
                return render(request, 'list.html', locals())
            else:
                context["error"] = "Sorry no routes availiable"
                return render(request, 'search.html', context)
    else:
            return render(request, 'search.html')


def createOrder(request):
    context = {}
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            id_r = form.cleaned_data['routeid']         
            seats_r = form.cleaned_data['nos']
            p = Route.objects.get(routeId=id_r)
            if p:
                if p.rem > int(seats_r):
                  username_r = request.user.username
                  email_r = request.user.email
                  source_r = p.source
                  dest_r = p.dest
                  date_r = p.date
                  time_r = p.time
                  cost = int(seats_r) * p.price
                  rem_r = p.rem - seats_r
                  Route.objects.filter(routeId=id_r).update(rem=rem_r)
                  p.rem=rem_r
                  book = Book(username=username_r,email=email_r,source=source_r,
                             dest=dest_r,date=date_r,time=time_r,
                             routeid=id_r,nos=seats_r,price=cost, status='Booked')
                  book.save()
                  return redirect('seebookings')
                else:
                  context["error"] = "Sorry select fewer number of seats"
                  return render(request, 'error.html', context)
           
    context = {'form':form}
    return render(request, 'order_form.html', context)


def cancellings(request):
    context = {}
    
    if request.method == 'POST':
      
            id_r = request.POST.get('route_id')
            try:
                book = Book.objects.get(id=id_r)
                route = Route.objects.get(routeId=book.routeid)
                rem_r = route.rem + book.nos
                route.rem=rem_r
                Route.objects.filter(routeId=book.routeid).update(rem=rem_r)
                #nos_r = book.nos - seats_r
                Book.objects.filter(id=id_r).update(status='Cancelled')
                
                Book.objects.filter(id=id_r).update(nos=0)
                Book.objects.filter(id=id_r).update(price=0)
                
               
                

              
                
                return redirect('seebookings')
            except Book.DoesNotExist:
                context["error"] = "No bookings available"
                return render(request, 'error.html', context)
    else:
        return render(request, 'search.html')

def seebookings(request,new={}):
    context = {}
    username_r = request.user.username
    book_list = Book.objects.filter(username=username_r)
    if book_list:
        return render(request, 'booklist.html', locals())
    else:
        context["error"] = "Sorry no route booked"
        return render(request, 'search.html', context)
















