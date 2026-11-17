from django.contrib.auth import views as auth_views
from django.urls import path

from jangela.presentation import views
from jangela.presentation.forms import SaioaHasiForm

urlpatterns = [
    path("", views.hasiera, name="hasiera"),
    # Login/logout: Django-ren bistak (UC01/UC02, UC06/UC07, UC18/UC19)
    path(
        "saioa-hasi/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=SaioaHasiForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # LogoutView-ek POST soilik onartzen du
    path("irten/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("ikaslea/dashboard/", views.ikaslea_dashboard, name="ikaslea_dashboard"),
    path("irakaslea/dashboard/", views.irakaslea_dashboard, name="irakaslea_dashboard"),
    path("sukaldea/dashboard/", views.sukaldea_dashboard, name="sukaldea_dashboard"),
    # Menuen CRUDa (UC15–UC17)
    path("sukaldea/menuak/", views.menuak, name="menuak"),
    path("sukaldea/menuak/sortu/", views.menua_sortu, name="menua_sortu"),
    path("sukaldea/menuak/<int:pk>/editatu/", views.menua_editatu, name="menua_editatu"),
    path("sukaldea/menuak/<int:pk>/ezabatu/", views.menua_ezabatu, name="menua_ezabatu"),
]
