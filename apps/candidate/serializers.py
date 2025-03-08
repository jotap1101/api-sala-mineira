from collections import OrderedDict
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import *

# Gender Serializer
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['url', 'id', 'name']
        read_only_fields = ['id', 'url']

# Drivers License Category Serializer
class DriversLicenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DriversLicenseCategory
        fields = ['url', 'id', 'name']
        read_only_fields = ['id', 'url']

# Candidate Serializer
class CandidateSerializer(serializers.ModelSerializer):
    # Contact Serializer
    class ContactSerializer(serializers.ModelSerializer):
        class Meta:
            model = Contact
            fields = ['phone_number', 'email']

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['phone_number'] = instance.get_formatted_phone_number()

            return representation

    # Address Serializer
    class AddressSerializer(serializers.ModelSerializer):
        state = serializers.SerializerMethodField(method_name='get_state')

        class Meta:
            model = Address
            fields = ['street', 'number', 'complement', 'neighborhood', 'zip_code', 'city', 'state']
            read_only_fields = ['state']
        
        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['zip_code'] = instance.get_formatted_zip_code()

            return representation
        
        def get_state(self, instance) -> str:
            return instance.city.state.abbreviation
        
    # Social Network Profile Serializer
    class SocialNetworkProfileSerializer(serializers.ModelSerializer):
        url_social_network = serializers.SerializerMethodField(method_name='get_url_social_network')
        
        class Meta:
            model = SocialNetworkProfile
            fields = ['social_network', 'username', 'url_social_network']
            extra_kwargs = {
                'username': {'write_only': True}
            }

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['social_network'] = instance.social_network.name

            return representation

        def get_url_social_network(self, instance) -> str:
            return instance.url

    contact = ContactSerializer(many=True, required=False)
    address = AddressSerializer(many=True, required=False)
    social_network_profile = SocialNetworkProfileSerializer(many=True, required=False)

    class Meta:
        model = Candidate
        fields = ['url', 'id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'cpf', 'rg', 'has_disability', 'disability_description', 'has_drivers_license', 'drivers_license_category', 'is_first_job', 'is_currently_employed', 'profile_picture', 'contact', 'address', 'social_network_profile', 'created_at', 'updated_at']
        read_only_fields = ['id', 'url', 'created_at', 'updated_at']
        extra_kwargs = {
            'profile_picture': {'required': False, 'allow_null': True},
        }

    def get_gender(self, instance) -> str:
        return instance.gender.name if instance.gender else None

    def get_formatted_cpf(self, instance) -> str:
        return instance.get_formatted_cpf()
    
    def get_formatted_rg(self, instance) -> str:
        return instance.get_formatted_rg() if instance.rg else None
    
    def get_drivers_license_category(self, instance) -> str:
        return instance.drivers_license_category.name if instance.drivers_license_category else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['gender'] = instance.gender.name
        representation['cpf'] = instance.get_formatted_cpf()
        representation['rg'] = instance.get_formatted_rg()
        representation['drivers_license_category'] = instance.drivers_license_category.name

        ordered_representation = OrderedDict()

        for key, value in representation.items():
            ordered_representation[key] = value

            if key == 'last_name' and instance.get_full_name():
                ordered_representation['full_name'] = instance.get_full_name()

            if key == 'date_of_birth':
                ordered_representation['age'] = instance.get_age()

        return ordered_representation
                
    
    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')
        social_network_profile_data = validated_data.pop('social_network_profile')

        with transaction.atomic():
            candidate = Candidate.objects.create(**validated_data)

            for contact in contact_data:
                Contact.objects.create(candidate=candidate, **contact)

            for address in address_data:
                Address.objects.create(candidate=candidate, **address)

            for social_network_profile in social_network_profile_data:
                SocialNetworkProfile.objects.create(candidate=candidate, **social_network_profile)

        return candidate
    
    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')
        social_network_profile_data = validated_data.pop('social_network_profile')

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()

            instance.contact.all().delete()
            instance.address.all().delete()
            instance.social_network_profile.all().delete()

            for contact in contact_data:
                Contact.objects.create(candidate=instance, **contact)

            for address in address_data:
                Address.objects.create(candidate=instance, **address)

            for social_network_profile in social_network_profile_data:
                SocialNetworkProfile.objects.create(candidate=instance, **social_network_profile)

        return instance
