from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import User,Transaction
from django.core.validators import RegexValidator

class UserSignUpForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="يجب أن تحتوي أرقام الهاتف على 8 أرقام.")
    username = forms.CharField(validators=[phone_regex], max_length=8,help_text=False,label="المستخدم")
    phone_number = forms.CharField(validators=[phone_regex], max_length=8,label='رقم الهاتف')
    location = forms.CharField(max_length=255,required=True,label='عنوانك')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name', 'last_name','email',
                    'phone_number' ,'location']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email',
                    'phone_number' ,'location']


class TransactionForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="يجب أن تحتوي أرقام الهاتف على 8 أرقام.")
    from_agent_number = forms.CharField(validators=[phone_regex], max_length=8,label='رقم الوكيل الموسل')
    to_agent_number = forms.CharField(validators=[phone_regex], max_length=8,required=True,label='رقم الوكيل المستلم')
    money = forms.CharField(max_length=255,required=True,label='المبلغ')
    fee = forms.CharField(max_length=255,required=True,label='الرسوم')
    beneficiary_number = forms.CharField(validators=[phone_regex],max_length=8,required=True,label='رقم العميل المستلم')

    def clean(self):
        # form level cleaning
        cleaned_data = super(TransactionForm, self).clean()

        from_agent_phone = cleaned_data.get("from_agent_number")
        to_agent_phone = cleaned_data.get("to_agent_number")

        from_agent =  User.objects.filter(phone_number=from_agent_phone).first()
        to_agent =  User.objects.filter(phone_number=to_agent_phone).first()

        if not from_agent and not to_agent:
            raise forms.ValidationError("عذرًا ، يجب أن يكون كل من الوكيل المرسل والوكيل المتلقي موجودًا ضمن الوكلاء المسجلين.")
        if not from_agent:
            raise forms.ValidationError("عذرًا ، يجب أن يكون رقم الوكيل المرسل موجودًا ضمن الوكلاء المسجلين.",)
        if not to_agent:
            raise forms.ValidationError("عذرًا ، يجب أن يكون رقم الوكيل المستلم ضمن الوكلاء المسجلين.",)
