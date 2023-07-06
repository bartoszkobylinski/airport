from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic.list import ListView
from .tasks import run_airplane_simulation, run_airport_simulation
from .models import Airplane


def index(request):
    return HttpResponse("Hello, word. Your at airport_class app")


class StartSimulationView(View):
    def get(self, request):
        run_airport_simulation.apply_async()
        run_airplane_simulation.apply_async(countdown=10)
        return JsonResponse({"message": "Simulation started"})


class StatsView(ListView):
    model = Airplane
    template_name = "airport_app/templates/airplane_list.html"
