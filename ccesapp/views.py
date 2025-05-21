import os
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ProvinceForm, DistrictForm, SectorForm, CellForm, VillageForm, FeedbackForm, ServiceEditForm, CitizenEditForm,CitizenForm, PublicServiceForm, AgentSignUpForm, CitizenRegistrationForm, CitizenLoginForm, AgencyFeedbackForm
from django.urls import reverse_lazy, reverse
from .models import Province, District, Sector, Cell, Village, PublicService,Complaint, Citizen,Agent, AgencyFeedback
import random
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404,render, redirect
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout, get_user_model
import logging
from django.core.files.storage import default_storage
import requests
from requests.auth import HTTPBasicAuth
import base64
from django.core.files.base import ContentFile

def index(request):
    
    return render(request, 'index.html' )

def signup(request):
    
    return render(request, 'verification.html' )


@login_required
def redirect_after_login(request):
    user = request.user

    # Redirect superuser or staff (admin)
    if user.is_superuser:
    # or user.is_staff:
        return redirect('/admin_dashboard/')  # or use a custom admin dashboard like: redirect('admin_dashboard')

    # Redirect Agent
    elif hasattr(user, 'agent'):
        return redirect('/citizen/registration') 

    # Redirect citizen
    elif hasattr(user, 'citizen'):
        return redirect('/citizen/dashboard')

    else:
    
        logout(request)
        return redirect('/login/')


def logout_view(request):
    
    logout(request)
    return redirect('/login/')

def agent_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                
                agent = user.agent 
                login(request, user)
                return redirect('/citizen/registration')
            except Agent.DoesNotExist:
                messages.error(request, 'You are not authorized as an agent.')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'agent_login.html')



def password(request):
    account_number = request.session.get('new_account_number')
    return render(request, 'password.html', {'account_number': account_number})


def usermanagement(request):
    
    return render(request, 'usermanagement.html' )


def citizenform(request):
    
    return render(request, 'citizenform.html' ) 





User = get_user_model() 


logger = logging.getLogger(__name__)

def save_citizen_from_session(request):
    ccitizen_data = request.session.get('citizen_data')

    if not all(citizen_data):
        messages.error(request, "Incomplete registration data.")
        return redirect('/agent/login')

    raw_password = citizen_data.get('raw_password')
    username = citizen_data.get('username')
    email = itizen_data.get('email')

    if not username or not raw_password:
        messages.error(request, "Missing username or password.")
        return redirect('/agent/login')

    try:
        # ✅ Create Django User with hashed password
        user = User(username=username, email=email)
        user.set_password(raw_password)
        # user.is_staff = True
        user.save()

        # ✅ Add user to 'Citizen' group
        try:
            citizen_group, created = Group.objects.get_or_create(name='Citizen')
            user.groups.add(citizen_group)
            print(f"[DEBUG] User {user.username} added to Citizen group.")
        except Exception as e:
            print(f"[ERROR] Assigning user to Citizen group failed: {e}")

        # ❌ Skipping login/authentication
        print(f"[DEBUG] User created (not logged in): {username}")

    except Exception as e:
        print(f"[ERROR] User creation error: {e}")
        messages.error(request, "Failed to create user.")
        return redirect('/agent/login')

    try:
        citizen = Citizen.objects.create(
            user=user,
            nid=citizen_data['nid'],
            name=citizen_data['name'],
            dob=citizen_data['dob'],
            nationality=citizen_data['nationality'],
            street=citizen_data['street'],
            account_number=citizen_data['account_number'],
            province=Province.objects.get(id=citizen_data['province']),
            district=District.objects.get(id=citizen_data['district']),
            sector=Sector.objects.get(id=citizen_data['sector']),
            cell=Cell.objects.get(id=citizen_data['cell']),
            village=Village.objects.get(id=citizen_data['village']),
            agent_reference=Agent.objects.get(id=citizen_data['agent_reference']),

            username=username,
            email=email,
            phone_number=citizen_data.get('phone_number'),
            password=user.password,  # already hashed
            marital_status=spouse_data.get('has_children') if spouse_data else None,
            
        )

        print(f"[DEBUG] Citizen profile created for {ccitizen.username}")

    except Exception as e:
        print(f"[ERROR] Citizen creation error: {e}")
        messages.error(request, "Failed to create citizen profile.")
        return redirect('/agent/login')

    # ✅ Clear session and render success page
    request.session.flush()
    return render(request, 'registration_success.html', {
        'citizen': citizen,
        'account_number': citizen.account_number,
        'username': username,
        'password': raw_password  # for confirmation only, remove in production
    })


