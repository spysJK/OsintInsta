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
        previous_followers = db.comparacao_followers(username)
        previous_following = db.comparacao_folliwing(username)
        if previous_followers != "":
            if profile.followers > previous_followers:
                print(f"Followers increased by" profile.followers, previous_followers)
            elif profile.followers < previous_followers:
                print(f"Followers decreased by" previous_followers, profile.followers)
            else:
                print("No change in followers")
        if previous_following != "":
            if profile.followees > previous_following:
                print(f"Following increased by" profile.followees, previous_following)
            elif profile.followees < previous_following:
                print(f"Following decreased by" previous_following, profile.followees)
            else:
                print("No change in following")
    