
from django.contrib import admin
from .models import Province, District, Sector, Cell, Village, Complaint, Feedback, Citizen, PublicService
from .forms import ProvinceForm, DistrictForm, SectorForm, CellForm, VillageForm, ComplaintForm, FeedbackForm

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    form = ProvinceForm
    list_display = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    form = DistrictForm
    list_display = ['name', 'province']
    list_filter = ['province']

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    form = SectorForm
    list_display = ['name', 'district']
    list_filter = ['district']

@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    form = CellForm
    list_display = ['name', 'sector']
    list_filter = ['sector']

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    form = VillageForm
    list_display = ['name', 'cell']
    list_filter = ['cell']

from .models import Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_reference', 'name')  # Displays agent_reference and name in the list view
    search_fields = ('agent_reference', 'name')  # Allows searching by agent_reference or name

admin.site.register(Agent, AgentAdmin) 

@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nid', 'account_number', 'nationality', 'province', 'district', 'agent_reference')
    search_fields = ('name', 'nid', 'account_number')
    list_filter = ('province', 'district', 'sector')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is in "Citizen" group, show only their own record
        if request.user.groups.filter(name="Citizen").exists():
            return qs.filter(user=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        # Citizens can only change their own record
        if request.user.groups.filter(name="Citizen").exists():
            if obj is not None and obj.user != request.user:
                return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        # Citizens can only view their own record
        if request.user.groups.filter(name="Citizen").exists():
            if obj is not None and obj.user != request.user:
                return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        # Prevent citizens from adding new Citizen records
        if request.user.groups.filter(name="Citizen").exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent citizens from deleting records
        if request.user.groups.filter(name="Citizen").exists():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(PublicService)
class PublicServiceAdmin(admin.ModelAdmin):
    list_display = ('serviceType', 'definition')
    search_fields = ('serviceType', 'definition')



@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintForm
    list_display = ('complaint_id', 'citizen', 'publicService', 'status', 'created_at')
    search_fields = ('complaint_id', 'citizen__name', 'publicService__name', 'status')
    list_filter = ('status', 'publicService')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    form = FeedbackForm
    list_display = ('complaint', 'created_at')
    search_fields = ('complaint__complaint_id',)