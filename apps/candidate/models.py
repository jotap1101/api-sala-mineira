from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.generate_hashed_filename import upload_to
from uuid import uuid4
import os

# Create your models here.
class Gender(models.Model):
    class Meta:
        db_table = 'candidate_gender'
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name
    
class DriversLicenseCategory(models.Model):
    class Meta:
        db_table = 'candidate_drivers_license_category'
        verbose_name = 'Categoria de CNH'
        verbose_name_plural = 'Categorias de CNH'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name
    
class Candidate(models.Model):
    class Meta:
        db_table = 'candidate_candidate'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

    def profile_picture_upload_to(instance, filename):
        return upload_to(instance, filename, 'candidates/profile_pictures')
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))
    date_of_birth = models.DateField(verbose_name=_('Date of birth'))
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, verbose_name=_('Gender'))
    cpf = models.CharField(max_length=11, unique=True, verbose_name=_('CPF'))
    rg = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name=_('RG'))
    has_disability = models.BooleanField(default=False, verbose_name=_('Has disability'))
    disability_description = models.TextField(null=True, blank=True, verbose_name=_('Disability description'))
    has_drivers_license = models.BooleanField(default=False, verbose_name=_('Has driver\'s license'))
    drivers_license_category = models.ForeignKey(DriversLicenseCategory, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('Driver\'s license category'))
    is_first_job = models.BooleanField(default=False, verbose_name=_('Is first job'))
    is_currently_employed = models.BooleanField(default=False, verbose_name=_('Is currently employed'))
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, null=True, blank=True, verbose_name=_('Profile picture'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()
    
    def get_age(self):
        return date.today().year - self.date_of_birth.year - ((date.today().month, date.today().day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def get_formatted_date_of_birth(self):
        return self.date_of_birth.strftime('%d/%m/%Y')
    
    def get_formatted_cpf(self):
        return f'{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}'
    
    def get_formatted_rg(self):
        if len(self.rg) == 10:
            return f'{self.rg[:2]}-{self.rg[2:4]}.{self.rg[4:7]}.{self.rg[7:]}'
        elif len(self.rg) == 11:
            return f'{self.rg[:2]}-{self.rg[2:4]}.{self.rg[4:7]}.{self.rg[7:10]}-{self.rg[10:]}'
        
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Candidate.objects.get(pk=self.pk)
                if old_instance.profile_picture and old_instance.profile_picture != self.profile_picture:
                    if os.path.isfile(old_instance.profile_picture.path):
                        os.remove(old_instance.profile_picture.path)
            except Candidate.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()
    
class Contact(models.Model):
    class Meta:
        db_table = 'candidate_contact'
        verbose_name = 'Informação de contato'
        verbose_name_plural = 'Informações de contato'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='contact', verbose_name=_('Candidate'))
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'))
    email = models.EmailField(null=True, blank=True, verbose_name=_('E-mail'))

    def get_formatted_phone_number(self):
        return f'{self.phone_number[:3]} ({self.phone_number[3:5]}) {self.phone_number[5:10]}-{self.phone_number[10:]}'
    
    def save(self, *args, **kwargs):
        self.phone_number = f'+55{self.phone_number}' if not self.phone_number.startswith('+55') else self.phone_number
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.candidate.get_full_name()
    
class State(models.Model):
    class Meta:
        db_table = 'candidate_state'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    abbreviation = models.CharField(max_length=2, unique=True, verbose_name=_('Abbreviation'))

    def __str__(self):
        return self.name
    
class City(models.Model):
    class Meta:
        db_table = 'candidate_city'
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name=_('State'))

    def __str__(self):
        return self.name
    
class Address(models.Model):
    class Meta:
        db_table = 'candidate_address'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='address', verbose_name=_('Candidate'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))
    number = models.CharField(max_length=10, verbose_name=_('Number'))
    complement = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Complement'))
    neighborhood = models.CharField(max_length=255, verbose_name=_('Neighborhood'))
    zip_code = models.CharField(max_length=8, verbose_name=_('ZIP code'))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('City'))

    def get_formatted_zip_code(self):
        return f'{self.zip_code[:5]}-{self.zip_code[5:]}'
    
    def get_address(self):
        return f'{self.street}, {self.number} - {self.neighborhood} - {self.city.name}/{self.city.state.abbreviation}'
    
    def __str__(self):
        return self.candidate.get_full_name()
    
class SocialNetwork(models.Model):
    class Meta:
        db_table = 'candidate_social_network'
        verbose_name = 'Nome da rede social'
        verbose_name_plural = 'Nomes das redes sociais'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name
    
class SocialNetworkProfile(models.Model):
    class Meta:
        db_table = 'candidate_social_network_profile'
        verbose_name = 'Perfil de rede social'
        verbose_name_plural = 'Perfis de redes sociais'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='social_network_profile', null=True, blank=True, verbose_name=_('Candidate'))
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.PROTECT, verbose_name=_('Social network'))
    username = models.CharField(max_length=255, verbose_name=_('Username'))
    url = models.URLField(unique=True, verbose_name=_('URL'))

    def save(self, *args, **kwargs):
        match self.social_network.name.lower():
            case 'linkedin':
                self.url = f'https://www.linkedin.com/in/{self.username}/'
            case 'github':
                self.url = f'https://www.github.com/{self.username}/'
            case 'facebook':
                self.url = f'https://www.facebook.com/{self.username}/'
            case 'instagram':
                self.url = f'https://www.instagram.com/{self.username}/'
            case 'x (twitter)':
                self.url = f'https://x.com/{self.username}/'
            case _:
                self.url = f'https://www.{self.social_network_name.name.lower()}.com/{self.username}/'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.candidate.get_full_name()