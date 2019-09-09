import re

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import User, LocationWeather
from .forms import NameForm, WeatherForm, DeleteForm

def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['user_name']
            #Confirm valid characters (cheap way to avoid url spoofing issues)
            if not re.match("^[A-Za-z0-9_]+$", name):
                return render(request, 'weather/index.html', {'form': form, 'message' : "Use only letters, numbers, and underscores."})
            if not User.objects.filter(user_name=name).exists():
            #TODO: Implement checking username and prompt to create or retry login, for now just creating user
            #    return render(request, 'weather/index.html', {'form': form, 'message' : "username does not exist"})
                #create a location for now that is temporary. need to move to postgresql and use array list, then look up or create LocationWeather
                u = User(user_name=name)
                u.save()
            return redirect('/weather/' + name)
        else:
            return render(request, 'weather/index.html', {'form': form, 'message' : "There was a problem with the form. Please try again"})
    form = NameForm()
    return render(request, 'weather/index.html', {'form': form})

def get_user(request, name):
    user = User.objects.get(user_name=name)
    for child in user.child_set.all():
        child.update_weather()

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            if len(user.child_set.filter(location_querry=form.cleaned_data['location'])) > 0:
                return render(request, 'weather/user.html', {'user': user, 'form' : form, 'message' : "Location already added"})
            l = LocationWeather(location_querry=form.cleaned_data['location'])
            if not l.get_weather():
                #send back message that location was invalid
                return render(request, 'weather/user.html', {'user': user, 'form' : form, 'message' : "Failed ot find location"})
            l.save()
            user.child_set.add(l)
        elif request.POST.get('logout_btn'):
            return redirect('/weather/')
        elif request.POST.get('remove_btn'):
            child_id = request.POST.get('child_id')
            user.child_set.filter(id=child_id).delete()
    user.save()
    form = WeatherForm()
    delete_form = DeleteForm()
    return render(request, 'weather/user.html', {'user': user, 'form' : form, 'delete_form': delete_form})
