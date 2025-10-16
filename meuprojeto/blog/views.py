
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
            if not profile_data:
                raise ValueError("profile_info não retornou dados")
        except Exception as e:
            # Exibe erro amigável no template
            return render(request, "blog/home.html", {
                "error": f"Erro ao buscar perfil: {e}"
            })

        profile_pic_path = profile_data.get("profile_pic_path")  # pode ser None
        followers = profile_data.get("followers")
        following = profile_data.get("following")

        previous_followers = db.comparacao_followers(username)
        previous_following = db.comparacao_folliwing(username)

        followers_message = ""
        following_message = ""

        if previous_followers != "":
            diff = followers - previous_followers
            if diff > 0:
                followers_message = f"{diff} seguidores"
            elif diff < 0:
                followers_message = f"{diff} seguidores a menos"
            else:
                followers_message = "Seguidores sem mudança"

        if previous_following != "":
            diff = following - previous_following
            if diff > 0:
                following_message = f"👣 +{diff} seguindo"
            elif diff < 0:
                following_message = f"{abs(diff)} seguindo a menos"
            else:
                following_message = "Seguindo sem mudança"

        context = {
            "username": username,
            "profile_pic_path": profile_pic_path,
            "followers": followers,
            "following": following,
            "followers_message": followers_message,
            "following_message": following_message,
              "profile_pic_path": profile_data.get("profile_pic_path"),  # <- importante!
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
