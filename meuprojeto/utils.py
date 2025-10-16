def comparar_seguidores(username, profile, db):
    resultados = {}

    previous_followers = db.comparacao_followers(username)
    previous_following = db.comparacao_folliwing(username)

    if previous_followers != "":
        if profile.followers > previous_followers:
            resultados["followers"] = f"Increased by {profile.followers - previous_followers}"
        elif profile.followers < previous_followers:
            resultados["followers"] = f"Decreased by {previous_followers - profile.followers}"
        else:
            resultados["followers"] = "No change"

    if previous_following != "":
        if profile.followees > previous_following:
            resultados["following"] = f"Increased by {profile.followees - previous_following}"
        elif profile.followees < previous_following:
            resultados["following"] = f"Decreased by {previous_following - profile.followees}"
        else:
            resultados["following"] = "No change"

    return resultados
