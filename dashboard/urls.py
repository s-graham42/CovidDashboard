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
    path('dashboard_admin/db_load_csv/<int:id>', views.db_load_csv),
    path('dashboard_admin/db_load_success/<int:row_count>', views.db_load_sucess),
    path('apiData', views.apiData),
    path('apiData/newYorkTimes/singleVariable', views.nyt_svot),
    path('compare/daily_cases', views.compare_daily_cases),
    path('compare/singleVariable', views.compare_single_variable),
    path('charts/USTotals', views.usTotalsChart, name="usTotalsChart"),
    path('charts/oneStateDailyCases', views.oneStateDailyCases, name="oneStateDailyCases"),
    path('charts/fourStatesDailyCases', views.fourStatesDailyCases, name="fourStatesDailyCases"),
    path('charts/singleVariableOverTime', views.singleVariableOverTime, name="singleVariableOverTime"),
]