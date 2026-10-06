<div align="center">
  <img src="assets/logo.png" alt="Noos NAS Logo" width="500"/>
  <br/><br/>

  # 🎮 Noos Game Eggs Hub
  ### *Le Hub Officiel de Serveurs de Jeux Vidéo Dédiés pour Noos NAS Edition*

  [![Games Count](https://img.shields.io/badge/Catalogue-50%20Jeux%20Certifi%C3%A9s-brightgreen?style=for-the-badge&logo=gamepad&logoColor=white)](https://github.com/Chomiam/noos_nas_eggs)
  [![Standard](https://img.shields.io/badge/Format-Pterodactyl%20Eggs%20V2-blue?style=for-the-badge)](#)
  [![Cost](https://img.shields.io/badge/%C3%89conomies-0%E2%82%AC%20de%20Location%2Fmois-orange?style=for-the-badge)](#)
  [![Isolation](https://img.shields.io/badge/Isolation-Conteneurs%20Docker%20%C3%89tanches-teal?style=for-the-badge&logo=docker&logoColor=white)](#)
  [![Language](https://img.shields.io/badge/Langue-100%25%20Fran%C3%A7ais-purple?style=for-the-badge)](#)

  <p align="center">
    <strong>Hébergez vos mondes multijoueurs privés en toute liberté. Vos amis, vos règles, vos sauvegardes, directement sur votre matériel.</strong>
  </p>
</div>

---

## 🕹️ Le Gaming Souverain : Pourquoi Héberger sur Votre Noos NAS ?

Louer un serveur de jeu auprès d'un hébergeur traditionnel implique des coûts récurrents élevés, des plafonds stricts sur le nombre de joueurs autorisés, des limitations de mémoire vive arbitraires et un risque de perdre vos sauvegardes si vous suspendez votre abonnement.

Avec **Noos Game Eggs Hub**, votre serveur de stockage personnel se transforme en une plateforme de jeu haute performance :

- 💸 **0 € de Frais Mensuels** : Rentabilisez votre matériel existant et jouez sans limite de temps ni facturation au slot.
- ⚡ **Performances Matérielles Brutes** : Vos serveurs exploitent directement la mémoire vive rapide et la vélocité des SSD/NVMe de votre NAS pour un monde sans ralentissement (*tick rate* optimal).
- 🚀 **Déploiement en 1-Clic** : Plus besoin de configurer manuellement SteamCMD, d'installer les dépendances Java/Wine ou d'écrire des scripts de démarrage barbares. L'Egg prend tout en charge automatiquement.
- 🌐 **Réseau Transparent & Sécurisé** : L'interface Noos affiche en un coup d'œil les adresses de connexion pour vos joueurs :
  - **IP Locale** pour jouer avec les membres du foyer sur le même réseau.
  - **IP VPN WireGuard** pour inviter vos amis dans un réseau privé virtuel ultra-sécurisé sans ouvrir le moindre port sur votre box internet.
  - **IP Publique** pour un accès direct avec ports pré-configurés.
- 🔒 **Isolation Complète** : Chaque serveur de jeu s'exécute dans un conteneur dédié et isolé, garantissant qu'aucune activité en jeu ne perturbe vos fichiers, vos partages ou vos autres applications NAS.

---

## 🎮 Catalogue Officiel des Jeux Certifiés

Chaque Egg de ce dépôt a été méticuleusement configuré, testé sur NixOS/Docker, traduit en français avec ports déclarés, icônes officielles HD et bannières panoramiques :

| Jeu | Catégorie | Mémoire Conseillée | Ports Réseau | Description / Rôle |
| :--- | :--- | :--- | :--- | :--- |
| **7 Days to Die Dedicated Server** | Survie / Post-Apocalyptique | 8 Go | `26900/both` | Survivez à la horde du 7ème jour dans un monde voxel hostile |
| **ARK: Survival Ascended Dedicated Server** | Survie / Dinosaures | 16 Go | `7777/udp` | L'expérience ARK réinventée sous Unreal Engine 5 avec rendu next-gen |
| **ARK: Survival Evolved Dedicated Server** | Survie / Dinosaures | 12 Go | `7777/udp` | Domptez des dinosaures et survivez sur une île préhistorique mystérieuse |
| **Abiotic Factor Dedicated Server** | Sci-Fi / Survie Coop | 8 Go | `7777/udp` | Survivez en tant que scientifiques face à des anomalies paranormales en centre souterrain |
| **Arma 3 Dedicated Server** | Simulation Militaire | 8 Go | `2302/udp` | Simulation de combat militaire réaliste et tactique en monde ouvert gigantesque |
| **Assetto Corsa Dedicated Server** | Course / Simulation | 4 Go | `9600/both` | Simulation de course automobile ultra-réaliste avec physique de pointe |
| **Astroneer Dedicated Server** | Exploration Spatiale | 6 Go | `8777/udp` | Explorez et façonnez des mondes lointains à l'ère des grandes découvertes aérospatiales |
| **Barotrauma Dedicated Server** | Simulation / Sous-Marin | 4 Go | `27015/udp` | Pilotez un sous-marin dans les profondeurs glaciales et hostiles d'Europe |
| **Black Mesa Dedicated Server** | FPS Multijoueur | 4 Go | `27015/both` | Le remake officiel et modernisé du mythique Half-Life en affrontement multijoueur |
| **Conan Exiles Dedicated Server** | Survie / Barbares | 8 Go | `7777/udp` | Survivez, bâtissez et dominez dans les Terres Exilées impitoyables de Conan |
| **Core Keeper Dedicated Server** | Aventure / Sandbox 2D | 4 Go | `27015/udp` | Explorez une caverne sans fin de reliques, de créatures et de ressources en coop |
| **Counter-Strike 2 Dedicated Server** | FPS Compétitif | 4 Go | `27015/both` | Le summum du tir tactique et compétitif par Valve |
| **Counter-Strike: Source Dedicated Server** | FPS Compétitif | 2 Go | `27015/both` | L'incontournable classique Source du combat terroristes contre antiterroristes |
| **DayZ Dedicated Server** | Survie Post-Apocalyptique | 8 Go | `2302/udp` | Survivez à l'infection, aux autres survivants et à la famine en Tcherno |
| **Don't Starve Together Dedicated Server** | Survie / Aventure | 4 Go | `10999/udp` | Explorez et survivez ensemble dans un univers hostile façonné à la main |
| **Eco Dedicated Server** | Écologie & Civilisation | 8 Go | `3000/both` | Bâtissez une civilisation florissante pour détruire un météore sans ruiner l'écosystème |
| **Empyrion: Galactic Survival Dedicated Server** | Survie Galactique | 8 Go | `30000/udp` | Aventure spatiale 3D avec exploration planétaire, construction et combats |
| **Enshrouded Dedicated Server** | Survie / Action RPG | 8 Go | `15636/udp` | Explorez le royaume déchu d'Embervale dans ce RPG de survie voxel |
| **Factorio Headless Server** | Automatisation / Gestion | 4 Go | `34197/udp` | Construisez et défendez des usines automatisées géantes sur une planète hostile |
| **Foundry Dedicated Server** | Usine & Voxel | 8 Go | `22500/udp` | Automatisez une usine colossale dans un monde voxel infini généré procéduralement |
| **Garry's Mod Dedicated Server** | Bac à sable Source | 4 Go | `27015/both` | Sandbox physique multijoueur légendaire sous Source Engine (TTT, DarkRP) |
| **HumanitZ Dedicated Server** | Survie Post-Apocalyptique | 6 Go | `7777/udp` | Survie en vue isométrique dans un monde ouvert envahi par les Zeeks |
| **Icarus Dedicated Server** | Survie Sci-Fi | 12 Go | `17777/udp` | Survivez sur une planète terraformée hostile lors de missions chronométrées |
| **Insurgency: Sandstorm Dedicated Server** | FPS Tactique | 6 Go | `27102/udp` | FPS tactique hardcore en combats urbains au Moyen-Orient axé sur le jeu d'équipe |
| **Killing Floor 2 Dedicated Server** | Horreur / Coopératif | 4 Go | `7777/udp` | Affrontez des vagues incessantes de spécimens mutants Zeds à 6 joueurs en coop |
| **Left 4 Dead 2 Dedicated Server** | Horreur / Coopératif | 4 Go | `27015/both` | Survivez à l'apocalypse zombie à 4 en coopération intense à travers le Sud des USA |
| **Minecraft: Bedrock Edition** | Bac à sable / Survie | 2 Go | `19132/udp` | Serveur officiel Mojang BDS pour consoles, smartphones et Windows 10/11 |
| **Minecraft: Java Edition** | Bac à sable / Survie | 4 Go | `25565/both` | Serveur Minecraft Java haute performance propulsé par PaperMC 1.21+ |
| **Mordhau Dedicated Server** | Combat Médiéval | 6 Go | `7777/udp` | Combats médiévaux sanglants et précis à la première personne à grande échelle |
| **Myth of Empires Dedicated Server** | Sandbox Multijoueur Médiéval | 12 Go | `7777/udp` | Bâtissez un empire oriental féodal, recrutez des armées et menez des sièges colossaux |
| **Night of the Dead Dedicated Server** | Tower Defense / Survie | 8 Go | `7777/udp` | Construisez une forteresse bardée de pièges mécaniques pour repousser les hordes nocturnes |
| **No More Room in Hell Dedicated Server** | Horreur / Survie Coop | 2 Go | `27015/both` | Survie réaliste et désespérée face à la mort vivante inspirée des films de Romero |
| **Palworld Dedicated Server** | Aventure / Survie | 8 Go | `8211/udp` | Serveur multijoueur Palworld avec multithreading et persistance |
| **Project Zomboid Dedicated Server** | Survie Zombie Hardcore | 4 Go | `16261/udp` | L'ultime simulateur de survie apocalypse zombie en multijoueur |
| **Rust Dedicated Server** | Survie PvP / Sandbox | 8 Go | `28015/udp` | Survie sans pitié, construction de base et PvP brutal |
| **Satisfactory Dedicated Server** | Usine & Automatisation | 8 Go | `7777/udp` | Construisez des usines colossales et automatisez la production sur une planète alien |
| **Sons of the Forest Dedicated Server** | Horreur / Survie | 8 Go | `8766/udp` | Survivez aux cannibales et mutants sur une île isolée cauchemardesque |
| **Soulmask Dedicated Server** | Survie / Tribale | 8 Go | `8777/udp` | Échappez au rituel sacrificiel et découvrez les secrets des masques ancestraux |
| **Space Engineers Dedicated Server** | Simulation Spatiale | 12 Go | `27016/udp` | Construisez des vaisseaux, stations spatiales et avant-postes planétaires réalistes |
| **Squad Dedicated Server** | FPS Tactique | 8 Go | `7787/udp` | Combats tactiques par escouades combinées à grande échelle à 100 joueurs |
| **Starbound Dedicated Server** | Sandbox Spatial 2D | 4 Go | `21025/tcp` | Explorez un univers procédural infini à bord de votre propre vaisseau spatial |
| **Stationeers Dedicated Server** | Ingénierie Spatiale | 6 Go | `27016/udp` | Gérez la pression, l'atmosphère et les circuits d'une station spatiale complexe |
| **Stormworks: Build and Rescue Dedicated Server** | Sauvetage / Véhicules | 6 Go | `25564/both` | Concevez hélicoptères, bateaux et sous-marins pour des missions de sauvetage héroïques |
| **Team Fortress 2 Dedicated Server** | FPS Compétitif | 4 Go | `27015/both` | Le FPS par équipes légendaire de Valve aux 9 classes emblématiques |
| **Terraria Dedicated Server** | Aventure / Sandbox 2D | 2 Go | `7777/both` | Exploration, construction et combats de boss en 2D multijoueur |
| **The Forest Dedicated Server** | Horreur / Survie | 6 Go | `27016/udp` | Construisez, explorez et survivez dans une forêt infestée de cannibales |
| **Unturned Dedicated Server** | Survie / Post-Apocalyptique | 4 Go | `27015/both` | Survie zombie voxel en monde ouvert avec artisanat, conduite et barricades |
| **V Rising Dedicated Server** | Action RPG / Vampires | 8 Go | `9876/udp` | Réveillez-vous en vampire, bâtissez votre château gothique et régnez sur Vardoran |
| **Valheim Dedicated Server** | Survie Mythologique | 4 Go | `2456/udp` | Serveur dédié viking persistant dans un monde procédural nordique |
| **Vintage Story Dedicated Server** | Survie / Voxel Réaliste | 4 Go | `42420/tcp` | Survie hardcore intransigeante dans un monde voxel axée sur la géologie et l'artisanat |

---

## 🖥️ Fonctionnalités Administrateur sur le Dashboard Noos

Depuis l'onglet **Serveurs de Jeux** de votre [Noos NAS Dashboard](https://github.com/Chomiam/noos-nas-dashboard) :

- 💬 **Console Interactive en Direct** : Envoyez instantanément vos commandes administratives (`/op`, `/whitelist`, `/kick`, `/give`, `/save-all`) et consultez les logs du serveur en temps réel.
- 💾 **Sauvegarde Garantie** : Lors de l'arrêt du serveur, un signal d'extinction propre est envoyé au moteur de jeu pour forcer l'écriture sur disque et empêcher toute corruption de carte.
- 📂 **Accès Immédiat aux Sauvegardes** : Un raccourci direct ouvre l'emplacement exact de vos fichiers et mondes dans l'Explorateur de Fichiers Noos pour créer des copies ou restaurer une ancienne partie.

---

## 🛠️ Structure & Définition d'un Egg

Un Egg Noos NAS est structuré sous forme déclarative afin d'assurer une reproductibilité totale :

```text
eggs/<nom_du_jeu>/
├── egg.json              # Définition Pterodactyl : variables, scripts d'installation, ports
├── icon.png              # Icône carrée haute définition
└── banner.jpg            # Bannière panoramique au ratio 16:9
```

Le catalogue complet est distribué de manière déclarative via `catalog.json` à la racine de ce dépôt et synchronisé automatiquement par le tableau de bord Noos NAS.

---

## 🤝 Contribuer au Hub de Jeux

Vous souhaitez rendre compatible votre jeu favori avec Noos NAS ?
1. Clonez ce dépôt.
2. Ajoutez un dossier dans `eggs/<nom_du_jeu>/` avec son `egg.json`, son icône et sa bannière.
3. Testez le démarrage du conteneur.
4. Ouvrez une Pull Request pour que la communauté Noos puisse en profiter !

---

<div align="center">
  <sub>Fait partie de l'écosystème officiel <a href="https://github.com/Chomiam/noos-nas">Noos NAS Edition</a>.</sub>
</div>
