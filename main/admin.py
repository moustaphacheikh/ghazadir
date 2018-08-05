from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from main.forms import UserSignUpForm, UserUpdateForm
from main.models import InboundMessage,OutboundMessage,Transaction

class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    add_form = UserSignUpForm
    form = UserUpdateForm

    #list_display = ['email', 'username']
from main.models import Transaction

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('id', 'from_agent__first_name', 'to_agent__first_name', 'fee','beneficiary_number')
        # export_order = ('id', 'price', 'author', 'name')
from import_export.admin import ImportExportModelAdmin

class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(InboundMessage)
admin.site.register(OutboundMessage)
