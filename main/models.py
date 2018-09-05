from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse
from django.utils import timezone
from ghaza import settings
from ghaza.settings import C_CODE
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from main import enums
from twilio.rest import Client
# Create your models here.
import random
import time
from datetime import datetime
def randomDate(start, end):

    frmt = '%d-%m-%Y %H:%M'

    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))

    ptime = stime + random.random() * (etime - stime)
    dt = datetime.fromtimestamp(time.mktime(time.localtime(ptime)))
    return dt


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(verbose_name ='صلاحية المدير',default=False)
    location = models.CharField(verbose_name  ='العنوان',max_length = 50)
    username = models.CharField(verbose_name  ='رقم الهاتف',unique=True,max_length=8)
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="يجب أن تحتوي أرقام الهاتف على 8 أرقام.")
    phone_number = models.CharField(verbose_name  ='الهاتف',validators=[phone_regex], max_length=8,unique=True)
    city = models.CharField(verbose_name  ='المدينة',max_length=25, choices=enums.CITY_CHOICES)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.location})'

    @property
    def name(self):
         return f'{self.first_name} {self.last_name} ({self.phone_number})'

    class Meta:
        ordering = ['created_at']
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمين"

class Transaction(models.Model):
    created_at = models.DateTimeField(verbose_name = 'تاريخ الأنشاء',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name  = 'تاريخ التحديث',auto_now=True)
    from_agent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name  ='العميل المرسل',related_name='committed',on_delete=models.CASCADE)
    to_agent = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name  ='العميل المستلم', related_name='received',on_delete=models.CASCADE)
    money = models.CharField(verbose_name  ='المبلغ',max_length=255,blank=True)
    fee = models.CharField(verbose_name  ='الرسوم',max_length=255,blank=True)
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="يجب أن تحتوي أرقام الهاتف على 8 أرقام.")
    beneficiary_number = models.CharField(verbose_name ='رقم المستفيد',validators=[phone_regex], max_length=8)

    is_done = models.BooleanField(verbose_name  ='تم الإيتلام',default=True)
    inbound_sid = models.CharField(max_length=255,default="")
    agent_outbound_sid = models.CharField(max_length=255, unique=True)
    beneficiary_outbound_sid = models.CharField(max_length=255, unique=True)

    def __str__(self):
         return f'from {self.from_agent} to {self.to_agent} for : {self.beneficiary_number}'


    class Meta:
        ordering = ['created_at']
        verbose_name = "تحويلة"
        verbose_name_plural = "التحويلات"

class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sid = models.CharField(max_length=255, unique=True)
    sender = models.CharField(max_length=255,default='')
    recipient = models.CharField(max_length=255,default='')
    body = models.TextField(blank=True,default='')
    price = models.TextField(blank=True,default='')
    is_outbound = models.BooleanField(default=False)
    # class Meta:
    #     abstract = True

class InboundMessage(Message):
    def __str__(self):
         return f'from {self.sender} to {self.recipient} body : {self.body}'

    class Meta:
        ordering = ['created_at']
        verbose_name = "رسالة واردة"
        verbose_name_plural = "الرسائل الواردة"

class OutboundMessage(Message):
    status = models.CharField(max_length=25, choices=enums.MESSAGE_STATUS_CHOICES,default=enums.MESSAGE_STATUS_ACCEPTED)
    def __str__(self):
         return f'from {self.sender} to {self.recipient} body : {self.body}'

    class Meta:
        ordering = ['created_at']
        verbose_name = "رسالة صادرة"
        verbose_name_plural = "الرسائل الصادرة"

def c_in_msg(messageSid,sender,to,body,price):

    inbound = InboundMessage.objects.create(sid=messageSid,
                                    sender=sender,
                                    recipient=settings.TWILIO_SMS_FROM,
                                    body=body,
                                    price=price)

    return inbound

def get_transaction(in_req):

    transaction = Transaction.objects.create(
                                    from_agent=from_agent,
                                    to_agent=to_agent,
                                    money=money,
                                    fee=fee,
                                    beneficiary_number=beneficiary_number,
                                    inbound_sid=inbound_sid,
                                    agent_outbound_sid=agent_outbound_sid,
                                    beneficiary_outbound_sid=beneficiary_outbound_sid)

    return transaction

def dummydata(client):
    message_sid = "SMc9f056d99a83be4e56c58c4b6d10d488"
    message = client.messages(message_sid).fetch()
    return messege

def get_client():
    return Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

def form_processing(form,user):
    data = form.cleaned_data
    from_ag_num = user.phone_number
    to_ag_num = data['to_agent_number']
    money = data['money']
    fee = data['fee']
    cl_num = data['beneficiary_number']

    from_ag =  User.objects.filter(phone_number=from_ag_num).first()
    to_ag =  User.objects.filter(phone_number=to_ag_num).first()

    cl_msg = f'يمكنكم من الأن سحب مبلغ {money} عن طريل مكتب غزة {to_ag}'
    to_ag_msg =f'صاحب الرقم {cl_num} يملك {money} مودعة عن طريق {from_ag}'


    form_clean = {'from_ag_num':from_ag_num,'to_ag_num':to_ag_num,'money':money,'fee':fee,
    'cl_num':cl_num,'in_sid':'','to_ag':to_ag,'from_ag':from_ag,'cl_msg':cl_msg,
    'to_ag_msg':to_ag_msg}

    return form_clean

