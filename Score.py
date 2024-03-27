def save_score(name, score, difficulty):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name} {score} {difficulty}\n")