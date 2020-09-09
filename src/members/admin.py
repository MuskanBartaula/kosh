from django.contrib import admin

from .models import Member, MonthlySaving

class MemberModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Member, MemberModelAdmin)
admin.site.register(MonthlySaving)