@login_required
def verify_nid(request):
    if request.method == "POST" and "national_id" in request.POST:
        national_id = request.POST.get("national_id")
        
        if not national_id or not national_id.isdigit():
            return JsonResponse({"error": "Please enter a valid National ID."})
        
        # Simulated data
        user_data = {
            "foreName": "John",
            "surName": "Doe",
            "nationality": "Rwandan",
            "gender": "MALE",
            "dateOfBirth": "1990-01-01",
            "maritalStatus": "Single",
            "province": "Kigali City",
            "district": "Gasabo",
            "sector": "Kacyiru",
            "cell": "Kacyiru Cell",
            "village": "Village A",
            "address": "KN 123 St",
            "photo": "" 
        }

        name = f"{user_data['foreName']} {user_data['surName']}".strip()
        request.session["user_data"] = user_data
        request.session["national_id"] = national_id

        photo_data = user_data.get("photo", "")
        formatted_photo = f"data:image/jpeg;base64,{photo_data}" if photo_data else None

        # Parse date of birth
        dob_str = user_data.get("dateOfBirth", "")
        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                dob = None

        # Dropdown data
        provinces = Province.objects.all()
        districts = District.objects.all()
        sectors = Sector.objects.all()
        cells = Cell.objects.all()
        villages = Village.objects.all()

        # Pre-select default location values
        default_province = Province.objects.filter(name=user_data.get("province", "")).first()
        default_district = District.objects.filter(name=user_data.get("district", "")).first() if default_province else None
        default_sector = Sector.objects.filter(name=user_data.get("sector", "")).first() if default_district else None
        default_cell = Cell.objects.filter(name=user_data.get("cell", "")).first() if default_sector else None
        default_village = Village.objects.filter(name=user_data.get("village", "")).first() if default_cell else None

        return render(request, "location_selection.html", {
            "user_data": user_data,
            "name": name,
            "nid": national_id,
            "nationality": user_data.get("nationality", ""),
            "photo": formatted_photo,
            "dob": user_data.get("dateOfBirth", ""),
            "status": user_data.get("maritalStatus", ""),
            "address": f"{user_data.get('province', '')}, {user_data.get('district', '')}, {user_data.get('sector', '')}, {user_data.get('cell', '')}",
            "provinces": provinces,
            "default_province": default_province.id if default_province else None,
            "default_district": default_district.id if default_district else None,
            "default_sector": default_sector.id if default_sector else None,
            "default_cell": default_cell.id if default_cell else None,
            "default_village": default_village.id if default_village else None,
            "default_street": user_data.get("address", "")
        })

    elif request.method == "POST" and "save_citizen" in request.POST:
        user_data = request.session.get("user_data", {})
        national_id = request.session.get("national_id", "")

        if not user_data or not national_id:
            return JsonResponse({"error": "Session expired. Please verify NID again."})

        # Location data from form
        province_id = request.POST.get("province")
        district_id = request.POST.get("district")
        sector_id = request.POST.get("sector")
        cell_id = request.POST.get("cell")
        village_id = request.POST.get("village")
        street = request.POST.get("street", "")

        # Authentication fields
        username = request.POST.get("username", f"user_{national_id}")
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")

        # Password
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        password = request.POST.get("password", random_password)

        try:
            province = Province.objects.get(id=province_id) if province_id else None
            district = District.objects.get(id=district_id) if district_id else None
            sector = Sector.objects.get(id=sector_id) if sector_id else None
            cell = Cell.objects.get(id=cell_id) if cell_id else None
            village = Village.objects.get(id=village_id) if village_id else None
        except (Province.DoesNotExist, District.DoesNotExist, Sector.DoesNotExist, Cell.DoesNotExist, Village.DoesNotExist):
            return JsonResponse({"error": "Invalid location selection."})

        # Process photo
        image_file = None
        if user_data.get("photo", ""):
            try:
                image_data = base64.b64decode(user_data["photo"])
                image_file = ContentFile(image_data)
            except Exception:
                pass

        # Parse DOB again
        dob = None
        try:
            dob = datetime.strptime(user_data.get("dateOfBirth", ""), "%Y-%m-%d").date()
        except Exception:
            pass

        # Get current agent
        agent = request.user.agent

        # Create or update Citizen
        citizen, created = Citizen.objects.update_or_create(
            nid=national_id,
            defaults={
                'name': f"{user_data.get('foreName', '')} {user_data.get('surName', '')}".strip(),
                'nationality': user_data.get('nationality', ''),
                'gender': 'M' if user_data.get('gender', '').upper() == 'MALE' else 'F',
                'dob': dob,
                'marital_status': user_data.get('maritalStatus', ''),
                'agent_reference': agent,
                'province': province,
                'district': district,
                'sector': sector,
                'cell': cell,
                'village': village,
                'street': street,
                'username': username,
                'email': email,
                'phone_number': phone_number,
                'password': make_password(password),
            }
        )

        if image_file:
            citizen.picture.save(f"{national_id}.jpg", image_file, save=True)

        # Clear session
        request.session.pop("user_data", None)
        request.session.pop("national_id", None)

        return redirect("/login/")

    return render(request, "nidvalidation.html")


