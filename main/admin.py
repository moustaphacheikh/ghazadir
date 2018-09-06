from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from main.forms import UserSignUpForm, UserUpdateForm
from main.models import InboundMessage,OutboundMessage,Transaction
from import_export.admin import ImportExportModelAdmin
class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    add_form = UserSignUpForm
    form = UserUpdateForm

    #list_display = ['email', 'username']
from main.models import Transaction

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('from_agent__username', 'to_agent__username','money', 'fee','beneficiary_number','created_at')
    def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((x.verbose_name for x in model_fields if x.name == field.column_name), field.column_name)
            headers.append(header)
            for i in range(len(headers)):
                if headers[i]=="from_agent__username":
                    headers[i]="الوكيل المرسل"
            for i in range(len(headers)):
                if headers[i]=="to_agent__username":
                    headers[i]= "الوكيل المستلم"

        return headers
        # export_order = ('id', 'price', 'author', 'name')
from import_export.admin import ExportMixin,ExportActionModelAdmin
from import_export.formats import base_formats

class TransactionAdmin(ExportActionModelAdmin):
    resource_class = TransactionResource
    date_hierarchy = 'created_at'
    verbose_name = True
    list_display = (
        'from_agent',
        'money',
        'fee',
        'beneficiary_number',
   )

    def get_export_formats(self):

            formats = (
                  base_formats.XLSX,
            )
            return [f for f in formats if f().can_export()]

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib.auth.models import Group


admin.site.unregister(Group)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(get_user_model())
