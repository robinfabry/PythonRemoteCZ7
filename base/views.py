from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView

from base.forms import RoomForm
from base.models import Room


# Create your views here.
def hello(request):
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello, {s} world!')


def search(request):
    q = request.GET.get('q', '')  # 127.0.0.1/search?q=Dja
    if q == '':
        return HttpResponse("Prosím zadejte hledaný výraz.")
    rooms = Room.objects.filter(
        Q(description__contains=q) |
        Q(name__contains=q)
    )
    context = {'query': q, 'rooms': rooms}
    return render(request, "base/search.html", context)

def room(request, id_room):
    room = Room.objects.get(id=id_room)
    context = {'room': room}
    return render(request, "base/room.html", context)

# def room_v2(request):
#     id_room = request.GET.get('id_room', '')
#     if id_room == '':
#         return HttpResponse("Prosím zadejte číslo do adresy room/*číslo*.")
#     room = Room.objects.get(id=id_room)
#     context = {'room': room}
#     return render(request, "base/room.html", context)

def RoomCreateView(request):
    if request.method == 'GET':
        form = RoomForm()
        context = {'form': form}
        return render(request,'base/room_form.html', context)
    elif request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        return redirect('index')


class RoomsView(ListView):
    template_name = 'base/index.html'
    model = Room