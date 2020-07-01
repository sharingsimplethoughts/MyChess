from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from game.models import *
from .forms import *
# Create your views here.
class ListGameTimeListView(TemplateView):
    def get(self,request,*args, **kwargs):
        durs = GameDuration.objects.all()
        return render(request,'agametime/gameduration.html',{'durs':durs})

class AddGameTimeView(TemplateView):
    def post(self,request,*args, **kwargs):
        durs = GameDuration.objects.all()
        newdur = request.POST['newdur']
        form = AddOrEditGameTimeForm(request.POST or None)
        if form.is_valid():
            g = GameDuration(
                duration = newdur,
            )
            g.save()
            message='Duration saved successfully'
            messages.add_message(request, messages.INFO, message)
            durs = GameDuration.objects.all()
            return render(request,'agametime/gameduration.html',{'durs':durs})
        print(form)
        print(form.non_field_errors)
        return render(request,'agametime/gameduration.html',{'form':form,'durs':durs})
        

class EditGameTimeView(TemplateView):
    def post(self,request,*args, **kwargs):
        print('inside------------')
        durs = GameDuration.objects.all()
        dur = request.POST['durid']
        newdur = request.POST['newdur']
        form = AddOrEditGameTimeForm(request.POST or None)
        if form.is_valid():
            obj = GameDuration.objects.filter(id=dur).first()
            if not obj:
                message = "Invalid duration id"
                messages.add_message(request, messages.INFO, message)
                return render(request,'agametime/gameduration.html',{'durs':durs})
            obj.duration = newdur
            obj.save()
            message = "Duration updated successfully"
            messages.add_message(request, messages.INFO, message)
            durs = GameDuration.objects.all()
            return render(request,'agametime/gameduration.html',{'durs':durs})
        return render(request,'agametime/gameduration.html',{'form':form,'durs':durs})
                

            


