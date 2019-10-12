from django.contrib import admin

from .models import Account

from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','organism','status','date_joined','last_login','is_admin','is_staff')

    search_fields = ("email",'first_name','last_name',)
    readonly_fields = ('date_joined','last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','last_name','organism','status'),
        }),
    )

admin.site.register(Account,AccountAdmin)
