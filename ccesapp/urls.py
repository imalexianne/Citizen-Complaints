from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from ccesproject import settings

from .views import admin_login
from .views import admin_dashboard
from .views import (
    ProvinceListView, ProvinceCreateView, ProvinceUpdateView, ProvinceDeleteView,
    DistrictListView, DistrictCreateView, DistrictUpdateView, DistrictDeleteView,
    SectorListView, SectorCreateView, SectorUpdateView, SectorDeleteView,
    CellListView, CellCreateView, CellUpdateView, CellDeleteView,
    VillageListView, VillageCreateView, VillageUpdateView, VillageDeleteView
)

app_name = "ccesapp"

urlpatterns = [
    
    path('', auth_views.LoginView.as_view(), name='index'),
    path('citizen/registration', views.signup, name='signup'),
    path('verify_nid', views.verify_nid, name='verify_nid'),
    path('password', views.password, name='password'),
    
    path('user-management', views.usermanagement, name='usermanagement'),

    path('confirm-save-citizen', views.save_citizen_from_session, name='save_citizen_from_session'),
    
    path('citizenform', views.citizenform, name='citizenform'),

    path('ajax/get-districts/', views.get_districts, name='get_districts'),
    path('ajax/get-sectors/', views.get_sectors, name='get_sectors'),
    path('ajax/get-cells/', views.get_cells, name='get_cells'),
    path('ajax/get-villages/', views.get_villages, name='get_villages'),

    path("admin-login/", admin_login, name="admin_login"),

    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path('provinces/', ProvinceListView.as_view(), name='province_list'),
    path('provinces/add/', ProvinceCreateView.as_view(), name='province_create'),
    path('provinces/<int:pk>/edit/', ProvinceUpdateView.as_view(), name='province_update'),
    path('provinces/<int:pk>/delete/', ProvinceDeleteView.as_view(), name='province_delete'),

    path('districts/', DistrictListView.as_view(), name='district_list'),
    path('districts/add/', DistrictCreateView.as_view(), name='district_create'),
    path('districts/<int:pk>/edit/', DistrictUpdateView.as_view(), name='district_update'),
    path('districts/<int:pk>/delete/', DistrictDeleteView.as_view(), name='district_delete'),

    path('sectors/', SectorListView.as_view(), name='sector_list'),
    path('sectors/add/', SectorCreateView.as_view(), name='sector_create'),
    path('sectors/<int:pk>/edit/', SectorUpdateView.as_view(), name='sector_update'),
    path('sectors/<int:pk>/delete/', SectorDeleteView.as_view(), name='sector_delete'),

    path('cells/', CellListView.as_view(), name='cell_list'),
    path('cells/add/', CellCreateView.as_view(), name='cell_create'),
    path('cells/<int:pk>/edit/', CellUpdateView.as_view(), name='cell_update'),
    path('cells/<int:pk>/delete/', CellDeleteView.as_view(), name='cell_delete'),

    path('villages/', VillageListView.as_view(), name='village_list'),
    path('villages/add/', VillageCreateView.as_view(), name='village_create'),
    path('villages/<int:pk>/edit/', VillageUpdateView.as_view(), name='village_update'),
    path('villages/<int:pk>/delete/', VillageDeleteView.as_view(), name='village_delete'),

    path('agent/create/', views.agent_create, name='agent_create'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agent/signup/', views.agent_signup, name='agent_signup'),
    
    path('agent/login', views.agent_login, name='agent_login'),
    path('citizen/login', views.citizen_login, name='citizen_login'),
    
    path('citizen/dashboard', views.citizen_dashboard, name='citizen_dashboard'),

    path('save-citizen/', views.save_citizen_info, name='save_citizen_info'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('dashboard/', views.redirect_after_login, name='redirect_after_login'),

    path('citizen_profile/<int:citizen_id>', views.citizen_profile, name='citizen_profile'),
    path('edit_citizen/<int:citizen_id>', views.edit_citizen, name='edit_citizen'),

    path('edit_service/<int:service_id>', views.edit_service, name='edit_service'),
    
    path('delete_citizen/<int:citizen_id>', views.delete_citizen, name='delete_citizen'),
    path('delete_service/<int:service_id>', views.delete_service, name='delete_service'),

    path('add_publicservice/', views.add_publicservice, name='add_publicservice'),
   
    path('submit_complaint/<int:service_id>/', views.submit_complaint, name='submit_complaint'),

    path('complaint_status/<int:complaint_id>/', views.complaint_status, name='complaint-status'),
    path('give_feedback/<int:complaint_id>', views.give_feedback, name='give_feedback'),
   
    path('submit_feedback/<int:service_id>/', views.submit_agency_feedback, name='submit_agency_feedback'),
   
    path('view_service_feedbacks/<int:service_id>/', views.view_service_feedbacks, name='view_service_feedbacks'),

    
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
