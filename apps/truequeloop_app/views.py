from asgiref.sync import async_to_sync
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import RegisterUserForm, CreateTradeForm, TradeImagesForm, UserUpdateForm, ProfilePicForm, EditTradeForm, \
    CommunityRequestForm, CreateCommunityForm, EditCommunityForm
from .models import Location, Community, Trade, TradeImages, Profile, OpenChat, Message, CommunityRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import JsonResponse
import json


# Create your views here.

def home_screen_view(request):
    all_communities = Community.objects.all
    return render(request, "index.html", {'communities': all_communities})  # {} DB variables pasar


def community_screen_view(request, id):
    all_locations = Location.objects.all
    community = Community.objects.get(id=id)
    n_trades = Trade.objects.filter(community=community, status='ACTIVE').count()
    community_trades = Trade.objects.filter(community_id=id)  # Tener en cuenta estados de los trueques
    return render(request, "community.html",
                  {'locations': all_locations, 'community': community, 'trades': community_trades,
                   'n_trades': n_trades})  # {} DB variables pasar


def login_screen_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "Usuario o contraseña erróneos, inténtelo de nuevo.")
            return redirect('login')
    else:
        return render(request, "login.html", {})  # {} DB variables pasar


def register_screen_view(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.get(username=username)
            profile = Profile(user=user)
            profile.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registrado correctamente!")
            return redirect('home')
        else:
            return render(request, "register.html", {'form': form})

    else:
        form = RegisterUserForm()

    return render(request, "register.html")  # {} DB variables pasar


def trade_screen_view(request, id):
    trade = Trade.objects.get(id=id)
    trade_images = TradeImages.objects.filter(trade_id=id)
    user_trade = User.objects.get(id=trade.user_id)
    profile_trade = Profile.objects.get(user_id=trade.user_id)

    return render(request, "trade.html", {'trade': trade,
                                          'trade_images': trade_images,
                                          'user_trade': user_trade,
                                          'profile_trade': profile_trade}
                  )


def profile_screen_view(request):
    print(request.headers)
    return render(request, "profile.html", {})  # {} DB variables pasar


# Función auxiliar
def get_community(name):
    return Community.objects.get(name=name)


# Función auxiliar
def get_location(location):
    return Location.objects.get(location=location)


# Función auxiliar
def get_profile(user_id):
    return Profile.objects.get(user_id=user_id)


@login_required
def create_trade_screen_view(request):
    if request.method == 'POST':

        form = CreateTradeForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")

        if form.is_valid():
            trade = form.save(commit=False)
            trade.user_id = request.user.id
            trade.location = get_location(location=request.POST.get("location"))
            trade.community = get_community(request.POST.get("community"))
            trade.save()

            for image in files:
                TradeImages.objects.create(
                    image=image,
                    trade=trade
                )

            messages.success(request, 'El trueque se ha creado correctamente.')

            return trade_screen_view(request, trade.id)
        else:
            all_locations = Location.objects.all
            all_communities = Community.objects.all
            return render(request, "create-trade.html",
                          {'locations': all_locations, 'communities': all_communities, 'form': form})

    all_locations = Location.objects.all
    all_communities = Community.objects.all

    return render(request, "create-trade.html",
                  {'locations': all_locations, 'communities': all_communities})  # {} DB variables pasar


@login_required()
def logout_user(request):
    logout(request)
    return redirect('home')


def user_chat_info_creation(request, open_chat):
    if open_chat.user1.username != request.user.username:
        user_chat_info = {
            'username': open_chat.user1.username,
            'last_login': open_chat.user1.last_login,
            'first_name': open_chat.user1.first_name,
            'last_name': open_chat.user1.last_name,
            'profile_pic': open_chat.user1.profile.profile_pic.url
        }
    else:
        user_chat_info = {
            'username': open_chat.user2.username,
            'last_login': open_chat.user2.last_login,
            'first_name': open_chat.user2.first_name,
            'last_name': open_chat.user2.last_name,
            'profile_pic': open_chat.user1.profile.profile_pic.url
        }
    return user_chat_info


@login_required
def chat_view(request, username):
    no_alert_messages = True
    user2 = User.objects.get(username=username)
    profile_chat = get_profile(user2.id)
    profile = get_profile(request.user.id)
    chat_exists1 = OpenChat.objects.filter(user1=request.user, user2=user2)
    chat_exists2 = OpenChat.objects.filter(user1=user2, user2=request.user)
    open_chats_filter = OpenChat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    open_chats = []

    for open_chat in open_chats_filter:
        if open_chat.user1.username != username and open_chat.user2.username != username:
            user_chat_info = user_chat_info_creation(request, open_chat)
            open_chats.append(user_chat_info)

    uuid = None
    messages_chat = None
    if not chat_exists1 and not chat_exists2:
        chat = OpenChat.objects.create(user1=request.user, user2=user2)
        chat.save()
        uuid = chat.uuid
    elif chat_exists1:
        uuid = chat_exists1.get().uuid
        messages_chat = Message.objects.filter(chat=chat_exists1.get())
    elif chat_exists2:
        uuid = chat_exists2.get().uuid
        messages_chat = Message.objects.filter(chat=chat_exists2.get())

    return render(request, 'chat.html', {'uuid': uuid, 'user_chat': user2, 'profile_chat': profile_chat,
                                         'profile': profile, 'messages': messages_chat, 'open_chats': open_chats,
                                         'no_alert_messages': no_alert_messages})


@login_required
def open_chats_screen_view(request):
    open_chats_filter = OpenChat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    open_chats = []
    for open_chat in open_chats_filter:
        user_chat_info = user_chat_info_creation(request, open_chat)
        open_chats.append(user_chat_info)

    return render(request, 'messages.html', {'open_chats': open_chats})


def render_profile(trades, request):
    return render(request, 'profile.html', {'trades': trades, 'n_trades': len(trades)})


@login_required
def profile_view(request):
    user_id = request.user.id
    trades = Trade.objects.filter(user_id=user_id)
    return render_profile(trades, request)


@login_required
def delete_trade(request, trade_id):
    trade = Trade.objects.get(id=trade_id)
    user_id = request.user.id
    trades = Trade.objects.filter(user_id=user_id)
    community = trade.community
    if request.user.id == trade.user_id:
        trade.delete()
        community.n_trades = Trade.objects.filter(community=community, status='ACTIVE').count()
        community.save()

    return render_profile(trades, request)


@login_required
@staff_member_required
def delete_trade_staff(request, trade_id):
    trade = Trade.objects.get(id=trade_id)
    community = trade.community
    trade.delete()
    community.n_trades = Trade.objects.filter(community=community, status='ACTIVE').count()
    community.save()

    return redirect('home')


@login_required
def delete_account(request, user_id):
    user = User.objects.get(id=user_id)
    trades = Trade.objects.filter(user_id=user.id)

    if request.user.id == user.id:
        logout(request)
        user.delete()
        return redirect('home')

    return render_profile(trades, request)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            user = form.save()
            profile = get_profile(user.id)
            profile_pic = ProfilePicForm(request.POST, request.FILES)
            if profile_pic.is_valid():
                profile_pic = profile_pic.clean_profile_pic()
                if profile_pic:
                    profile.profile_pic = profile_pic
                    profile.save()
            else:
                return render(request, 'edit-profile.html', {'form': form, 'form_profile_pic': profile_pic})

            return redirect('profile')
    else:
        form = UserChangeForm(instance=user)
        profile_pic = ProfilePicForm(request.FILES)

    return render(request, 'edit-profile.html', {'form': form, 'form_profile_pic': profile_pic})


# AUX -- refactor -- complexity reduced
def process_form_edit_trade(trade, form, request, files, images_to_delete):
    trade.description = form.cleaned_data['description']
    main_image = form.clean_main_image()
    if main_image:
        trade.main_image = main_image
    trade.interested = form.cleaned_data['interested']
    trade.status = form.cleaned_data['status']
    trade.title = form.cleaned_data['title']
    trade.location = get_location(location=request.POST.get("location"))
    trade.community = get_community(name=request.POST.get("community"))
    trade.save()

    for image in files:
        TradeImages.objects.create(
            image=image,
            trade=trade
        )
    images_to_delete[:] = (value for value in images_to_delete if value != '')
    # Borramos las imágenes seleccionadas
    if images_to_delete:
        for image_id in images_to_delete:
            image_instance = TradeImages.objects.get(id=image_id)
            image_instance.delete()

    return redirect('profile')


@login_required
def edit_trade(request, trade_id):
    trade = Trade.objects.get(id=trade_id)
    trade_images = TradeImages.objects.filter(trade_id=trade_id)

    if request.method == 'POST':

        form = EditTradeForm(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        images_to_delete = request.POST.get('images_to_delete', '').split(',')

        if form.is_valid():
            return process_form_edit_trade(trade, form, request, files, images_to_delete)
        else:
            all_locations = Location.objects.all
            all_communities = Community.objects.all
            return render(request, "edit-trade.html",
                          {'locations': all_locations, 'communities': all_communities, 'form': form, 'trade': trade,
                           'trade_images': trade_images})

    all_locations = Location.objects.all
    all_communities = Community.objects.all

    return render(request, 'edit-trade.html',
                  {'trade': trade, 'locations': all_locations, 'communities': all_communities,
                   'trade_images': trade_images})


@login_required
def community_request_screen_view(request):
    if request.method == 'POST':
        form = CommunityRequestForm(request.POST, request.FILES)

        if form.is_valid():
            community_request = form.save(commit=False)
            community_request.requester = request.user
            image = form.clean_suggested_image()
            if image:
                community_request.sug_image = image
            community_request.save()

            messages.success(request, "Solicitud creada con éxito.")
            return redirect('home')
        else:
            return render(request, "community-request.html", {'form': form})

    return render(request, 'community-request.html')


@login_required
@staff_member_required
def moderator_panel_screen_view(request):
    comunity_requests = CommunityRequest.objects.order_by('-created_at').all()

    return render(request, 'moderator-panel.html', {'comunity_requests': comunity_requests})


@login_required
@staff_member_required
def create_community_screen_view(request):
    if request.method == 'POST':
        form = CreateCommunityForm(request.POST, request.FILES)

        if form.is_valid():
            community = form.save(commit=False)
            community_image = form.clean_community_image()
            if community:
                community.community_image = community_image
            community.save()

            messages.success(request, "Comunidad creada con éxito.")
            return redirect('moderation')
        else:
            return render(request, "create-community.html", {'form': form})

    return render(request, 'create-community.html')


# manage_communities_screen_view, delete_community, edit_community
@login_required
@staff_member_required
def manage_communities_screen_view(request):
    all_communities = Community.objects.all
    return render(request, 'manage-communities.html', {'communities': all_communities})


@login_required
@staff_member_required
def delete_community(request, community_id):
    community = Community.objects.get(id=community_id)
    community.delete()

    all_communities = Community.objects.all
    return render(request, 'manage-communities.html', {'communities': all_communities})


@login_required
@staff_member_required
def edit_community(request, community_id):
    community = Community.objects.get(id=community_id)
    if request.method == 'POST':
        form = EditCommunityForm(request.POST, request.FILES)

        if form.is_valid():

            community.name = form.cleaned_data['name']
            community_image = form.clean_community_image()
            if community_image:
                community.community_image = community_image
            community.save()

            messages.success(request, "Comunidad editada con éxito.")
            return redirect('manage-communities')
        else:
            return render(request, "edit-community.html", {'form': form, 'community': community})

    return render(request, 'edit-community.html', {'community': community})


@login_required
@staff_member_required
def delete_request(request, request_id):
    community_req = CommunityRequest.objects.get(id=request_id)
    community_req.delete()

    comunity_requests = CommunityRequest.objects.order_by('-created_at').all()

    return render(request, 'moderator-panel.html', {'comunity_requests': comunity_requests})
