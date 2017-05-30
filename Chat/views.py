# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from .models import Messages
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForms
from django.contrib.auth.views import logout

def signin(request):

    if request.POST.get('action') == 'login':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('Chat:contacts'))
        context = {'Message': 'Either the username or the password is wrong '}
        return render(request,'Chat/login.html',context)

    elif request.POST.get('action') == 'signup':
        return HttpResponseRedirect(reverse('Chat:signup'))
    return render(request, 'Chat/login.html')

def signup(request):
    if request.POST.get('action') == 'signup':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        try:
            User.objects.get(username=username)
            context = {'Message': 'username already taken chose another username '}
            return render(request, 'Chat/signup.html', context)

        except User.DoesNotExist:
            if password == password2:
                user = User.objects.create_user(username=username, password=password, first_name =firstname, last_name=lastname)
                user.save()
                return HttpResponseRedirect(reverse('Chat:contacts'))
            else:
                context = {'Message': 'password not the same '}
                return render(request, 'Chat/signup.html', context)

    return render(request,'Chat/signup.html')

def contacts(request):

    if request.POST.get('action') == 'leave':
        logout(request,request.user)
        return HttpResponseRedirect(reverse('Chat:signin'))

    users = User.objects.all().values('username')
    userslist = []
    for user in users:
        if user['username'] != 'admin' and user['username'] != request.user.username:
            userslist.append(user['username'])
    context = {'userslist': userslist}
    return render(request, 'Chat/contacts.html', context)

def chating(request):
    if request.POST.get('action') == 'back':
        return HttpResponseRedirect(reverse('Chat:contacts'))

    elif request.POST.get('action') == 'leave':
        logout(request,request.user)
        return HttpResponseRedirect(reverse('Chat:signin'))


    message = request.POST.get('message')
    nameuser = request.POST.get('nameuser')
    _user = request.user.username
    sentMessages = Messages.objects.filter(receiver=nameuser, sender=_user)
    receivedMessages = Messages.objects.filter(receiver=_user, sender=nameuser)

    sentMessages.order_by("id")
    receivedMessages.order_by("id")
    count1 = sentMessages.count()
    count2 = receivedMessages.count()
    sum1 = 0
    sum2 = 0
    totalMessage = []
    print(count1)
    print(count2)

    while sum1!=count1 and sum2!=count2:
        if sentMessages[sum1].id <= receivedMessages[sum2].id:
            totalMessage.append(sentMessages[sum1])
            sum1 += 1
        elif sentMessages[sum1].id >= receivedMessages[sum2].id:
            totalMessage.append(receivedMessages[sum2])
            sum2 += 1
    if sum1<count1:
        for x in range(sum1,count1,1):
            totalMessage.append(sentMessages[x])
    elif sum2<count2:
        for x in range(sum2,count2,1):
            totalMessage.append(receivedMessages[x])
    print(len(totalMessage))
    for x in range(len(totalMessage)):
        print(totalMessage[x].sender)
        print(totalMessage[x].message_text)

    if message:
        message = Messages(sender=request.user.username, receiver=nameuser, sent_date=timezone.now(), message_text=message)
        message.save()
    context = {'nameuser': nameuser, 'allmessages':totalMessage}
    return render(request,'Chat/chatWindow.html',context)

#
#class UserFormViews(View):
#    form_class = UserForms
#    template_name = 'Chats/login.html'
#
#    def get(self,request):
#        form = self.form_class(None)
#        return render(request,self.template_name, {'form': form})
#
#    def post(self,request):
#        form = self.form_class(request.POST)
#        if form.is_valid():
#            user = form.save(commit=false)
#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            user.set_password(password)
#            user.save()
#
#            user = authenticate(username=username, password=password)
#            if user is not None:
#                if user.is_active:
#                    login(request,user)
#                    return redirect('Chat:chat')
#        return render(request,self.template_name, {'form': form})
#
#def 
