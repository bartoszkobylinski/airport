from django.urls import path
from .views import index, StartSimulationView, StatsView, AirplaneCoordinatesView, AnimationView

urlpatterns = [
    path("", index, name="index"),
    path("start_simulation/", StartSimulationView.as_view(), name="start_simulation"),
    path("airplanes/", StatsView.as_view(), name="airplanes"),
    path("fetch_airplane_coordinates/", AirplaneCoordinatesView.as_view(), name="fetch_airplane_coordinates"),
    path("animation/", AnimationView.as_view(), name="animation_view"),
]
