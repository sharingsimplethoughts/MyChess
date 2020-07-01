from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
import openpyxl
from usubscription.models import *
from accounts.models import *
from .forms import *
# Create your views here.

class SubscriptionListView(TemplateView):
    def get(self,request,*args, **kwargs):
        subs = SubscriptionPlan.objects.filter(is_deleted=False)
        return render(request,'asubscription/subscriptions.html',{'subs':subs})

class AddSubscriptionView(TemplateView):
    def get(self,request,*args, **kwargs):
        return render(request,'asubscription/add-subscription.html')
    def post(self,request,*args, **kwargs):
        context={}
        context['name']=request.POST['name']
        # context['duration_m']=request.POST['duration_m']
        # context['duration_y']=request.POST['duration_y']
        context['price_m']=request.POST['price_m']
        context['price_y']=request.POST['price_y']
        context['benefits']=request.POST['benefits']
        form=AddSubscriptionForm(data=request.POST or None,)
        if form.is_valid():
            # period_m=str(int(context['duration_m'])-1)
            # period_y=str(int(context['duration_y'])-1)
            sp = SubscriptionPlan(
                plan_name=context['name'],
                # period_m=context['duration_m'],
                price_m=context['price_m'],
                # period_y=context['duration_y'],
                price_y=context['price_y'],
                description=context['benefits'],
            )
            sp.save()
            message='Plan saved successfully'
            messages.add_message(request, messages.INFO, message)
            return render(request,'asubscription/add-subscription.html')
        return render(request,'asubscription/add-subscription.html',context={'con':context,'form':form})

class EditSubscriptionView(TemplateView):
    def get(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        con = SubscriptionPlan.objects.filter(id=id).first()
        # pb = PlanBenifits.objects.filter(plan=s).first()
        return render(request,'asubscription/subscription-edit.html',{'con':con})
    def post(self,request,*args, **kwargs):
        context={}
        context['id'] = self.kwargs['pk']
        context['plan_name']=request.POST['name']
        # context['period_m']=request.POST['duration_m']
        # context['period_y']=request.POST['duration_y']
        context['price_m']=request.POST['price_m']
        context['price_y']=request.POST['price_y']
        context['description']=request.POST['benefits']
        form=AddSubscriptionForm(data=request.POST or None,)
        if form.is_valid():
            # period_m=str(int(context['period_m'])-1)
            # period_y=str(int(context['duration_y'])-1)
            subp = SubscriptionPlan.objects.filter(id=context['id']).first()
            if subp:
                subp.plan_name=context['plan_name']
                # subp.period_m=context['period_m']
                subp.price_m=context['price_m']
                # subp.period_y=context['period_y']
                subp.price_y=context['price_y']
                subp.description=context['description']
                subp.save()
                message='Plan saved successfully'
                messages.add_message(request, messages.INFO, message)
                return HttpResponseRedirect('/admin_panel/subscription/view/'+str(context['id']))
            else:
                message='Invalid plan id'
            
        messages.add_message(request, messages.INFO, message)
        return render(request,'asubscription/subscription-edit.html',context={'con':context,'form':form})

class ViewSubscriptionView(TemplateView):
    def get(self,request,*args, **kwargs):
        id = self.kwargs['pk']
        s = SubscriptionPlan.objects.filter(id=id).first()
        # pb = PlanBenifits.objects.filter(plan=s).first()
        return render(request,'asubscription/view-subscription.html',{'s':s})

class ImportSubscriptionView(TemplateView):
    def post(self,request,*args,**kwargs):
        message=''
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        status = validate_excel(excel_data)
        if status!="1":
            messages.add_message(request, messages.INFO, status)
            return HttpResponseRedirect('/admin_panel/subscription/list')     
        counter=0
        for row_data in excel_data:
            counter+=1
            if counter!=1:
                ach = SubscriptionPlan(
                    plan_name=row_data[0],
                    # period_m=row_data[1],
                    # period_y=row_data[2],
                    price_m=row_data[3],
                    price_y=row_data[4],
                    description=row_data[5],
                )
                ach.save()
                message='Data saved successfully'
        messages.add_message(request, messages.INFO, message)
        return HttpResponseRedirect('/admin_panel/subscription/list')  

def validate_excel(excel_data):
    counter=0
    less_id_list=[]
    if len(excel_data[0])<3:
        return 'Please use proper excel file format'
    for row_data in excel_data:
        counter += 1
        name=row_data[0]
        price_m=row_data[1]
        price_y=row_data[2]
        benefits=row_data[3]
        # duration_m=row_data[1]
        # duration_y=row_data[2]
        # price_m=row_data[3]
        # price_y=row_data[4]
        # benefits=row_data[5]
        # if counter==1:
        #     if (name!='Name' or duration_m!='Duration(Monthly)' 
        #         or duration_y!='Duration(Yearly)' or price_m!='Price(Monthly)' 
        #         or price_y!='Price(Yearly)' or benefits!='Benefits'):
        #         return 'Please use proper excel file format'
        if counter==1:
            if (name!='Name' or price_m!='Price(Monthly)' 
                or price_y!='Price(Yearly)' or benefits!='Benefits'):
                return 'Please use proper excel file format'
        else:
            if not name or name=="":
                return 'Please provide name at row '+str(counter)
            # if not duration_m or duration_m=="":
            #     return 'Please provide duration(monthly) '+str(counter)
            # if not duration_y or duration_y=="":
            #     return 'Please provide duration(yearly) '+str(counter)
            if not price_m or price_m=="":
                return 'Please provide price(monthly) at row '+str(counter)
            if not price_y or price_y=="":
                return 'Please provide price(yearly) '+str(counter)
            if not benefits or benefits=="":
                return 'Please provide benefits '+str(benefits)

            if len(name)>40:
                return "Name length is exceeding at row "+str(counter)
            # if len(duration_m)>10:
            #     return "Duration(monthly) length is exceeding at row "+str(counter)
            # if len(duration_m)>10:
            #     return "Duration(yearly) is exceeding at row "+str(counter)
            if len(price_m)>10:
                return "Price(monthly) length is exceeding at row "+str(counter)
            if len(price_y)>10:
                return "Price(yearly) is exceeding at row "+str(counter)
            if len(benefits)>900:
                return "Benefits length is exceeding at row "+str(counter)
            
            p1 = price_m.split('.')
            if len(p1)>2:
                return 'Price(monthly) is invalid at row '+str(counter)
            if not p1[0].isdigit():
                return 'Price(monthly) is invalid at row '+str(counter)
            if len(p1)==2 and (not p1[1].isdigit()):
                return 'Price(monthly) is invalid at row '+str(counter)

            p2 = price_y.split('.')
            if len(p2)>2:
                return 'Price(yearly) is invalid at row '+str(counter)
            if not p2[0].isdigit():
                return 'Price(yearly) is invalid at row '+str(counter)
            if len(p2)==2 and (not p2[1].isdigit()):
                return 'Price(yearly) is invalid at row '+str(counter)

            # if duration_m not in ['1','2','3','4','5','6','7','8','9','10','11']:
            #     return 'Duration(monthly) is not valid at row '+str(counter)
            # if duration_y not in ['1','2','3','4','5']:
            #      return 'Duration(yearly) is not valid at row '+str(counter)

    if counter in (0,1):
        return "Excel file is empty"
    return "1"