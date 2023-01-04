from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistrationForm, LoginForm,UserChangeForm
from django.contrib.auth import get_user_model,authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MyPasswordChangeForm
from .models import Account
from django.core.mail import send_mail
from django.urls import reverse_lazy
import time

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "account/home.html"
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/user.html'
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)
class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'account/changepass.html'
    form_class = UserChangeForm
    success_url = 'account:home'
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs
def sent_pass(request):
    template_name = 'account/sentpass.html'
    usermail = request.user.email
    userid = request.user.uuid
    senttime=time.time()
    message='以下のリンクからパスワードを変更してください。\nhttps://www.sounding.chart.link/account/changepassword/'+str(userid)+'/'+str(senttime)
    #send_mail('SoundingChart パスワード変更',message,'noreply@sounding-chart.link', [usermail], fail_silently=False)
    #return render(request, template_name)   
    
    return redirect('/account/changepass/'+str(userid)+'/'+str(senttime))
def password_change(request,user,senttime):
    count=float(senttime)-time.time()
    if count>300:
         return render(request, 'account/timeover.html')
    else:
        template_name = 'account/changepass.html'
        form = MyPasswordChangeForm(user=Account.objects.filter(uuid=user))
        context = {
            'form': form,
        }
        return render(request, template_name, context)
# パスワードの変更を保存する処理
def password_change_post(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('account:home')
    
class MyLoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
        return redirect('account:home')

class MyLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('account:login')

class MyUserView(TemplateView):
    template_name = 'account/user.html'

class RegistrationView(CreateView):
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('account:home')