def get_districts(request):
    province_id = request.GET.get("province_id")
    districts = District.objects.filter(province_id=province_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)

def get_sectors(request):
    district_id = request.GET.get("district_id")
    sectors = Sector.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(sectors), safe=False)

def get_cells(request):
    sector_id = request.GET.get("sector_id")
    cells = Cell.objects.filter(sector_id=sector_id).values("id", "name")
    return JsonResponse(list(cells), safe=False)

def get_villages(request):
    cell_id = request.GET.get("cell_id")
    villages = Village.objects.filter(cell_id=cell_id).values("id", "name")
    return JsonResponse(list(villages), safe=False)


@login_required
def admin_dashboard(request):
    user_count = Citizen.objects.count()
    citizens = Citizen.objects.all()
    complaints = Complaint.objects.all()
    publicservices = PublicService.objects.all()
    publicservices_count = PublicService.objects.count()
    villages = Village.objects.select_related(
        'cell__sector__district__province'
    ).all()

    context = {
        "publicservices_count":publicservices_count,
        "user_count": user_count,
        "citizens": citizens,
        "villages": villages,
        "publicservices":publicservices,
        "complaints":complaints
    }
    return render(request, "dashboard.html", context)



def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/admin_dashboard/")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "admin_login.html")

class ProvinceListView(ListView):
    model = Province
    template_name = 'locations/province_list.html'
    context_object_name = 'provinces'

class ProvinceCreateView(CreateView):
    model = Province
    form_class = ProvinceForm
    template_name = 'locations/province_form.html'
    success_url = '/provinces/'

class ProvinceUpdateView(UpdateView):
    model = Province
    form_class = ProvinceForm
    template_name = 'locations/province_form.html'
    success_url = reverse_lazy('province_list')

class ProvinceDeleteView(DeleteView):
    model = Province
    template_name = 'locations/province_confirm_delete.html'
    success_url = reverse_lazy('province_list')

class DistrictListView(ListView):
    model = District
    template_name = 'locations/district_list.html'
    context_object_name = 'districts'

