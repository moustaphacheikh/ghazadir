from django.shortcuts import render
from main.forms import UserSignUpForm,TransactionForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView,DetailView,ListView
from django.views import generic
from django.views.generic.edit import UpdateView
from main.models import *
from ghaza import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import json
# Create your views here.
import string
from random import *

##################### TESTED #########################

class HomePageView(TemplateView):
    template_name = 'home.html'

class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    success_url = reverse_lazy('home')
    template_name_suffix = '_detail'

class UserListView(LoginRequiredMixin,ListView):
    model = User
    template_name_suffix = '_list'
    context_object_name = 'user_list'  # Default: object_list
    paginate_by = 5


    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['some_data'] = 'This is just some data'
        return context
from datetime import date, timedelta

class DashboardView(LoginRequiredMixin,ListView):
    model = User

    template_name = 'main/dashboard.html'
    context_object_name = 'users'  # Default: object_list

    def get_queryset(self):

        return User.objects.filter(is_admin=False)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        yesterday = date.today() - timedelta(1)
        # Create any data and add it to the context
        context['count'] = Transaction.objects.count()
        context['yesterday']  =yesterday
        context['some_data'] = 'This is just some data'
        return context



class TransactionListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name_suffix = '_list'
    context_object_name = 'transaction_list'  # Default: object_list
    paginate_by = 10


    def get_queryset(self):
        yesterday = date.today() - timedelta(1)
        return Transaction.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['range'] = range(context['paginator'].num_pages)

        # context['some_data'] = 'This is just some data'
        return context
