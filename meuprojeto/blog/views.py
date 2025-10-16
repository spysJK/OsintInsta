
from scraping import profile_info
from database import Database
from django.contrib import messages 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

db = Database()
def home(request):
    if request.method == "POST":
        username = request.POST.get("username")

        db.create_table()
        try:
            profile_data = profile_info(username)
        except Exception as e:
            return render(request, "blog/home.html", {
                "error": f"Erro ao buscar perfil: {e}"
            })

        # extrai dados do scraping
        profile_pic_url = profile_data.get("profile_pic_url")
        current_followers = profile_data.get("followers")
        current_following = profile_data.get("following")

        previous_followers = db.comparacao_followers(username)
        previous_following = db.comparacao_folliwing(username)

        followers_message = ""
        following_message = ""

        if previous_followers != "":
            diff = current_followers - previous_followers
            if diff > 0:
                followers_message = f"🔼 +{diff} seguidores"
            elif diff < 0:
                followers_message = f"🔽 {abs(diff)} seguidores a menos"
            else:
                followers_message = "Seguidores sem mudança"

        if previous_following != "":
            diff = current_following - previous_following
            if diff > 0:
                following_message = f"👣 +{diff} seguindo"
            elif diff < 0:
                following_message = f"{abs(diff)} seguindo a menos"
            else:
                following_message = "Seguindo sem mudança"

        context = {
            "username": username,
            "profile_pic_url": profile_pic_url,  # 👈 adicionamos aqui
            "followers": current_followers,
            "following": current_following,
            "followers_message": followers_message,
            "following_message": following_message,
        }

        return render(request, "blog/home.html", context)

    return render(request, "blog/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return render(request, "blog/login.html")
