from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from base.forms import RoomForm, MessageForm
from base.models import Room, Message

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

class RoomCreateView(CreateView): #použitím CreateView je ukládání do databáze automatizováno
    template_name = 'base/room_form.html' #šablona použití formuláře
    form_class = RoomForm #který formulář použijeme
    success_url = reverse_lazy('index') #podobné jako return redirect

    def form_invalid(self, form):
       return super().form_invalid(form)

class RoomUpdateView(UpdateView):
    template_name = 'base/room_form.html'
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        return super().form_invalid(form)

class RoomDeleteView(DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    success_url = reverse_lazy('index')
# def RoomCreateView(request):
#     if request.method == 'POST':
#         form = RoomForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     form = RoomForm()
#     context = {'form': form}
#     return render(request, 'base/room_form.html', context)

def MessageCreateView(request):
    if request.method == 'GET':
        message_form = MessageForm()
        context = {'message_form': message_form}
        return render(request,'base/message_form.html', context)
    elif request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()
            return redirect('index')
    else:
        return redirect('index')



class RoomsView(ListView):
    template_name = 'base/index.html'
    model = Room

# class MessageView(ListView):
#     template_name = 'base/room.html'
#     model = Message

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    # POST
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    # GET
    context = {'room': room, 'messages': messages}
    return render(request, 'base/room.html', context)