from django.urls import path
from .views import index, StartSimulationView, StatsView

urlpatterns = [
    path("", index, name="index"),
    path("start_simulation/", StartSimulationView.as_view(), name="start_simulation"),
    path("airplanes/", StatsView.as_view(), name="airplanes")
]
