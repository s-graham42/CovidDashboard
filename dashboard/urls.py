from django.urls import path
from .  import views

urlpatterns = [
    path('', views.index),
    path('covidInformation', views.covid_info),
    path('vaccines', views.vaccines_main),
    path('dashboard_admin', views.dashboard_admin),
    path('dashboard_admin/demos', views.demo_charts),
    path('dashboard_admin/upload_csv', views.upload_csv),
    path('dashboard_admin/upload_success', views.upload_success),
    path('dashboard_admin/db_load_states', views.db_load_states),
    path('dashboard_admin/view_states', views.view_states),
    path('apiData/<str:source>/singleVariable', views.singleVariable),
    path('charts/USTotals', views.usTotalsChart, name="usTotalsChart"),
    path('charts/singleVariableOverTime/<str:source>', views.singleVariableOverTime, name="singleVariableOverTime"),
]