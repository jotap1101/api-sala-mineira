from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(DriversLicenseCategory)
class DriversLicenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    class ContactInline(admin.StackedInline):
        model = Contact
        extra = 0

    class AddressInline(admin.StackedInline):
        model = Address
        extra = 0

    class SocialNetworkProfileInline(admin.StackedInline):
        model = SocialNetworkProfile
        exclude = ['url']
        extra = 0

    inlines = [ContactInline, AddressInline, SocialNetworkProfileInline]
    list_display = ['id', 'first_name', 'last_name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'email']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    class CityInline(admin.StackedInline):
        model = City
        extra = 0

    inlines = [CityInline]
    list_display = ['id', 'name', 'abbreviation']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'street', 'number', 'complement', 'neighborhood', 'zip_code', 'city']

@admin.register(SocialNetworkProfile)
class SocialNetworkProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'social_network', 'url']

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
