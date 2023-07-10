from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .tasks import run_airplane_simulation, run_airport_simulation
from .models import Airplane


def index(request):
    return HttpResponse("Hello, word. Your at airport_class app")


class StartSimulationView(View):
    def get(self, request):
        Airplane.delete_all()
        run_airport_simulation.apply_async()
        run_airplane_simulation.apply_async(countdown=10)
        return JsonResponse({"message": "Simulation started"})


class StatsView(ListView):
    model = Airplane
    template_name = "airport_app/airplane_list.html"


class AirplaneCoordinatesView(View):

    def get(self, request, *args, **kwargs):
        airplanes = Airplane.objects.all().order_by('airplane_id')
        airplane_data = []

        for airplane in airplanes:
            cached_positions = request.session.get(f'cached_positions_{airplane.airplane_id}', [])
            next_position_index = request.session.get(f'next_position_index_{airplane.airplane_id}', 0)

            if next_position_index >= len(cached_positions) - 1:
                cached_positions = list(airplane.positions.order_by('timestamp')[
                                        next_position_index:next_position_index + 20
                                        ].values('x', 'y', 'z', 'status', 'fuel'))
                next_position_index = 0

            if cached_positions:
                next_position = cached_positions[next_position_index]
                next_position_index += 1

                request.session[f'cached_positions_{airplane.airplane_id}'] = cached_positions
                request.session[f'next_position_index_{airplane.airplane_id}'] = next_position_index

                airplane_data.append({
                    'id': airplane.airplane_id,
                    **next_position,
                })


class AnimationView(TemplateView):
    template_name = "airport_app/an.html"
