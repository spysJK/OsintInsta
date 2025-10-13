import instaloader
from database import Database
import os 
l = instaloader.Instaloader()

db = Database()


def profile_info(username):
    profile = instaloader.Profile.from_username(l.context, username)
    os.system("clear")
    print("Username: ", profile.username)
    print("User ID: ", profile.userid)
    print("Number of Posts: ", profile.mediacount)
    print("Followers: ", profile.followers)
    print("Following: ", profile.followees)
    print("Bio: ", profile.biography)
    print("Profile Pic URL: ", profile.profile_pic_url)
    db.add_user(profile.username, profile.followers, profile.followees)
if __name__ == "__main__":   
    user = input("Enter Instagram username: ")
    profile_info(user)
