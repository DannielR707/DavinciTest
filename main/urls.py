from django.urls import path

from django.conf.urls import include, url
from django.contrib import admin

from main import views


urlpatterns = [
    path('', views.home, name='home'),
    path('crear_campaña', views.createCampaign, name='createCampaign'),
    path('borrar_campaña/<int:campaign_id>', views.deleteCampaign, name='deleteCampaign'),
    path('campaña/<int:campaign_id>', views.detailCampaign, name='detailCampaign'),
    path('subir_información/<int:campaign_id>', views.model_form_upload, name='model_form_upload'),
    path('revisar_archivo/<int:campaign_id>', views.checkFileColumns, name='checkFileColumns'),
    path('borrar_información/<int:info_id>', views.deleteInfo, name='deleteInfo'),
    path('borrar_toda_información/<int:campaign_id>', views.deleteAllInfo, name='deleteAllInfo'),
    
]