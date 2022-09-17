from django.views.generic import ListView

from base.models import Room


class RoomsView(ListView):
    template_name = 'base/index.html'
    model = Room