from datetime import datetime, timedelta
from django.db import IntegrityError
from django.shortcuts import render
from django.utils import timezone
from config.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
import requests
from .forms import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAdminUser])
def user(request):
    curr_user = SrdcUser.objects.first()
    user_form = SrdcUserForm(request.GET)
    users = list()
    if user_form.is_valid() and user_form.cleaned_data.get("srdc_username"):
        username = user_form.cleaned_data.get("srdc_username")
        url = "https://www.speedrun.com/api/v1/users?name=" + username
        data = requests.get(url).json()["data"][:10]
        for i in range(0, len(data)):
            user = data[i]
            users.append(user)
    return render(request, "user.html", {'user_form': user_form, 'users': users, 'curr_user': curr_user})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def setuser(request):
    try:
        model_instance = SrdcUser(
            srdc_user=request.data.get("my_user"),
            srdc_user_name=request.data.get("my_user_name")
        )
        model_instance.save()
    except IntegrityError:
        pass
    if len(request.data.get("query")) > 0:
        return HttpResponseRedirect("/config/user/" + "?srdc_username=" + request.data.get("query"))
    else:
        return HttpResponseRedirect("/config/user/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def index(request):
    srdcgames = list()
    mygames = Game.objects.all()
    aliases = GameAliases.objects.all()
    alias_form = GameAlias(request.GET)
    game_form = GameForm(request.GET)
    url = "https://www.speedrun.com/api/v1/games"
    if game_form.is_valid() and game_form.cleaned_data.get("game_name"):
        url += "?name=" + game_form.cleaned_data.get("game_name")
        data = requests.get(url).json()["data"][:10]
        for i in range(0, len(data)):
            srdcgame = data[i]
            srdcgame["assets"]["cover_tiny"] = srdcgame["assets"].pop(
                "cover-tiny")
            srdcgames.append(srdcgame)

    return render(request, "games.html", {'srdcgames': srdcgames, 'mygames': mygames, 'aliases': aliases, 'game_form': game_form, 'alias_form': alias_form})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def addgame(request):
    try:
        model_instance = Game(
            game_code=request.data.get("game_code"),
            game_name=request.data.get("game_name"),
            game_abbreviation=request.data.get("game_abbreviation"),
        )
        model_instance.save()
    except IntegrityError:
        pass
    if len(request.data.get("query")) > 0:
        return HttpResponseRedirect("/config/" + "?game_name=" + request.data.get("query"))
    else:
        return HttpResponseRedirect("/config/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def deletegame(request):
    model_instance = Game.objects.get(game_code=request.GET.get("game_code"))
    model_instance.delete()
    if len(request.GET.get("query")) > 0:
        return HttpResponseRedirect("/config/" + "?game_name=" + request.GET.get("query"))
    else:
        return HttpResponseRedirect("/config/")


@api_view(["POST"])
@permission_classes([IsAdminUser])
def addalias(request):
    try:
        model_instance = GameAliases(
            game_alias=request.data.get("game_alias").lower(),
            game=Game.objects.get(game_code=request.data.get("game")),
        )
        model_instance.save()

    except IntegrityError:
        pass

    if len(request.data.get("query")) > 0:
        return HttpResponseRedirect("/config/" + "?game_name=" + request.data.get("query"))
    else:
        return HttpResponseRedirect("/config/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def deletealias(request):
    model_instance = GameAliases.objects.filter(
        game=Game(game_code=request.GET.get("game_code")))
    model_instance.delete()
    if len(request.GET.get("query")) > 0:
        return HttpResponseRedirect("/config/" + "?game_name=" + request.GET.get("query"))
    else:
        return HttpResponseRedirect("/config/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def categories(request, game_code):
    mycategories = Category.objects.all()
    srdccategories = list()
    srdclevels = list()
    mygame = Game.objects.get(game_code=game_code)
    aliases = CategoryAliases.objects.all()
    alias_form = CategoryAlias(request.GET)
    # level_form = Level(request.GET)
    url = "https://www.speedrun.com/api/v1/games/" + mygame.game_code + "/categories"
    data = requests.get(url).json()["data"]
    for i in range(0, len(data)):
        srdcategory = data[i]
        srdccategories.append(srdcategory)
    url = "https://www.speedrun.com/api/v1/games/" + mygame.game_code + "/levels"
    data = requests.get(url).json()["data"]
    for i in range(0, len(data)):
        srdclevel = data[i]
        srdclevels.append(srdclevel)
    return render(request, "categories.html", {'mygame': mygame, 'srdccategories': srdccategories, 'srdclevels': srdclevels,
                                               'mycategories': mycategories, 'aliases': aliases, 'alias_form': alias_form})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def addcategory(request, game_code):
    try:
        model_instance = Category(
            game=Game.objects.get(game_code=game_code),
            category_code=request.data.get("category_code"),
            category_name=request.data.get("category_name"),
            category_type=request.data.get("category_type"),
            category_level=request.data.get("category_level"),
            players_type=request.data.get("players_type"),
            players_value=request.data.get("players_value"),
            miscellaneous=request.data.get("miscellaneous"),
        )
        model_instance.save()
    except IntegrityError:
        pass

    return HttpResponseRedirect("/config/" + game_code + "/categories/")


@api_view(["POST"])
@permission_classes([IsAdminUser])
def addcategoryalias(request, game_code):
    try:
        alias_duplicate = CategoryAliases.objects.filter(
            category__category_code=request.data.get("category_code"), category_alias=request.data.get("category_alias").lower()).exists()
        alias_duplicate_game = CategoryAliases.objects.filter(
            category__game__game_code=game_code, category_alias=request.data.get("category_alias").lower()).exists()
        if not alias_duplicate and not alias_duplicate_game:
            model_instance = CategoryAliases(
                category_alias=request.data.get("category_alias").lower(),
                category=Category.objects.get(
                    id=request.data.get("category")),
            )
            model_instance.save()

    except IntegrityError:
        pass

    return HttpResponseRedirect("/config/" + game_code + "/categories/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def deletecategory(request, game_code):
    model_instance = Category.objects.get(
        id=request.GET.get("category"))
    model_instance.delete()
    return HttpResponseRedirect("/config/" + game_code + "/categories/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def deletecategoryalias(request, game_code):
    model_instance = CategoryAliases.objects.filter(
        category=Category(id=request.GET.get("category")))
    model_instance.delete()
    return HttpResponseRedirect("/config/" + game_code + "/categories/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def changelevel(request, game_code):
    model_instance = Category.objects.get(
        id=request.GET.get("category"))
    model_instance.category_level = request.GET.get("level")
    model_instance.save()
    return HttpResponseRedirect("/config/" + game_code + "/categories/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def variables(request, game_code, category):
    mygame = Game.objects.get(game_code=game_code)
    mycategory = Category.objects.get(id=category)
    myvariables = VariableFilters.objects.filter(category=category)
    srdcvariables = list()
    url = "https://www.speedrun.com/api/v1/categories/" + \
        mycategory.category_code + "/variables"
    data = requests.get(url).json()["data"]
    for i in range(0, len(data)):
        srdcvariable = data[i]
        srdcvariables.append(srdcvariable)
    return render(request, "variables.html", {'mygame': mygame, 'mycategory': mycategory, 'myvariables': myvariables, 'srdcvariables': srdcvariables})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def addfilter(request, game_code, category):
    try:
        if not request.data.get("variable_value"):
            messages.warning(
                request, "Must select an option to apply the filter.")
            return HttpResponseRedirect("/config/" + game_code + "/categories/" + category + "/filter/")
        name = request.data.get("variable_value").split(",")[1]
        value = request.data.get("variable_value").split(",")[0]
        model_instance = VariableFilters(
            category=Category(id=category),
            variable_code=request.data.get("variable_code"),
            variable_name=request.data.get("variable_name"),
            variable_value=value,
            variable_value_name=name
        )
        model_instance.save()
    except IntegrityError:
        messages.warning(
            request, "Filter already applied to this variable, please remove the current filter, or add another category entry to have another filter with this type.")

    return HttpResponseRedirect("/config/" + game_code + "/categories/" + category + "/filter/")


@api_view(["GET"])
@permission_classes([IsAdminUser])
def deletefilter(request, game_code, category):
    model_instance = VariableFilters.objects.get(
        id=request.GET.get("id"), category=category)
    model_instance.delete()
    return HttpResponseRedirect("/config/" + game_code + "/categories/" + category + "/filter/")


class VariableNotMatching(Exception):
    pass


class LevelNotMatching(Exception):
    pass


@api_view(["GET"])
def srdcrequest(request, game_code, category_code, srdc_guest=None):
    if srdc_guest:
        url = "https://www.speedrun.com/api/v1/users?name=" + srdc_guest
        response = requests.get(url).json()["data"][0]
        user_id = response["id"]
        guest_name = response["names"]["international"]
    else:
        user = SrdcUser.objects.first()
        user_id = user.srdc_user
        user_name = user.srdc_user_name
    try:
        srdc_game = GameAliases.objects.get(
            game_alias=game_code.lower()).game
        srdc_game_code = srdc_game.game_code
    except ObjectDoesNotExist:
        return HttpResponse("Game code not found.", status.HTTP_404_NOT_FOUND)
    try:
        srdc_category = CategoryAliases.objects.get(
            category_alias=category_code.lower(), category__game__game_code=srdc_game_code).category
        srdc_category_code = srdc_category.category_code
        srdc_category_name = srdc_category.category_name
        srdc_level = srdc_category.category_level if srdc_category.category_type == "per-level" else None
    except ObjectDoesNotExist:
        return HttpResponse("Category code not found.", status.HTTP_404_NOT_FOUND)

    url = "https://www.speedrun.com/api/v1/users/" + \
        user_id + "/personal-bests?game=" + srdc_game_code
    pbs = requests.get(url).json()["data"]

    name = guest_name if srdc_guest else user_name

    if len(pbs) < 1:
        return HttpResponse("{} has no PBs in this game.".format(name), status.HTTP_400_BAD_REQUEST)

    variables = VariableFilters.objects.filter(
        category=srdc_category)

    for pb in pbs:
        try:
            if pb["run"]["category"] == srdc_category_code:
                if len(variables) > 0:
                    for v in variables:
                        if pb["run"]["values"][v.variable_code] != v.variable_value:
                            raise VariableNotMatching
                if srdc_level:
                    if pb["run"]["level"] != srdc_level:
                        raise LevelNotMatching

                # Get PB info
                place = pb['place']
                seconds_input = pb["run"]['times']["primary_t"]
                time = str(timedelta(seconds=seconds_input))[:-3] if str(timedelta(
                    seconds=seconds_input))[-7] == '.' else str(timedelta(seconds=seconds_input))
                link = pb["run"]['weblink']
                return HttpResponse("{} has a PB of {} (#{}) in {} {} {}".format(name, time, str(place), game_code, category_code, link), status.HTTP_200_OK)
        except (VariableNotMatching, LevelNotMatching):
            continue
    return HttpResponse("{} has no PBs in this category.".format(name), status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def multisrdcrequest(request, game_code):
    user = SrdcUser.objects.first()
    user_id = user.srdc_user
    user_name = user.srdc_user_name
    try:
        srdc_game = GameAliases.objects.get(
            game_alias=game_code.lower()).game
        srdc_game_code = srdc_game.game_code
    except ObjectDoesNotExist:
        return HttpResponse("Game code not found.", status.HTTP_404_NOT_FOUND)
    categories = Category.objects.filter(
        game=GameAliases.objects.get(game_alias=game_code.lower()).game)

    url = "https://www.speedrun.com/api/v1/users/" + \
        user_id + "/personal-bests?game=" + srdc_game_code
    pbs = requests.get(url).json()["data"]

    category_codes = {c.category_code: c.category_name for c in categories}

    records = list()

    for pb in pbs:
        if pb["run"]["category"] in list(category_codes.keys()):

            # Get PB info
            place = pb['place']
            seconds_input = pb["run"]['times']["primary_t"]
            time = str(timedelta(seconds=seconds_input))[:-3] if str(timedelta(
                seconds=seconds_input))[-7] == '.' else str(timedelta(seconds=seconds_input))
            link = pb["run"]['weblink']
            desc = "{} #{} in {}".format(
                time, str(place), category_codes[pb["run"]["category"]])

            if pb["run"]["level"]:
                url = "https://www.speedrun.com/api/v1/levels/" + \
                    pb["run"]["level"]
                response = requests.get(url).json()["data"]
                desc = desc + " " + response["name"]

            variables = pb["run"]["values"]
            var_keys = list(variables.keys())
            if len(variables) > 0:
                var_desc = list()
                for v in var_keys:
                    var_url = "https://www.speedrun.com/api/v1/variables/" + v
                    response = requests.get(var_url).json()["data"]
                    var_desc.append(response["values"]
                                    ["values"][variables[v]]["label"])

                var_desc = " (" + ", ".join(var_desc) + ")"
                desc = desc + var_desc
            records.append(desc)

    if len(records) > 0:
        return HttpResponse("; ".join(records), status.HTTP_200_OK)
    else:
        return HttpResponse("No PBs found in this game", status.HTTP_404_NOT_FOUND)


@ api_view(["GET"])
def about(request):
    games = Game.objects.all()
    game_aliases = GameAliases.objects.all()
    categories = Category.objects.all()
    category_aliases = CategoryAliases.objects.all()

    return render(request, "about.html", {'games': games, 'game_aliases': game_aliases, 'categories': categories, 'category_aliases': category_aliases})


@ api_view(["GET"])
def helpmsg(request):
    host = request.get_host()
    msg = "Command usage instructions + guide to get these commands on your channel: {}".format(
        request.scheme + "://" + host + "/about")
    return HttpResponse(msg, status.HTTP_200_OK)


@ api_view(["GET"])
def help(request):
    aliases = [a.game_alias for a in GameAliases.objects.all()]
    aliases_string = "; ".join(aliases)
    c_aliases = [a.category_alias for a in CategoryAliases.objects.all()]
    c_aliases_string = "; ".join(set(c_aliases))
    response = "Command: !pb game_alias [category_alias] [srdc_username]" + \
        " | Games: " + aliases_string + " | Categories: " + c_aliases_string
    return HttpResponse(response, status.HTTP_200_OK)
