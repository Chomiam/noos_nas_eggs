<div align="center">
  <img src="assets/logo.png" alt="Noos NAS Logo" width="500"/>
  <br/><br/>

  # 🎮 Noos Game Eggs Hub
  ### *Le Hub Officiel de Serveurs de Jeux Vidéo Dédiés pour Noos NAS Edition*

  [![Games Count](https://img.shields.io/badge/Catalogue-10%20Jeux%20Certifi%C3%A9s-brightgreen?style=for-the-badge&logo=gamepad&logoColor=white)](https://github.com/Chomiam/noos_nas_eggs)
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

| Jeu | Catégorie | Mémoire Conseillée | Ports Réseau | Points Forts de l'Egg |
| :--- | :--- | :--- | :--- | :--- |
| **Minecraft: Java Edition** | Bac à sable / Survie | 4 Go | `25565/both` | Détection automatique des versions Paper/Spigot/Vanilla, support des plugins et mods. |
| **Minecraft: Bedrock Edition** | Bac à sable / Crossplay | 2 Go | `19132/udp` | Idéal pour consoles (Switch, PS5, Xbox), tablettes et smartphones. |
| **Palworld Dedicated Server** | Aventure / Survie | 8 Go | `8211/udp` | Optimisation de la mémoire vive et persistance des bases et Pals des joueurs. |
| **Valheim Dedicated Server** | Survie Mythologique | 4 Go | `2456/udp`, `2457/udp` | Synchronisation automatique des mondes et sauvegardes régulières. |
| **7 Days to Die** | Survie Zombie / Craft | 8 Go | `26900/both`, `8081/tcp` | Prise en charge du panneau d'administration web et des cartes procédurales. |
| **Project Zomboid** | Survie Hardcore | 4 Go | `16261/udp`, `16262/udp` | Gestion simplifiée des mods Steam Workshop et réglages bac à sable. |
| **Rust Dedicated Server** | Survie PvP / Craft | 8 Go | `28015/udp`, `28016/tcp` | Serveur dédié officiel avec support de l'application Rust+ et console RCON. |
| **Terraria Dedicated Server** | Aventure 2D Sandbox | 2 Go | `7777/both` | Très faible consommation de ressources, fluide jusqu'à 16 joueurs simultanés. |
| **Enshrouded Dedicated Server** | Action RPG / Survie | 8 Go | `15636/udp`, `15637/udp` | Mondes voxel haute fidélité pour explorer l'univers en coopération. |
| **Counter-Strike 2** | FPS Compétitif | 4 Go | `27015/both`, `27020/udp` | Serveur officiel basé sur le moteur Source 2 avec tick rate élevé. |

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
