import json
import csv

filepath = "data/Full_version_french_clan_list"

# Ouvrir le fichier JSON et le lire
with open(filepath+'.json', 'r') as f:
    data = json.load(f)

# Exporter en CSV
with open(filepath+'.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Écrire la ligne d'en-tête
    writer.writerow(['ID', 'Clan Tag', 'Clan Name'])
    # Écrire chaque ligne de données
    for id, clan_data in data.items():
        writer.writerow([id, clan_data['clan_tag'], clan_data['clan_name']])

# Exporter en TXT
with open(filepath+'.txt', 'w') as f:
    # Écrire chaque ligne de données avec un formatage spécifique
    for id, clan_data in data.items():
        f.write(f"ID: {id}\nClan Tag: {clan_data['clan_tag']}\nClan Name: {clan_data['clan_name']}\n\n")