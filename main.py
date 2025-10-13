from scraping import profile_info, db

if __name__ == "__main__":
    user = input("Enter Instagram username: ")
    profile_info(user)
    db.close()
