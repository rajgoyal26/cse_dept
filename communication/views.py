from django.shortcuts import render, redirect
from .forms import MessageForm, GroupForm,NotificationForm
from .models import Message, Block, Group
from django.contrib import messages
from django.contrib.auth.models import User
from student.models import Student
from student.models import Profile
from .filters import UserFilter
import json
from django.http import HttpResponse

# Create your views here.


def send(request):
    if request.method == 'POST':
        receiver_id = request.POST['receiver_id']
        receiver_list = receiver_id.split(',')
        sender = request.user
        for instance in receiver_list:
            print(instance)
            if 'GP' in instance:
                group = Group.objects.get(group_id=instance)
                receiver_list = group.group_list.split(',')
                print(receiver_list)
                for receiver in receiver_list:
                    message_form = MessageForm(request.POST, request.FILES)
                    if message_form.is_valid():
                        form = message_form.save(commit=False)
                        form.receiver_group = group
                        form.receiver = User.objects.get(id=receiver)
                        form.sender = sender
                        form.save()
            else:
                message_form = MessageForm(request.POST, request.FILES)
                if message_form.is_valid():
                    form = message_form.save(commit=False)
                    form.receiver = User.objects.get(id=instance)
                    form.sender = sender
                    form.save()

        return HttpResponse('Your message has been sent successfully')

    else:
        form = MessageForm()
        receiver = User.objects.raw('select id,username,first_name,last_name from auth_user')
        context = {'form': form, 'receiver': receiver}
        return render(request, 'communication/send.html', context)



def receive(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(first_name__icontains=q)
        groups = Group.objects.filter(group_name__icontains=q)
        results = []
        for i in users:
            users_json = {}
            users_json['label'] = i.first_name + " " + i.last_name
            users_json['value'] = i.first_name + " " + i.last_name
            users_json['id'] = i.id
            results.append(users_json)
        for i in groups:
            users_json = {}
            users_json['label'] = i.group_name
            users_json['value'] = i.group_list
            users_json['id'] = i.group_id
            results.append(users_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def read(request):
    receiver = request.user.id
    message = Message.objects.raw("Select * from communication_message where receiver_id = %s group by sender_id", [receiver])
    return render(request, 'communication/receive.html', {'form': message})


def read_view(request, pk):
    receiver = request.user.id
    message = Message.objects.raw("Select * from communication_message where sender_id = %s and receiver_id=%s order by date desc",
                                  [pk, receiver])
    return render(request, 'communication/read_view.html', {'form': message, 'sender': pk})


def block(request, pk):
    sender = User.objects.get(id=pk)
    Block.objects.create(receiver=request.user, sender=sender)
    return redirect('communication:read')


def unblock(request, pk):
    receiver = request.user.id
    Block.objects.filter(sender=pk, receiver=receiver).delete()
    return redirect('communication:read')


def create_group(request):

    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        user_list = request.POST['receiver_id']
        print(group_form.errors.as_data())
        if group_form.is_valid():
            form = group_form.save(commit=False)
            form.created_by = request.user
            form.save()
            form = group_form.save(commit=False)
            form.group_id = "GP"+str(form.id)
            form.group_list = str(user_list)
            form.save()
            return redirect('message:send')
        return HttpResponse('Form Invalid')

    else:
        form = GroupForm()
        return render(request, 'communication/group.html', {'form': form})


def notificationCreate(request):
    if request.method=="POST":
        notification_form=NotificationForm(request.POST,request.FILES)
        if notification_form.is_valid():
            form=notification_form.save(commit=False)
            form.created_by=str(request.user.first_name+" "+request.user.last_name)
            form.save()
            return HttpResponse("Your Notification has been Created Successfully")
        return render(request,'communication/create_notification.html',{'form':notification_form})
    else:
        form=NotificationForm()
        return render(request, 'communication/create_notification.html', {'form':form})