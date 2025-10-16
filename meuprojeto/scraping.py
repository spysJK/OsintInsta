import instaloader
from database import Database
import os

l = instaloader.Instaloader()
db = Database()

def profile_info(username):
    profile = instaloader.Profile.from_username(l.context, username)

    db.create_table()
    os.system("clear")

    print("Username:", profile.username)
    print("Profile Pic URL:", profile.profile_pic_url)

    # 🔽 Salva a imagem localmente (instaloader faz isso automaticamente)
    profile_pic_path = f"media/{username}_profile_pic.jpg"
    os.makedirs("media", exist_ok=True)
    l.download_pic(profile_pic_path, profile.profile_pic_url)

    db.add_user(profile.username, profile.followers, profile.followees)

    return {
        "username": profile.username,
        "followers": profile.followers,
        "following": profile.followees,
        "bio": profile.biography,
        "profile_pic_path": profile_pic_path,  # 👈 caminho local
    }
