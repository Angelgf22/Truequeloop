from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from PIL import Image

from .models import Trade, TradeImages, Location, Community, Profile, CommunityRequest


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CreateTradeForm(forms.ModelForm):
    title = forms.CharField(max_length=65, required=True)
    description = forms.CharField(max_length=1000)
    interested = forms.CharField(max_length=200)
    location = forms.CharField(max_length=60)
    community = forms.CharField(max_length=65)
    main_image = forms.ImageField(required=True)

    def clean_location(self):
        value = self.cleaned_data.get('location')
        if not Location.objects.filter(location=value).exists():
            raise forms.ValidationError("Esta localización no existe o no está disponible.")
        return value

    def clean_community(self):
        value = self.cleaned_data.get('community')
        if not Community.objects.filter(name=value).exists():
            raise forms.ValidationError("Esta comunidad no existe o no está disponible.")
        return value

    class Meta:
        model = Trade
        fields = ('title', 'description', 'interested', 'main_image')


class EditTradeForm(forms.ModelForm):
    title = forms.CharField(max_length=65, required=True)
    description = forms.CharField(max_length=1000)
    interested = forms.CharField(max_length=200)
    location = forms.CharField(max_length=60)
    community = forms.CharField(max_length=65)
    main_image = forms.ImageField(required=False)

    def clean_location(self):
        value = self.cleaned_data.get('location')
        if not Location.objects.filter(location=value).exists():
            raise forms.ValidationError("Esta localización no existe o no está disponible.")
        return value

    def clean_community(self):
        value = self.cleaned_data.get('community')
        if not Community.objects.filter(name=value).exists():
            raise forms.ValidationError("Esta comunidad no existe o no está disponible.")
        return value

    class Meta:
        model = Trade
        fields = ('title', 'description', 'interested', 'main_image', 'status')

    def clean_main_image(self):
        main_image = self.cleaned_data.get('main_image', False)
        if main_image:
            try:
                img = Image.open(main_image)
                img.verify()
                if main_image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("La imagen es demasiado grande (máximo 2 MB).")
            except Exception:
                raise forms.ValidationError("El archivo no es una imagen válida.")

        return main_image


class TradeImagesForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = TradeImages
        fields = ('image',)


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


class ProfilePicForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('profile_pic',)

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic', False)
        if profile_pic:
            try:
                img = Image.open(profile_pic)
                img.verify()
                if profile_pic.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("La imagen es demasiado grande (máximo 2 MB).")
            except Exception:
                raise forms.ValidationError("El archivo no es una imagen válida.")

        return profile_pic


class CommunityRequestForm(forms.ModelForm):
    sug_image = forms.ImageField(required=False)

    class Meta:
        model = CommunityRequest
        fields = ('community_name', 'community_description', 'sug_image',)

    def clean_suggested_image(self):
        sug_image = self.cleaned_data.get('sug_image', False)
        if sug_image:
            try:
                img = Image.open(sug_image)
                img.verify()
                if sug_image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("La imagen es demasiado grande (máximo 2 MB).")
            except Exception:
                raise forms.ValidationError("El archivo no es una imagen válida.")

        return sug_image


class CommunityFormBase(forms.ModelForm):
    community_image = forms.ImageField(required=False)

    class Meta:
        model = Community
        fields = ('name', 'community_image')

    def clean_community_image(self):
        community_image = self.cleaned_data.get('community_image', False)
        if community_image:
            try:
                img = Image.open(community_image)
                img.verify()
                if community_image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError("La imagen es demasiado grande (máximo 2 MB).")
            except Exception:
                raise forms.ValidationError("El archivo no es una imagen válida.")

        return community_image


class CreateCommunityForm(CommunityFormBase):
    community_image = forms.ImageField(required=True)


class EditCommunityForm(CommunityFormBase):
    pass