def create_dummy_db_data():

    User.objects.filter(is_superuser=False).delete()
    for user in users:
        User.objects.create_user(username=user['username'],
                            first_name=user['first_name'],
                            last_name=user['last_name'],
                            location=user['location'],
                            phone_number=user['phone_number'],
                            email=user['email'],
                            password=user['password'],)


def cs_trans_form(req_clean,cl_out,to_ag_out):

    trans= Transaction.objects.create(
                                    from_agent=req_clean['from_ag'],
                                    to_agent=req_clean['to_ag'],
                                    money=req_clean['money'],
                                    fee=req_clean['fee'],
                                    beneficiary_number=req_clean['cl_num'],
                                    inbound_sid='',
                                    agent_outbound_sid=to_ag_out.sid,
                                    beneficiary_outbound_sid=cl_out.sid)
##################### TESTED #########################

def cs_trans(req_clean,in_msg,cl_out,to_ag_out):

    trans= Transaction.objects.create(
                                    from_agent=req_clean['from_ag'],
                                    to_agent=req_clean['to_ag'],
                                    money=req_clean['money'],
                                    fee=req_clean['fee'],
                                    beneficiary_number=req_clean['cl_num'],
                                    inbound_sid=in_msg.sid,
                                    agent_outbound_sid=to_ag_out.sid,
                                    beneficiary_outbound_sid=cl_out.sid)

    return trans

def req_is_valid(request):
    body = request.POST.get('Body')
    body_ = body.split('*')
    from_ag_num = request.POST.get('From')[-8:]
    to_ag_num = body_[3]
    from_ag =  User.objects.filter(phone_number=from_ag_num).first()
    to_ag =  User.objects.filter(phone_number=to_ag_num).first()
    if from_ag is None or to_ag is None or len(body.split("*"))!=4:
        return False
    else:
        return True

def sent(num,body,is_client):
    client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    if(is_client):
        msg = client.api.account.messages.create(to = num,from_='GazaTelecom',body= body)
    else:
        msg = client.api.account.messages.create(to = num,from_= settings.TWILIO_NUM,body= body)
    return msg

def in_req_clean(request):
    from_ = request.POST.get('From')
    in_sid = request.POST.get('MessageSid')
    to = request.POST.get('To')
    body = request.POST.get('Body')
    price = request.POST.get('Price')

    body_ = body.split("*")
    from_ag_num = from_[-8:]
    cl_num, money,fee ,to_ag_num = body_[0],body_[1],body_[2],body_[3]
    from_ag =  User.objects.filter(phone_number=from_ag_num).first()
    to_ag =  User.objects.filter(phone_number=to_ag_num).first()

    cl_msg = f'يمكنكم من الأن سحب مبلغ {money} عن طريل مكتب غزة {to_ag}'
    to_ag_msg =f'صاحب الرقم {cl_num} يملك {money} مودعة عن طريق {from_ag}'

    req_clean = {'from_ag_num':from_ag_num,'money':money,'fee':fee,
    'cl_num':cl_num,'in_sid':in_sid,'to_ag':to_ag,'from_ag':from_ag,
    'body':body,'price':price,'to_ag_num':to_ag_num,'cl_msg':cl_msg,
    'to_ag_msg':to_ag_msg,'to':to}

    return req_clean

def cv_in(in_req):
    in_sms = InboundMessage.objects.create(sid = in_req['in_sid'],
                                            sender = in_req['from_ag_num'],
                                            recipient = in_req['to'],
                                            body = in_req['body'],
                                            price = str(in_req['price']),
                                            is_outbound = False)

    return in_sms

def scv_cl_out(in_req):
    cl_num = in_req['cl_num']
    cl_num = f'{C_CODE}{cl_num}'
    msg = sent(cl_num,in_req['cl_msg'],True)
    cl_out = cv_out(msg)
    return cl_out

def scv_ag_out(in_req):
    to_ag_num = in_req['to_ag_num']
    to_ag_num = f'{C_CODE}{to_ag_num}'
    msg = sent(to_ag_num,in_req['to_ag_msg'],False)
    cl_out = cv_out(msg)
    return cl_out

def cv_out(msg):
    out_sms = OutboundMessage.objects.create(sid=msg.sid,
                                    sender=msg.from_,
                                    recipient=msg.to,
                                    body=msg.body,
                                    price=str(msg.price),
                                    status=msg.status,
                                    is_outbound=True)
    return out_sms
####################### END ###########################


#********************************************************#
#********************************************************#
#********************************************************#


##################### NEED TESTE #########################




######################## END ###############################
