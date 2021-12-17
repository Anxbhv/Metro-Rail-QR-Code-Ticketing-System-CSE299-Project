from django.urls import path
from .views import SignUp,GeneralUserSignUpView,TrainMasterSignUpView
from . import views


urlpatterns = [
  path('signup/',SignUp,name='signup'),
  path('log/', views.log, name="log"),
  path('log2/', views.log2, name="log2"),
  path('accounts/signup/guser/', GeneralUserSignUpView.as_view(), name='guser_signup'),
  path('accounts/signup/trainmaster/', TrainMasterSignUpView.as_view(), name='trainmaster_signup'),
  path('log_out/', views.log_out, name="log_out"),
  path('search/', views.search, name="search"),
  path('create_order/', views.createOrder, name="create_order"),
  path('seebookings/', views.seebookings, name="seebookings"),

  path('cancellings/<str:pk>/', views.cancellings, name="cancellings"),
  path('payments/<str:pk>/', views.payment, name="payments"),
]