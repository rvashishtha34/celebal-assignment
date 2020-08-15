from django.contrib import admin
from .models import Account, Transaction
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class TransactionResource(resources.ModelResource):

    class Meta:
        model = Transaction


class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource


admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)
