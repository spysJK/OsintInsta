# scraping.py
import instaloader
from database import Database
import os
import requests

l = instaloader.Instaloader()
db = Database()

def profile_info(username):
    # Tenta obter o perfil (lança exceção se usuário não existir ou instaloader falhar)
    profile = instaloader.Profile.from_username(l.context, username)

    # Garante tabela no DB
    db.create_table()

    # Imprime no terminal (opcional)
    print("Username:", profile.username)
    print("User ID:", profile.userid)
    print("Number of Posts:", profile.mediacount)
    print("Followers:", profile.followers)
    print("Following:", profile.followees)
    print("Bio:", profile.biography)
    print("Profile Pic URL:", profile.profile_pic_url)

    # Tenta salvar a imagem localmente usando requests (mais confiável)
    os.makedirs("media/profile_pics", exist_ok=True)
    filename = f"{username}_profile_pic.jpg"
    profile_pic_path = os.path.join("media", "profile_pics", filename)

    try:
        resp = requests.get(str(profile.profile_pic_url), timeout=10)
        resp.raise_for_status()
        with open(profile_pic_path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        # se houve problema no download, define None e imprime o erro
        print("Erro ao baixar imagem de perfil:", e)
        profile_pic_path = None

    # Salva no banco (sua função existente)
    db.add_user(profile.username, profile.followers, profile.followees)

    # Comparações existentes (mantém seu comportamento)
    previous_followers = db.comparacao_followers(username)
    previous_following = db.comparacao_folliwing(username)

    if previous_followers != "":
        if profile.followers > previous_followers:
            print(f"Followers increased by {profile.followers - previous_followers}")
        elif profile.followers < previous_followers:
            print(f"Followers decreased by {previous_followers - profile.followers}")
        else:
            print("No change in followers")

    if previous_following != "":
        if profile.followees > previous_following:
            print(f"Following increased by {profile.followees - previous_following}")
        elif profile.followees < previous_following:
            print(f"Following decreased by {previous_following - profile.followees}")
        else:
            print("No change in following")

    # Retorna dicionário para a view
    return {
        "username": profile.username,
        "user_id": profile.userid,
        "num_posts": profile.mediacount,
        "followers": profile.followers,
        "following": profile.followees,
        "bio": profile.biography,
       "profile_pic_path": f"/{profile_pic_path}",
 # caminho relativo ao projeto (media/...)
    }
