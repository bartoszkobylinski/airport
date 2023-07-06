from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .airport_sim import AirportSimulator
from .plane_sim import AirplaneSimulator


@shared_task()
def run_airport_simulation():
    airport_simulator = AirportSimulator()
    airport_simulator.run_simulation()


@shared_task()
def run_airplane_simulation():
    airplane_simulator = AirplaneSimulator()
    airplane_simulator.run_simulation()
