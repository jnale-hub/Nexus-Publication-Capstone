from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from nexus_pub.models import User

def games(request):
    return render(request, "games/games.html", {"games": True})

def wordle(request):
    user = request.user
    wordle_data = user
    games_played = wordle_data
    games_won = wordle_data
    
    percentage_wins = 0

    return render(request, "games/wordle.html", {
        'games_played': games_played,
        'games_won': games_won,
        'percentage_wins': percentage_wins,
    })

@csrf_exempt
@login_required
def update_points(request):
    if request.method == "POST":
        user = request.user
        user.points += 1
        user.save()
        return JsonResponse({
            "success": True,
            "points": user.points,
        })
    return JsonResponse({"success": False})