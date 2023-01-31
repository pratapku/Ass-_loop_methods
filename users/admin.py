from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import MyUser,Category,Product,Sub_category,contect_us,Post,comment
from import_export.admin import ImportExportModelAdmin
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
     pass
admin.site.register(Category,BlogAdmin)
admin.site.register(Product,BlogAdmin)
admin.site.register(Sub_category,BlogAdmin)
admin.site.register(contect_us,BlogAdmin)
admin.site.register(Post,BlogAdmin)
admin.site.register(comment,BlogAdmin)




class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('name','roll','M_number','email', 'date_of_birth' )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('name','roll','M_number', 'email', 'password', 'date_of_birth','is_active', 'is_admin', )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_of_birth', 'is_admin', )
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        
      
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','roll','M_number','email', 'date_of_birth','password1', 'password2', ),
           
            
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)