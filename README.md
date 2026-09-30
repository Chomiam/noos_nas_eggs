# 🥚 STEvE_OS Game Eggs Hub (`steve_nas_eggs`)

Catalogue officiel et certifié d'Eggs de serveurs de jeu conteneurisés pour **STEvE_OS NAS**.

Chaque Egg de ce dépôt est autonome, testé sur NixOS/Docker, traduit en français avec ports déclarés, icônes officielles HD et bannières panoramiques.

---

## 🎮 Jeux Disponibles (10)

| Jeu | Catégorie | Mémoire Recommandée | Ports Déclarés |
| :--- | :--- | :--- | :--- |
| **Minecraft: Java Edition** | Bac à sable / Survie | 4096 Mo | `25565/both` |
| **Minecraft: Bedrock Edition** | Bac à sable / Survie | 2048 Mo | `19132/udp` |
| **Palworld Dedicated Server** | Aventure / Survie | 8192 Mo | `8211/udp` |
| **Valheim Dedicated Server** | Survie Mythologique | 4096 Mo | `2456/udp + 2457/udp` |
| **7 Days to Die Dedicated Server** | Survie / Post-Apocalyptique | 8192 Mo | `26900/both + 26901/udp, 26902/udp, 8081/tcp` |
| **Project Zomboid Dedicated Server** | Survie Zombie Hardcore | 4096 Mo | `16261/udp + 16262/udp` |
| **Rust Dedicated Server** | Survie PvP / Sandbox | 8192 Mo | `28015/udp + 28016/tcp` |
| **Terraria Dedicated Server** | Aventure / Sandbox 2D | 2048 Mo | `7777/both` |
| **Enshrouded Dedicated Server** | Survie / Action RPG | 8192 Mo | `15636/udp + 15637/udp` |
| **Counter-Strike 2 Dedicated Server** | FPS Compétitif | 4096 Mo | `27015/both + 27020/udp` |

---

## 📡 Utilisation dans STEvE_OS

Le Dashboard STEvE_OS synchronise automatiquement ce catalogue en interrogeant :
```
https://raw.githubusercontent.com/Chomiam/steve_nas_eggs/main/catalog.json
```
