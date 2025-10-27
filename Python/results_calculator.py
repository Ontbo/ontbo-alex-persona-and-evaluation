import pandas as pd
import os

# Dossier contenant les fichiers CSV
csv_dir = "."

# Initialisation des compteurs
gpt_yes_count = 0
gpt_total = 0
ontbo_yes_count = 0
ontbo_total = 0

# Parcourir tous les fichiers CSV dans le dossier
for filename in os.listdir(csv_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_dir, filename)
        df = pd.read_csv(filepath)

        # Comptage des "yes" pour gpt
        gpt_rows = df[df['agent'] == 'gpt']
        gpt_yes_count += (gpt_rows['reponse'].str.lower() == 'yes').sum()
        gpt_total += len(gpt_rows)

        # Comptage des "yes" pour ontbo
        ontbo_rows = df[df['agent'] == 'ontbo']
        ontbo_yes_count += (ontbo_rows['reponse'].str.lower() == 'yes').sum()
        ontbo_total += len(ontbo_rows)

# Calcul des moyennes
gpt_avg = gpt_yes_count / gpt_total if gpt_total > 0 else 0
ontbo_avg = ontbo_yes_count / ontbo_total if ontbo_total > 0 else 0

print(f"Moyenne de 'yes' pour gpt : {gpt_avg:.2f}")
print(f"Moyenne de 'yes' pour ontbo : {ontbo_avg:.2f}")
