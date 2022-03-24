from django.contrib.auth.models import User
from django.db import models

from django.utils.safestring import mark_safe

from userdashboard.choices import USER_POST_CHOICES, LOOKING_FOR_CHOICES, MOVE_IN_CHOICES, HOUSING_TYPE_CHOICES


class UserRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    university = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class UserPosts(models.Model):
    user_reg = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True, choices=USER_POST_CHOICES, default='AVAILABLE')
    looking_for = models.CharField(max_length=20, choices=LOOKING_FOR_CHOICES, null=True, blank=True)
    move_in = models.CharField(max_length=20, choices=MOVE_IN_CHOICES, null=True, blank=True)
    housing_type = models.CharField(max_length=12, choices=HOUSING_TYPE_CHOICES, null=True, blank=True)
    date = models.DateField()
    no_of_bedrooms = models.IntegerField(null=True, blank=True)
    no_of_bathrooms = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user_reg.user.username


class ImageModel(models.Model):
    main_image = models.ImageField(upload_to='images/', null=True)
    image = models.ForeignKey(UserPosts, on_delete=models.CASCADE)

    def image_tag(self):
        if self.main_image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.main_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f'ID: {self.image.id} {self.image.user_reg.user.username} is looking for {self.image.looking_for}'

    def save(self, *args, **kwargs):
        try:
            this = ImageModel.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)


class UserContacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    contacted_for = models.ForeignKey(UserPosts, on_delete=models.CASCADE)

    def __str__(self):
        return f'contacted {self.contacted_for.user_reg.user.username} for {self.contacted_for.looking_for}'