class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm
    template_name = 'locations/district_form.html'
    success_url = ('/districts/')

class DistrictUpdateView(UpdateView):
    model = District
    form_class = DistrictForm
    template_name = 'locations/district_form.html'
    success_url = reverse_lazy('district_list')

class DistrictDeleteView(DeleteView):
    model = District
    template_name = 'locations/district_confirm_delete.html'
    success_url = reverse_lazy('district_list')

class SectorListView(ListView):
    model = Sector
    template_name = 'locations/sector_list.html'
    context_object_name = 'sectors'

class SectorCreateView(CreateView):
    model = Sector
    form_class = SectorForm
    template_name = 'locations/sector_form.html'
    success_url = ('/sectors/')

class SectorUpdateView(UpdateView):
    model = Sector
    form_class = SectorForm
    template_name = 'locations/sector_form.html'
    success_url = reverse_lazy('sector_list')

class SectorDeleteView(DeleteView):
    model = Sector
    template_name = 'locations/sector_confirm_delete.html'
    success_url = reverse_lazy('sector_list')

class CellListView(ListView):
    model = Cell
    template_name = 'locations/cell_list.html'
    context_object_name = 'cells'

class CellCreateView(CreateView):
    model = Cell
    form_class = CellForm
    template_name = 'locations/cell_form.html'
    success_url = reverse_lazy('cell_list')

class CellUpdateView(UpdateView):
    model = Cell
    form_class = CellForm
    template_name = 'locations/cell_form.html'
    success_url = reverse_lazy('cell_list')

class CellDeleteView(DeleteView):
    model = Cell
    template_name = 'locations/cell_confirm_delete.html'
    success_url = reverse_lazy('cell_list')

class VillageListView(ListView):
    model = Village
    template_name = 'locations/village_list.html'
    context_object_name = 'villages'

class VillageCreateView(CreateView):
    model = Village
    form_class = VillageForm
    template_name = 'locations/village_form.html'
    success_url = reverse_lazy('village_list')

class VillageUpdateView(UpdateView):
    model = Village
    form_class = VillageForm
    template_name = 'locations/village_form.html'
    success_url = reverse_lazy('village_list')

class VillageDeleteView(DeleteView):
    model = Village
    template_name = 'locations/village_confirm_delete.html'
    success_url = reverse_lazy('village_list')


def agent_create(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/agents/')
    else:
        form = AgentForm()
    
    return render(request, 'agent_create.html', {'form': form})




def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'agent_list.html', {'agents': agents})


def agent_signup(request):
    if request.method == 'POST':
        form = AgentSignUpForm(request.POST)
        if form.is_valid():
            # Create the user account
            user = form.save()
            # Create the agent profile linked to the user
            Agent.objects.create(
                user=user,
                name=form.cleaned_data.get('name'),
                agent_reference=form.cleaned_data.get('agent_reference')
            )
            # Log the user in
            login(request, user)
            return redirect('/agent/login')
    else:
        form = AgentSignUpForm()
    return render(request, 'agent_signup.html', {'form': form})




