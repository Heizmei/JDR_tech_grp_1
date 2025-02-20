import json
import subprocess

def git_push():
    commit_message = "auto-commit"
    try:
        subprocess.run(["git", "add", "stat_global"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Modification poussée avec succès !")
    except subprocess.CalledProcessError as e:
        print("❌ Une erreur est survenue :", e)

def ask_question(prompt, default_value):
    user_input = input(f"{prompt} (default: {default_value})\n: ").strip()
    return int(user_input) if user_input.isdigit() else default_value

def augment_lvl(stats):
    
    name = "your_name"
    
    # name = input("Quel personnage gagne un niveau ?\n: ").strip()
    # if name not in stats["name"]:
        # print(f"❌ Le personnage '{name}' n'existe pas !")
        # return
    
    valid_stats = ["int", "per", "agi", "for", "char"]
    while True:
        stat = input(f"Quelle stat augmenter ? {valid_stats}\n: ").strip()
        if stat in valid_stats:
            break
        print("❌ Stat invalide, veuillez choisir parmi :", valid_stats)
    
    while True:
        try:
            value = int(input(f"De combien augmenter {stat} ?\n: ").strip())
            break
        except ValueError:
            print("❌ Entrée invalide. Veuillez entrer un nombre entier.")
    
    stats["name"][name]["LVL"] += 1
    stats["name"][name][stat] += value
    print(f"✅ {name} passe au niveau {stats['name'][name]['LVL']} et gagne {value} en {stat} !")

def debuff(stats, parts):
    if len(parts) < 4:
        print("❌ Commande incorrecte ! Format: debuff <name> <stat> <valeur>")
        return
    
    name = "your_name"
    
    stat, valeur = parts[1], parts[2], parts[3]
    if stat not in stats["name"][name]:
        print("❌ stat invalide !")
        return
    stats["name"][name][stat] += int(valeur)
    print(f"✅ {name} a perdu {valeur} en {stat}")

def regen(stats, value_hp, value_mp):
    
    name = "your_name"

    for name in stats["name"]:
        stats["name"][name]["HP"] += value_hp
        stats["name"][name]["MP"] += value_mp

def main():
    with open("your_folder/stats.json", "r") as f:
        stats = json.load(f)
    stats_base = json.loads(json.dumps(stats))  # Copie profonde
    
    while True:
        print("\nCommandes disponibles:")
        print("- quit (Quitter le programme)")
        print("- next (Passer au tour suivant et régénérer passivement)")
        print("- lvl_up (Augmenter une stat lors d'un level-up)")
        print("- start_combat (Sauvegarde l'état des stats avant le combat)")
        print("- fin_combat (Restaure les stats sauvegardées avant le combat)")
        
        commande = input("Action ?\n: ").strip()
        parts = commande.split()
        if not parts:
            continue

        if parts[0] == "quit":
            break

        if parts[0] == "start_combat":
            stats_base = json.loads(json.dumps(stats))
            print("✅ Stats sauvegardées avant combat.")

        if parts[0] == "debuff":
            debuff(stats, parts)

        if parts[0] == "next":
            value_hp = ask_question("Change value for HP ?", 5)
            value_mp = ask_question("Change value for MP ?", 5)
            regen(stats, value_hp, value_mp)
            git_push()

        if parts[0] == "lvl_up":
            augment_lvl(stats)

        if parts[0] == "fin_combat":
            stats = json.loads(json.dumps(stats_base))
            print("✅ Stats restaurées après le combat.")
        
        with open("stat_global/stats.json", "w") as f:
            json.dump(stats, f, indent=4)
        
if __name__ == "__main__":
    main()
