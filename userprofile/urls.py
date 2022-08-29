from .views import ProfileView, upgrade_me, DownGrade, profile_edit_view
from django.urls import path

app_name = 'profile'

urlpatterns = [
    path('', ProfileView.as_view(), name='lk'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('downgrade/', DownGrade.as_view(), name='downgrade'),
    path('edit/', profile_edit_view, name='edit'),
]
