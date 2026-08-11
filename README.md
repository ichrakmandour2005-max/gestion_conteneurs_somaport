# 📦 Gestion des Conteneurs — SOMAPORT

Application web développée dans le cadre d'un stage à **SOMAPORT** (terminal à conteneurs, Port de Casablanca), permettant d'automatiser le suivi et le placement des conteneurs sur le parc de stockage.

## ✨ Fonctionnalités

- **Pointage automatique** : date et heure d'entrée / sortie enregistrées sans saisie manuelle
- **Placement automatique** des conteneurs dans le parc, selon des règles métier :
  - Un conteneur de **20 pieds** occupe une seule position
  - Un conteneur de **40 pieds** occupe deux positions consécutives, affichées sous un code de position paire (ex. `AA04A`)
  - Empilement sur 7 niveaux (A à G), du bas vers le haut
  - Un conteneur vide ne peut jamais être placé sous un autre conteneur
  - Un conteneur de 40 pieds ne peut pas reposer sur un conteneur de 20 pieds
- **Validation automatique** du nom des conteneurs (format ISO : 4 lettres + 7 chiffres)
- **Suivi du statut** : entrée → transfert (interne / externe) → sortie (terrestre / maritime)
- **Tableau de bord** avec indicateurs en temps réel (occupation par zone, entrées/sorties du jour)
- **Plan visuel du parc**, avec code couleur (libre / occupé, plein / vide) et fusion visuelle des cases pour les conteneurs 40 pieds
- **Recherche** par nom de conteneur ou par code d'emplacement
- **Durée de séjour** moyenne, avec **export Excel**
- **Historique du stock** consultable à n'importe quelle date passée

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python / Django |
| Base de données | MySQL |
| Frontend | HTML / CSS (sur mesure, sans framework externe) |
| Export de données | openpyxl |
| Environnement local | WampServer |

## 📁 Structure du projet

```
gestion_conteneurs/
├── config/                          # Configuration du projet Django
├── conteneurs/
│   ├── models.py                    # Modèles Conteneur, Emplacement
│   ├── services.py                  # Logique métier (placement, empilement)
│   ├── views.py                     # Vues de l'application
│   ├── urls.py
│   ├── admin.py
│   ├── management/commands/
│   │   └── generer_emplacements.py  # Génération des emplacements du parc
│   ├── static/conteneurs/css/
│   └── templates/conteneurs/
├── manage.py
└── requirements.txt
```

## 🚀 Installation

**1. Cloner le dépôt**
```bash
git clone https://github.com/<ton-nom-utilisateur>/gestion_conteneurs.git
cd gestion_conteneurs
```

**2. Créer et activer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Configurer les variables d'environnement**

Créer un fichier `.env` à la racine du projet :
```
SECRET_KEY=ta-secret-key-django
DB_NAME=gestion_conteneurs_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

**5. Créer la base de données MySQL**
```sql
CREATE DATABASE gestion_conteneurs_db CHARACTER SET utf8mb4;
```

**6. Appliquer les migrations**
```bash
python manage.py migrate
```

**7. Générer les emplacements du parc**
```bash
python manage.py generer_emplacements
```

**8. Créer un compte administrateur**
```bash
python manage.py createsuperuser
```

**9. Lancer le serveur**
```bash
python manage.py runserver
```

L'application est accessible sur `http://127.0.0.1:8000/`

## 📐 Modèle de données

- **Conteneur** : nom (validé), taille (20/40 pieds), état (plein/vide), statut, dates d'entrée/sortie
- **Emplacement** : zone, rangée (niveau d'empilement), position — lié à un conteneur via une clé étrangère

## 👤 Auteure

**Ichrak Mandour** — Élève ingénieure en Informatique et Réseaux, EMSI
Stage réalisé chez SOMAPORT

## 📄 Licence

Projet académique — usage éducatif dans le cadre d'un stage de fin d'année.
