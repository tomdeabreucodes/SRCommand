from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class SrdcUser(models.Model):
    srdc_user = models.CharField(primary_key=True, max_length=8)
    srdc_user_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if len(SrdcUser.objects.all()) > 0:
            SrdcUser.objects.all().delete()
        super(SrdcUser, self).save(*args, **kwargs)


class Game(models.Model):
    game_code = models.CharField(primary_key=True, max_length=8)
    game_name = models.CharField(max_length=200)
    game_abbreviation = models.CharField(max_length=50)


class GameAliases(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_alias = models.CharField(max_length=50, unique=True)


class Category(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=200)
    category_code = models.CharField(max_length=8)
    category_type = models.CharField(max_length=20)
    category_level = models.CharField(max_length=50)
    players_type = models.CharField(max_length=10)
    players_value = models.IntegerField(default=1)
    miscellaneous = models.BooleanField(default=False)


class CategoryAliases(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_alias = models.CharField(max_length=50)


class VariableFilters(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    variable_code = models.CharField(max_length=8)
    variable_name = models.CharField(max_length=100)
    variable_value = models.CharField(max_length=8)
    variable_value_name = models.CharField(max_length=100)

    class Meta:
        unique_together = [['variable_code', 'category']]


@receiver(post_save, sender=Game)
def default_game_alias(sender, instance, **kwargs):
    model_instance = GameAliases(
        game_alias=instance.game_abbreviation,
        game=Game.objects.get(game_code=instance.game_code),
    )
    model_instance.save()


@receiver(post_save, sender=Category)
def default_category_alias(sender, instance, **kwargs):
    alias = instance.category_name.lower().replace(" ", "")
    alias_duplicate = CategoryAliases.objects.filter(
        category__category_code=instance.category_code, category_alias=alias).exists()
    alias_duplicate_game = CategoryAliases.objects.filter(
        category__game__game_code=instance.game.game_code, category_alias=alias).exists()
    if not alias_duplicate and not alias_duplicate_game:
        model_instance = CategoryAliases(
            category_alias=alias,
            category=Category.objects.get(id=instance.id),
        )
        model_instance.save()
