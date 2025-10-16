import instaloader
import os
import requests

def profile_info(username):
    l = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(l.context, username)
    except Exception as e:
        raise ValueError(f"Erro ao buscar perfil: {e}")

    os.makedirs("media/profile_pics", exist_ok=True)
    filename = f"{username}_profile_pic.jpg"
    profile_pic_path = os.path.join("media", "profile_pics", filename)

    try:
        resp = requests.get(str(profile.profile_pic_url), timeout=10)
        resp.raise_for_status()
        with open(profile_pic_path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        print("Erro ao baixar imagem:", e)
        profile_pic_path = None

    return {
        "username": profile.username,
        "followers": profile.followers,
        "following": profile.followees,
        "bio": profile.biography,
        "profile_pic_path": f"/{profile_pic_path}" if profile_pic_path else None,
    }
