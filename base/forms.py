from django.forms import ModelForm
from django.core.exceptions import ValidationError
from virtualenv.report import LOGGER

from base.models import Message, Room


class RoomForm(ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            validation_error = ValidationError('Jméno musí být delší jak dva')
            LOGGER.warning(f'{validation_error}: {name}')
            raise validation_error
        if Room.objects.filter(name__iexact=name).exists():
            validation_error = ValidationError('Tato místnost již existuje')
            LOGGER.warning(f'{validation_error}: {name}')
            raise validation_error
        return name
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
