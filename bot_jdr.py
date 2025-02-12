import json
import subprocess

def git_push():
    commit_message="Auto commit"
    try:
        # Ajouter tous les fichiers
        subprocess.run(["git", "add", "*"], check=True)

        # Commit avec un message
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Pousser vers le repo distant
        subprocess.run(["git", "push"], check=True)

        print("✅ Modification poussée avec succès !")

    except subprocess.CalledProcessError as e:
        print("❌ Une erreur est survenue :", e)

def augment_lvl(stats):

    name = input(f"quel stats a augmenter ?\n: ")
    array = name.split()
    name = array[0]
    stat = array[1]
    stats["name"][name]["LVL"] += 1
    stats["name"][name][stat] += int(array[2])


def ask_question_MP(default_value):
     user_input_MP = input(f"change value for MP ?\n(default value is 5)\n: ")
     if user_input_MP == "":
          return default_value
     return user_input_MP

def ask_question_HP(default_value):
     user_input_HP = input(f"change value for HP ?\n(default_value is 5)\n: ")
     if user_input_HP == "":
          return default_value
     return user_input_HP

def debuff(stats, parts):
    name = parts[1]
    stat = parts[2]
    valeur = int(parts[3])
    stats["name"][name][stat] += valeur
    print(stats)


def regen(stats, value_HP, value_MP, parts):
        if parts[0] != "":
            name = parts[0]
        for name in stats["name"]:
            stats["name"][name]["HP"] += int(value_HP)
            stats["name"][name]["MP"] += int(value_MP)
    

def main():
    with open("stats.json", "r") as f:
        stats = json.load(f)
    stats_base = json.loads(json.dumps(stats))  # Copie profonde
    while True:
        commande = input("action ?\n")
        parts = commande.split()
        if parts[0] == "quit":
            break

        if parts[0] == "debuff":
            debuff(stats, parts) 
        
        if parts[0] == "next":
            value_hp = ask_question_HP(5)
            value_mp = ask_question_MP(5)
            regen(stats, value_hp, value_mp, parts)
            git_push()

        if parts[0] == "lvl_up":
             augment_lvl(stats)
        
        if parts[0] == "fin_combat":
            stats = json.loads(json.dumps(stats_base))  # Reset stats
        
        with open("stats.json", "w") as f:
                json.dump(stats, f, indent=4)  # Sauvegarde dans le fichier


if __name__ == "__main__":
    main()