def get_districts(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def get_sectors(request):
    district_id = request.GET.get('district_id')
    sectors = Sector.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse(list(sectors), safe=False)

def get_cells(request):
    sector_id = request.GET.get('sector_id')
    cells = Cell.objects.filter(sector_id=sector_id).values('id', 'name')
    return JsonResponse(list(cells), safe=False)

def get_villages(request):
    cell_id = request.GET.get('cell_id')
    villages = Village.objects.filter(cell_id=cell_id).values('id', 'name')
    return JsonResponse(list(villages), safe=False)

def generate_account_number():
    return f"ACCT{random.randint(10000000, 99999999)}"

@login_required
def save_citizen_info(request):
    if request.method == 'POST':
        # Retrieve POST data
        nid = request.POST.get('nid')
        street = request.POST.get('street')
        province_id = request.POST.get('province')
        district_id = request.POST.get('district')
        sector_id = request.POST.get('sector')
        cell_id = request.POST.get('cell')
        village_id = request.POST.get('village')
        account_number = request.POST.get('account_number') or generate_account_number()
        
        username = request.POST.get('username', f"user_{nid}")
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')

        # Generate random password if not provided
        raw_password = request.POST.get('password')
        if not raw_password:
            raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        hashed_password = make_password(raw_password)

        # Get optional fields
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        nationality = request.POST.get('nationality')

        # Get authenticated agent
        try:
            agent = request.user.agent
        except Agent.DoesNotExist:
            return render(request, 'error.html', {'error': 'Agent profile not found for user'})

        try:
            province = Province.objects.get(id=province_id)
            district = District.objects.get(id=district_id)
            sector = Sector.objects.get(id=sector_id)
            cell = Cell.objects.get(id=cell_id)
            village = Village.objects.get(id=village_id)
        except Exception as e:
            return render(request, 'error.html', {'error': f'Location selection error: {str(e)}'})

        # Create a new Django User
        user = User.objects.create_user(username=username, email=email, password=raw_password)
        
        # Create the Citizen record
        Citizen.objects.create(
            user=user,
            username=username,
            email=email,
            phone_number=phone_number,
            nid=nid,
            account_number=account_number,
            nationality=nationality,
            dob=dob,
            name=name,
            agent_reference=agent,
            province=province,
            district=district,
            sector=sector,
            cell=cell,
            village=village,
            street=street,
            password=hashed_password
        )
       
        return redirect('/login/') 
    return redirect('form_page') 


@login_required
def citizen_dashboard(request):
    citizen = request.user.citizen
    complaints = Complaint.objects.filter(citizen=citizen).order_by('-created_at')  # show latest first
    services = PublicService.objects.all()
    # Handle form submission
    if request.method == 'POST':
        form = CitizenEditForm(request.POST, instance=citizen)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('/citizen/dashboard')
    else:
        form = CitizenEditForm(instance=citizen)

  

    return render(request, 'citizendashboard.html', {
        'citizen': citizen,
        'form': form,
        'services':services,
        'complaints': complaints,

    })



def citizen_login_view(request):
    if request.method == 'POST':
        identifier = request.POST['username']
        password = request.POST['password']

        user = None

        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            # Matching with Citizen model by nid or account_number
            citizen = Citizen.objects.filter(nid=identifier).first()
            if not citizen:
                citizen= Citizen.objects.filter(account_number=identifier).first()
            if citizen:
                user = citizen.user

        # Confirm we have a real User instance
        if isinstance(user, User):
            auth_user = authenticate(request, username=user.username, password=password)
            if isinstance(auth_user, User):
                if Citizen.objects.filter(user=auth_user).exists():
                    login(request, auth_user)
                    return redirect('/citizen/dashboard/')
                else:
                    messages.error(request, 'You are not registered as a citizen.')
            else:
                messages.error(request, 'Invalid credentials.')
        else:
            messages.error(request, 'User not found.')

    return render(request, 'login.html')

User = get_user_model()


def citizen_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            User = get_user_model()
            user = User.objects.get(username=user.username)

            if hasattr(user, 'citizen'):
                citizen = user.citizen
                login(request, user)
                messages.success(request, f"Welcome {citizen.name or citizen.username}!")

                return redirect('/citizen/dashboard')
            else:
                messages.error(request, "You are authenticated but not registered as a citizen.")

        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def citizen_profile(request, citizen_id):
    citizen = get_object_or_404(Citizen, id=citizen_id)
    return render(request, 'citizen_profile.html', {'citizen': citizen})

@login_required
def edit_citizen(request, citizen_id):
    citizen = get_object_or_404(Citizen, id=citizen_id)
    
    complaints = citizen.complaints.all()
    
    if request.method == 'POST':
        form = CitizenEditForm(request.POST, request.FILES, instance=citizen)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('/admin_dashboard/')
            else:
                return redirect('/citizen/dashboard')
    else:
        form = CitizenEditForm(instance=citizen)

    return render(request, 'edit_citizen.html', {
        'form': form,
        'complaints': complaints,
    })


@login_required
def edit_service(request, service_id):
    service = get_object_or_404(PublicService, id=service_id)
    
    
    if request.method == 'POST':
        form = ServiceEditForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('/admin_dashboard/')
            else:
                return redirect('/citizen/dashboard')
    else:
        form = ServiceEditForm(instance=service)

    return render(request, 'edit_service.html', {
        'form': form,

    })
def delete_citizen(request, citizen_id):
    citizen = get_object_or_404(Citizen, id=citizen_id)
    if request.method == 'POST':
        citizen.delete()
        messages.success(request, "Citizen deleted successfully.")
    return redirect('/admin_dashboard/')


def delete_citizen(request, citizen_id):
    citizen = get_object_or_404(Citizen, id=citizen_id)
    if request.method == 'POST':
        citizen.delete()
        messages.success(request, "Citizen deleted successfully.")
    return redirect('/admin_dashboard/')

def delete_service(request, service_id):
    service= get_object_or_404(PublicService, id=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully.")
    return redirect('/admin_dashboard/')

def add_publicservice(request):
    if request.method == 'POST':
        form = PublicServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_dashboard/')
    else:
        form = PublicServiceForm()
    return render(request, 'addpublicservice.html', {'form': form})


@login_required
def submit_complaint(request, service_id):
    try:
        citizen = request.user.citizen 
    except Citizen.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to submit a complaint. Login as citizen")

    try:
        publicservice = PublicService.objects.get(id=service_id)
    except PublicService.DoesNotExist:
        messages.error(request, "Selected public service does not exist.")
        return redirect('services')

    if request.method == 'POST':
        complaint_nature = request.POST.get('complaintNature')
        complaint_details = request.POST.get('details')

        complaint = Complaint.objects.create(
            citizen=citizen,
            publicService=publicservice,
            complaintNature=complaint_nature,
            details=complaint_details,
            complaint_id=f"COMP-{uuid.uuid4().hex[:8].upper()}",
            status="pending",
        )

        messages.success(request, "Complaint submitted successfully.")
        return redirect(f'/complaint_status/{complaint.id}/')

    return render(request, 'submit_complaint.html', {
        'publicservice': publicservice 
    })



@login_required
def complaint_status(request, complaint_id):
    if request.user.is_superuser:
        # Allow admin to view any complaint
        complaint = get_object_or_404(Complaint, id=complaint_id)
    else:
        try:
            citizen = request.user.citizen
        except Citizen.DoesNotExist:
            return HttpResponseForbidden("You are not authorized to view Complaint details")

        
        complaint = get_object_or_404(Complaint, id=complaint_id, citizen=citizen)

    return render(request, 'complaint_status.html', {'complaint': complaint})


def give_feedback(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.complaint = complaint
            feedback.save()

            # Update the complaint's status to 'Resolved'
            complaint.status = 'Resolved'
            complaint.save()

            return redirect('/admin_dashboard/')  # Adjust as needed
    else:
        form = FeedbackForm()

    return render(request, 'give_feedback.html', {
        'form': form,
        'complaint': complaint
    })


@login_required
def submit_agency_feedback(request, service_id):
    service = get_object_or_404(PublicService, id=service_id)

    if request.method == 'POST':
        details = request.POST.get('details')

        AgencyFeedback.objects.create(
            publicservice=service,
            user=request.user,
            details=details
        )
        return redirect(f'/view_service_feedbacks/{service.id}/')

    return render(request, 'submit_agency_feedback.html', {'service': service})


@login_required
def view_service_feedbacks(request, service_id):
    service = get_object_or_404(PublicService, id=service_id)
    feedbacks = service.agencyfeedbacks.all().order_by('-created_at')
    return render(request, 'view_service_feedbacks.html', {'service': service, 'feedbacks': feedbacks})


