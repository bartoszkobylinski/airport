from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.db.models import Min
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
        all_airplanes = Airplane.objects.values_list('airplane_id', flat=True).distinct()
        airplane_data = []

        for airplane_id in all_airplanes:
            cached_positions = request.session.get(f'cached_positions_{airplane_id}', [])
            next_position_index = request.session.get(f'next_position_index_{airplane_id}', 0)

            if next_position_index >= len(cached_positions):
                cached_positions = list(Airplane.objects.filter(airplane_id=airplane_id).order_by('timestamp')[
                                        next_position_index:next_position_index + 20
                                        ].values('x', 'y', 'z', 'status', 'fuel', 'image_url'))
                next_position_index = 0

            if cached_positions:
                next_position = cached_positions[next_position_index]
                next_position_index += 1

                request.session[f'cached_positions_{airplane_id}'] = cached_positions
                request.session[f'next_position_index_{airplane_id}'] = next_position_index

                x, y, z = next_position['x'], next_position['y'], next_position['z']
                x_2d, y_2d, image_size = Airplane.project_to_screen(x, y, z)
                x_2d = round(x_2d)
                y_2d = round(y_2d)
                next_position['x'], next_position['y'], next_position['image_size'] = x_2d, y_2d, image_size

                airplane_data.append({
                    'id': airplane_id,
                    **next_position,
                })

        return JsonResponse(airplane_data, safe=False)


class AnimationView(TemplateView):
    template_name = "airport_app/an.html"


class TestS3BucketImageView(TemplateView):
    template_name = "airport_app/test_view.html"