class Transactions(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'main/transactions.html'
    context_object_name = 'transactions'  # Default: object_list
    paginate_by = 10


    def get_queryset(self):
        yesterday = date.today() - timedelta(1)
        return []

    def get_context_data(self, **kwargs):
        context = super(Transactions, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['range'] = range(context['paginator'].num_pages)
        transactions = Transaction.objects.filter(Q(to_agent=self.request.user) | Q(from_agent=self.request.user))
        context['transactions'] = transactions
        return context

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    # fields = ['username','first_name','last_name','email']
    fields = ['phone_number','first_name', 'last_name','username','email','city',
                'location','is_admin']
    success_url = reverse_lazy('home')
    template_name_suffix = '_update_form'


class SignUp(generic.CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('user-list')
    template_name = 'signup.html'

class UserListView(LoginRequiredMixin,ListView):
    model = User
    template_name_suffix = '_list'

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['some_data'] = 'This is just some data'
        return context

def html_404(request):
    # debug must be set to False
    html = '404.html'
    return HttpResponse(html)

@csrf_exempt
def sms_response(request):
    # Start our TwiML response
    TEST = True
    resp = MessagingResponse()
    if request.method!='POST':
        return HttpResponse(str(resp))
    if req_is_valid(request) and request.method=='POST':
        req_clean = in_req_clean(request)
        if TEST:
            to_ag_out = OutboundMessage.objects.all().first()
            in_msg = InboundMessage.objects.all().first()
            to_cl_out = OutboundMessage.objects.all().first()
            trans = cs_trans(req_clean,in_msg,to_cl_out,to_ag_out)
        else:
            in_msg = cv_in(req_clean)
            to_cl_out = scv_cl_out(req_clean)
            to_ag_out = scv_ag_out(req_clean)
            trans = cs_trans(req_clean,in_msg,to_cl_out,to_ag_out)
        return HttpResponse(str(resp))
    else:
        return HttpResponse(str(resp))

@login_required
def new_transtaction(request):
    TEST =True
    # Retrieve post by id
    if request.method == 'POST':
    # Form was submitted
        form = TransactionForm(request.POST)
        if form.is_valid():
            if TEST:
                pass
            else:
                form_clean = form_processing(form,request.user)
                to_cl_out = scv_cl_out(form_clean)
                to_ag_out = scv_ag_out(form_clean)
                trans = cs_trans_form(form_clean,to_cl_out,to_ag_out)
            return HttpResponseRedirect(reverse_lazy('transtaction-list'))
            #Create a new transaction with default status to delivered
    else:
        form = TransactionForm(initial={'from_agent_number':request.user.phone_number})
        return render(request, 'main/new_transtaction.html', {'form': form})
####################### END ###########################


#********************************************************#
#********************************************************#
#********************************************************#


##################### NEED TESTE #########################

from datetime import tzinfo, timedelta, datetime,timezone
import random


class DataGenerator:

    def __init__(self):
        self.start = datetime(2018, 1, 1, tzinfo=timezone.utc)
        self.end  = datetime.now(tz=timezone.utc)

    def get_datetime(self,start,end):
        return fake.date_time_ad(tzinfo=timezone.utc, end_datetime=end, start_datetime=start)

    def get_in_msg(self,cl_num,money,fee,to_ag_num):
        return f'{cl_num}*{money}*{fee}*{to_ag_num}'

    def gen_in_msg(self):
        cl_num = "6127598"
        money = 35000
        fee = "500"
        to_ag_num ='93607148'
        return self.get_in_msg(cl_num,money,fee,to_ag_num)

    def gen_random_location(self):
        num = random.choice(['B','F','C','A'])+ str(self.random_with_N_digits(2))
        return f'{num} الحانوت رقم'

    def random_with_N_digits(self,n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)

    def get_names_cities_fname(self,fnames,fcitites):


        cities = []
        names = []
        with open(f'{fcitites}.txt','r',encoding='utf8') as file:
            for line in file.readlines():
                cities.append(line.replace('\n',''))

        with open(f'{fnames}.txt','r',encoding='utf8') as file:
            for line in file.readlines():
                names.append([line.replace('\n','').split('ولد')[0] , line.replace('\n','').split('ولد')[1]])
        return names,cities
    def gen_sid(self):
        allchar = string.ascii_letters + string.punctuation + string.digits
        return "".join(random.choice(allchar) for x in range(random.randint(34, 34)))

def client_search(request):
    num = request.GET.get("phone_number")
    if num is None or num == "":
        return render(request, 'main/client_detail.html', {'transactions': None})
    else:
        transactions = Transaction.objects.filter(beneficiary_number=num)
        if transactions:
            return render(request, 'main/client_detail.html', {'transactions': transactions})
        else:
            return render(request, 'main/client_detail.html', {'transactions': None})
from django.db.models import Q

def agent_search(request):
    num = request.GET.get("phone_number")


    if num is None or num == "":
        return render(request, 'main/agent_detail.html', {'transactions': None})
    else:
        if request.user.is_admin:
            transactions = Transaction.objects.filter(Q(from_agent__phone_number=num) | Q(to_agent__phone_number=num))
        else:
            transactions = Transaction.objects.filter(Q(from_agent__phone_number=num) | Q(to_agent__phone_number=num) & Q(to_agent__phone_number=request.user.phone_number) & Q(from_agent__phone_number=request.user.phone_number))
        if transactions:
            return render(request, 'main/agent_detail.html', {'transactions': transactions})
        else:
            return render(request, 'main/agent_detail.html', {'transactions': None})

from main import enums
def gen_user(gen,n):

    users ,cities = gen.get_names_cities_fname('main/names','main/cities')
    user_dicts = []
    for i in range(n):
        user = random.choice(users)
        while user[0].startswith('الله') or user[1].startswith('الله') :
            user = random.choice(users)
        first_name = user[0]
        last_name = user[1]
        email = "test@test.com"
        is_admin = False
        phone_number = gen.random_with_N_digits(8)
        username = phone_number
        city = random.choice([c[1] for c in enums.CITY_CHOICES])
        location = gen.gen_random_location()

        password = 'test123456test'
        user_dict = {'first_name':first_name,'last_name':last_name,'email':email,'is_admin':is_admin,
                    'password':password,
                     'username':username,'phone_number':phone_number,'city':city,'location':location}
        user_dicts.append(user_dict)

    return user_dicts

def gen_users(n):
    gen = DataGenerator()
    User.objects.filter(is_superuser=False).delete()
    user_dicts = gen_user(gen,n)
    for user_dict in user_dicts:
        user = User.objects.create_user(username=user_dict['username'],
                            first_name=user_dict['first_name'],
                            last_name=user_dict['last_name'],
                            location=user_dict['location'],
                            phone_number=user_dict['phone_number'],
                            email=user_dict['email'],
                            city= user_dict['city'],
                            password=user_dict['password'],)
# 15511310

def gen_transactions(n):
    gen = DataGenerator()
    users = User.objects.filter(is_superuser=False)
    numbers = [user.phone_number for user in users]
    for i in range(n):
        in_sid = gen.gen_sid()
        cl_num = gen.random_with_N_digits(8)
        money = random.randint(500,15000)
        fee = int(money*random.uniform(0.01,0.07))
        from_ag_num = random.choice(numbers)
        body = f'{cl_num}*{money}*{fee}*{random.choice(numbers)}'
        body_ = body.split('*')
        to_ag_num = body_[3]
        created_at = randomDate("01-01-2015 00:00", "03-08-2018 00:50")
        from_ag =  User.objects.filter(phone_number=from_ag_num).first()
        to_ag =  User.objects.filter(phone_number=to_ag_num).first()
        cl_msg = f'يمكنكم من الأن سحب مبلغ {money} عن طريل مكتب غزة {to_ag_num}'
        to_ag_msg =f'صاحب الرقم {cl_num} يملك {money} مودعة عن طريق {from_ag_num}'

        price ='-0.075'

        req_clean = {'from_ag_num':from_ag_num,'money':money,'fee':fee,'created_at':created_at,
        'cl_num':cl_num,'in_sid':in_sid,'to_ag':to_ag,'from_ag':from_ag,
        'body':body,'price':price,'to_ag_num':to_ag_num,'cl_msg':cl_msg,
        'to_ag_msg':to_ag_msg,'to':'+18135364577'}
        #cv_in(req_clean)
        in_msg = cv_in(req_clean)
        date = created_at  =randomDate("01-01-2016 00:00", "03-08-2018 00:50")

        to_cl_out = OutboundMessage.objects.create(sid=gen.gen_sid(),
                                        sender=req_clean['to'],
                                        recipient=req_clean['cl_num'],
                                        body=req_clean['body'],
                                        price=req_clean['price'],
                                        status='delivered',
                                        created_at  =date,
                                        is_outbound=True)
        to_ag_out = OutboundMessage.objects.create(sid=gen.gen_sid(),
                                        sender=req_clean['to'],
                                        recipient=req_clean['to_ag_num'],
                                        body=req_clean['body'],
                                        price=req_clean['price'],
                                        status='delivered',
                                        created_at  =date,
                                        is_outbound=True)

        trans = cs_trans(req_clean,in_msg,to_cl_out,to_ag_out)
        trans.created_at = created_at  =date
        trans.save()

@login_required
def generate_new_dataset(request):
    # gen_users(200)
    # gen_transactions(1000)
    # return HttpResponseRedirect(reverse_lazy('transtaction-list'))
    return render(request, 'home.html', {'data': 'data'})


######################## END ###############################
