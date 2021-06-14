from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name='Nazwa')
    points = models.IntegerField(null=True, verbose_name='Punkty')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = ("Zespol")
        verbose_name_plural = ("Zespoly")


class Player(models.Model):
    name = models.CharField(max_length=50, null=True, verbose_name='Nazwa')
    surname = models.CharField(max_length=50, null=True, verbose_name='Nazwisko')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Imie')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Zespol')
    number = models.IntegerField(null=True, verbose_name='Numer')

    class Meta:
        verbose_name = ("Zawodnik")
        verbose_name_plural = ("Zawodnicy")

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Gospodarz')
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Gosc')
    home_score = models.IntegerField(null=True, verbose_name='Bramki_gosp')
    away_score = models.IntegerField(null=True, verbose_name='Bramki_gosc')

    class Meta:
        verbose_name = ("Mecz")
        verbose_name_plural = ("Mecze")

class Comment(models.Model):
    text = models.TextField(verbose_name='Tekst')
    date_created = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Data')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Uzytkownik')
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mecz')

    class Meta:
        ordering = ['date_created']
        verbose_name = ("Komentarz")
        verbose_name_plural = ("Komentarze")

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()

