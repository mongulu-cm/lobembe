from github import Github
from tqdm import tqdm

# Remplacez ces variables par vos informations
token = "xxxxxxxxx"
repo_source = "mongulu-cm/chama"
repo_cible = "mongulu-cm/icons-fasaha"

# Authentification avec votre token GitHub
g = Github(token)

# Obtention de l'objet du repo source et cible
source = g.get_repo(repo_source)
cible = g.get_repo(repo_cible)

# Récupération des labels du repo source
labels_source = list(source.get_labels())

# Suppression de tous les labels existants du repo cible
labels_cible = list(cible.get_labels())
for label in tqdm(labels_cible, desc="Suppression des labels existants"):
    label.delete()

# Création des labels du repo source dans le repo cible
for label in tqdm(labels_source, desc="Création des labels dans le repo cible"):
    cible.create_label(name=label.name, color=label.color, description=label.description)


print("Les labels ont été copiés avec succès.")
