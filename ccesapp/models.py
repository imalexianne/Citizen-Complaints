from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import random
import uuid

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))  # 10-digit number

# Province Model
class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# District Model (Belongs to a Province)
class District(models.Model):
    name = models.CharField(max_length=100, unique=True )
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return f"{self.name} ({self.province.name})"

# Sector Model (Belongs to a District)
class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="sectors")

    def __str__(self):
        return f"{self.name} ({self.district.name})"

# Cell Model (Belongs to a Sector)
class Cell(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="cells")

    def __str__(self):
        return f"{self.name} ({self.sector.name})"

# Village Model (Belongs to a Cell)
class Village(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name="villages")

    def __str__(self):
        return f"{self.name} ({self.cell.name})"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent', null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    agent_reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.agent_reference

def citizen_image_upload_path(instance, filename):
    """Defines the path where citizen images will be stored."""
    return f'citizen_images/{instance.nid}/{filename}'

class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='citizen')
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    nid = models.CharField(max_length=16, unique=True)
    account_number = models.CharField(max_length=20, unique=True, default=generate_account_number, editable=False)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")], null=True)
    dob = models.CharField(null=True, blank=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True) 
    name = models.CharField(max_length=50, null=True)
    agent_reference = models.ForeignKey(Agent, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    cell = models.ForeignKey(Cell, on_delete=models.SET_NULL, null=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to=citizen_image_upload_path, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)  # store hashed password
    blacklisted = models.BooleanField(default=False, null=True, blank=True,)

    def __str__(self):
        
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_account_number()
            
       
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
            
        super().save(*args, **kwargs)

class PublicService(models.Model):
    serviceType = models.CharField(max_length=100, blank=True, default="Mituelle")
    definition = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.serviceType

class Complaint(models.Model):
    citizen = models.ForeignKey('Citizen', on_delete=models.CASCADE, related_name='complaints')
    publicService = models.ForeignKey(PublicService, on_delete=models.SET_NULL, null=True, related_name='complaints')
    status = models.CharField(max_length=30, default="pending")
    complaintNature = models.CharField(max_length=30)
    complaint_id = models.CharField(max_length=50, unique=True)
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.complaint_id

class Feedback(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.SET_NULL, null=True, related_name='feedbacks')
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.complaint.complaint_id) if self.complaint else "No Complaint"



class AgencyFeedback(models.Model):
    publicservice = models.ForeignKey(PublicService, on_delete=models.SET_NULL, null=True, related_name='agencyfeedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agency_feedbacks', null=True)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.publicservice}" if self.publicservice else "No Feedback"



class ServiceDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='serviceadmin')
    publicservice = models.ForeignKey(PublicService, on_delete=models.SET_NULL, null=True, related_name='serviceadmin')
    name = models.CharField(max_length=100, blank=True, null=True)
    nid = models.CharField(max_length=16, unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.name


