from django.urls import path
from .  import views

urlpatterns = [
    path('', views.index),
    path('demos', views.demo_charts),
    path('upload_csv', views.upload_csv),
    path('upload_success', views.upload_success),
    path('db_load_csv/<int:id>', views.db_load_csv),
    path('db_load_success/<int:row_count>', views.db_load_sucess),
    path('compare/daily_cases', views.compare_daily_cases),
    path('charts/oneStateDailyCases', views.oneStateDailyCases, name="oneStateDailyCases"),
    path('charts/fourStatesDailyCases', views.fourStatesDailyCases, name="fourStatesDailyCases"),
]