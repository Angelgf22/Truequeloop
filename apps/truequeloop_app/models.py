import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings


class Location(models.Model):
    location = models.CharField(max_length=90, blank=True)

    def __str__(self):
        return self.location


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="./profiles/", default="profiles/default-user.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''
    # To add Validation and feedback stats for the user
    feedback = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    n_feedbacks = models.IntegerField(default=0)
    
    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(feedback__gte=0.0) & Q(feedback__lte=5.0),
                name='foo_feedback_range'),
        )
    '''


class Community(models.Model):
    name = models.CharField(max_length=255, null=False)
    n_trades = models.BigIntegerField(default=0)
    community_image = models.ImageField(upload_to='./communities', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Trade(models.Model):
    title = models.CharField(max_length=65, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(null=False, upload_to="./trades/")
    description = models.CharField(blank=True, max_length=1000)
    interested = models.CharField(blank=True, max_length=200)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=10, choices=[('ACTIVE', 'Activo'), ('INACTIVE', 'Inactivo')], default='ACTIVE')

    def __str__(self):
        return self.title


@receiver(post_save, sender=Trade)
def update_n_trades(sender, instance, **kwargs):
    community = instance.community
    active_trades = Trade.objects.filter(community=community, status='ACTIVE').count()
    community.n_trades = active_trades
    community.save()


class TradeImages(models.Model):
    image = models.ImageField(upload_to='./trades/', null=True, blank=True)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True)


class OpenChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_openchats')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_openchats')
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.user1.username} <-> {self.user2.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField()
    chat = models.ForeignKey(OpenChat, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content}"


class CommunityRequest(models.Model):
    community_name = models.TextField(null=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    community_description = models.TextField(null=False, max_length=1000)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    sug_image = models.ImageField(null=True, blank=True, upload_to="./communities")
    approved = models.BooleanField(null=True)


@receiver(pre_delete, sender=CommunityRequest)
def delete_image_community_request(sender, instance, **kwargs):
    if instance.sug_image:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.sug_image)))


@receiver(pre_delete, sender=TradeImages)
def delete_image_trade_images(sender, instance, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.image)))


@receiver(pre_delete, sender=Trade)
def delete_image_trade(sender, instance, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.main_image)))


@receiver(pre_delete, sender=Community)
def delete_image_community(sender, instance, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.community_image)))


@receiver(pre_delete, sender=Profile)
def delete_image_profile(sender, instance, **kwargs):
    if str(instance.imagen) != 'profiles/default-user.jpg':
        os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.profile_pic)))
