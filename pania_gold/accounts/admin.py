from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User,HomeImage,CompanySeller
from django.utils.safestring import mark_safe



class UserAdmin(BaseUserAdmin):
    list_display = ('l_name','f_name', 'mellicod', 'user_groups', 'is_superuser_status','is_admin_status', 'is_active_status')
    list_filter = ('is_active', 'groups')  # فیلتر کردن بر اساس فعال بودن
    fieldsets = (
        ('User Info', {'fields': ('mellicod', 'password')}),
        ('Personal Info', {'fields': ('f_name', 'l_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'permission', 'groups')}),
    )

    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()]) if obj.groups.exists() else "بدون گروه"
    user_groups.short_description = "گروه‌ها"
    def is_admin_status(self, obj):
        return mark_safe('<span style="color: green;">✔</span>') if obj.is_admin else mark_safe(
            '<span style="color: red;">✘</span>')
    is_admin_status.short_description = "ادمین"
    def is_superuser_status(self, obj):
        return mark_safe('<span style="color: green;">✔</span>') if obj.is_superuser else mark_safe(
            '<span style="color: red;">✘</span>')
    is_superuser_status.short_description = "ابرکاربر"
    def is_active_status(self, obj):
        return mark_safe('<span style="color: green;">✔</span>') if obj.is_active else mark_safe(
            '<span style="color: red;">✘</span>')
    is_active_status.short_description = "فعال"

    # فیلدهایی که در صفحه افزودن کاربر جدید نمایش داده می‌شوند
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mellicod', 'f_name', 'l_name', 'phone', 'password1', 'password2', 'groups'),
        }),
    )
    search_fields = ('f_name', 'l_name',)  # امکان جستجو بر اساس کد ملی
    ordering = ('mellicod',)  # مرتب‌سازی بر اساس کد ملی
    filter_horizontal = ('permission',)  # نمایش مجوزها به صورت افقی در پنل مدیریت



# ======================= مدیریت تصاویر صفحه اصلی ==========================
@admin.register(HomeImage)
class HomeImageAdmin(admin.ModelAdmin):
    list_display = ('id','description', 'image')

# # ======================= مدیریت فروشندگان ==========================
@admin.register(CompanySeller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name','vitrin_name' ,'mellicode')
    search_fields = ('name',)



admin.site.register(User, UserAdmin)



