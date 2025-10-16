from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login

from scraping import profile_info
from database import Database

db = Database()
db.create_table()

def home(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if not username:
            context["error"] = "Digite um nome de usuário válido."
            return render(request, "blog/home.html", context)

        try:
            profile_data = profile_info(username)
        except Exception as e:
            context["error"] = str(e)
            return render(request, "blog/home.html", context)

        followers = profile_data.get("followers", 0)
        following = profile_data.get("following", 0)
        bio = profile_data.get("bio", "")
        profile_pic_path = profile_data.get("profile_pic_path")

        old_user = db.get_user(username)
        db.add_or_update_user(username, followers, following)

        followers_message = ""
        following_message = ""

        if old_user:
            diff = db.compare_user(username, followers, following)
            if diff["diff_followers"] > 0:
                followers_message = f"+{diff['diff_followers']} seguidores"
            elif diff["diff_followers"] < 0:
                followers_message = f"{abs(diff['diff_followers'])} seguidores a menos"
            else:
                followers_message = "Seguidores sem mudança"

            if diff["diff_following"] > 0:
                following_message = f"+{diff['diff_following']} seguindo"
            elif diff["diff_following"] < 0:
                following_message = f"{abs(diff['diff_following'])} seguindo a menos"
            else:
                following_message = "Seguindo sem mudança"
        else:
            followers_message = "Novo usuário cadastrado!"
            following_message = ""

        context.update({
            "username": username,
            "profile_pic_path": profile_pic_path,
            "followers": followers,
            "following": following,
            "bio": bio,
            "followers_message": followers_message,
            "following_message": following_message,
            "history": db.list_users(limit=6),
            "now": timezone.now(),
        })

    else:
        context["history"] = db.list_users(limit=6)
        context["now"] = timezone.now()

    return render(request, "blog/home.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return render(request, "blog/login.html")
