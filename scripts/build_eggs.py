#!/usr/bin/env python3
"""
build_eggs.py - Scrapes, formats, validates and registers 40 new game eggs
into the noos_nas_eggs repository and catalog.json.
Ensures official Steam CDN assets (1920x620 banner.jpg, icon.png) are retrieved.
"""

import os
import json
import urllib.request
import urllib.error
from PIL import Image
import io

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EGGS_DIR = os.path.join(BASE_DIR, "eggs")
CATALOG_PATH = os.path.join(BASE_DIR, "catalog.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

NEW_GAMES = [
    {
        "id": "satisfactory",
        "name": "Satisfactory Dedicated Server",
        "author": "Coffee Stain Studios & Noos NAS",
        "category": "Usine & Automatisation",
        "icon": "🏭",
        "tagline": "Construisez des usines colossales et automatisez la production sur une planète alien",
        "description": "Serveur dédié multijoueur officiel Satisfactory pour automatiser la production d'usines complexes avec vos amis sur une planète extraterrestre, incluant mises à jour automatiques SteamCMD et sauvegarde continue.",
        "steam_app_id": "1690800",
        "store_app_id": 526870,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 8888, "protocol": "udp", "description": "Port de messagerie fiable"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "./Engine/Binaries/Linux/*-Linux-Shipping FactoryGame -Port={{SERVER_PORT}} -ReliablePort={{RELIABLE_PORT}}",
        "variables": [
            {"name": "Port de messagerie fiable", "env_variable": "RELIABLE_PORT", "description": "Port UDP fiable", "default_value": "8888", "input_type": "number", "options": None},
            {"name": "Nombre de sauvegardes tournantes", "env_variable": "NUM_AUTOSAVES", "description": "Nombre de sauvegardes automatiques", "default_value": "5", "input_type": "number", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité max de joueurs", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "ark-survival-evolved",
        "name": "ARK: Survival Evolved Dedicated Server",
        "author": "Studio Wildcard & Noos NAS",
        "category": "Survie / Dinosaures",
        "icon": "🦖",
        "tagline": "Domptez des dinosaures et survivez sur une île préhistorique mystérieuse",
        "description": "Serveur dédié multijoueur complet pour ARK: Survival Evolved avec support des cartes personnalisées, gestion d'élevage, taming et console RCON intégrée.",
        "steam_app_id": "376030",
        "store_app_id": 346110,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 7778, "protocol": "udp", "description": "Port Raw UDP de jeu secondaire"},
            {"port": 27015, "protocol": "udp", "description": "Port de requête Steam Query"},
            {"port": 27020, "protocol": "tcp", "description": "Port console RCON"}
        ],
        "default_memory_mb": 12288,
        "min_memory_mb": 6144,
        "startup_cmd": "./ShooterGame/Binaries/Linux/ShooterGameServer {{SERVER_MAP}}?listen?SessionName=\"{{SERVER_NAME}}\"?ServerPassword=\"{{SERVER_PASSWORD}}\"?ServerAdminPassword=\"{{ADMIN_PASSWORD}}\"?Port={{SERVER_PORT}}?QueryPort={{QUERY_PORT}}?RCONPort={{RCON_PORT}} -server -log",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché dans la liste des serveurs ARK", "default_value": "Serveur ARK Noos NAS", "input_type": "text", "options": None},
            {"name": "Carte du monde", "env_variable": "SERVER_MAP", "description": "Nom de la carte de jeu", "default_value": "TheIsland", "input_type": "select", "options": ["TheIsland", "TheCenter", "ScorchedEarth_P", "Ragnarok", "Aberration_P", "Extinction", "Valguero_P", "Genesis", "CrystalIsles", "Gen2", "LostIsland", "Fjordur"]},
            {"name": "Mot de passe joueur", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe pour se connecter", "default_value": "", "input_type": "password", "options": None},
            {"name": "Mot de passe Administrateur", "env_variable": "ADMIN_PASSWORD", "description": "Mot de passe admin console", "default_value": "NoosArkAdmin123!", "input_type": "password", "options": None},
            {"name": "Port Steam Query", "env_variable": "QUERY_PORT", "description": "Port de requête Steam", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Port RCON", "env_variable": "RCON_PORT", "description": "Port de gestion RCON", "default_value": "27020", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "ark-survival-ascended",
        "name": "ARK: Survival Ascended Dedicated Server",
        "author": "Studio Wildcard & Noos NAS",
        "category": "Survie / Dinosaures",
        "icon": "🦕",
        "tagline": "L'expérience ARK réinventée sous Unreal Engine 5 avec rendu next-gen",
        "description": "Serveur dédié officiel ARK: Survival Ascended sous Unreal Engine 5 propulsé par Proton avec gestion du cross-play et modding CurseForge intégré.",
        "steam_app_id": "2430930",
        "store_app_id": 2399830,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"},
            {"port": 27020, "protocol": "tcp", "description": "Port RCON"}
        ],
        "default_memory_mb": 16384,
        "min_memory_mb": 10240,
        "startup_cmd": "wine ArkAscendedServer.exe {{SERVER_MAP}}?listen?SessionName=\"{{SERVER_NAME}}\"?ServerPassword=\"{{SERVER_PASSWORD}}\"?ServerAdminPassword=\"{{ADMIN_PASSWORD}}\"?Port={{SERVER_PORT}}?QueryPort={{QUERY_PORT}}?RCONPort={{RCON_PORT}} -server -log",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur ASA", "default_value": "Serveur ASA Noos NAS", "input_type": "text", "options": None},
            {"name": "Carte du monde", "env_variable": "SERVER_MAP", "description": "Nom de la carte", "default_value": "TheIsland_WP", "input_type": "select", "options": ["TheIsland_WP", "ScorchedEarth_WP", "TheCenter_WP", "Aberration_WP"]},
            {"name": "Mot de passe joueur", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe joueur", "default_value": "", "input_type": "password", "options": None},
            {"name": "Mot de passe Administrateur", "env_variable": "ADMIN_PASSWORD", "description": "Mot de passe admin", "default_value": "NoosAsaAdmin123!", "input_type": "password", "options": None},
            {"name": "Port Query", "env_variable": "QUERY_PORT", "description": "Port Steam Query", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Port RCON", "env_variable": "RCON_PORT", "description": "Port RCON", "default_value": "27020", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "garrys-mod",
        "name": "Garry's Mod Dedicated Server",
        "author": "Facepunch Studios & Noos NAS",
        "category": "Bac à sable Source",
        "icon": "🔧",
        "tagline": "Sandbox physique multijoueur légendaire sous Source Engine (TTT, DarkRP)",
        "description": "Serveur dédié SRCDS officiel pour Garry's Mod avec support complet du Steam Workshop, gamemodes communautaires (DarkRP, Trouble in Terrorist Town, Prop Hunt) et console FastDL.",
        "steam_app_id": "4020",
        "store_app_id": 4000,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [
            {"port": 27005, "protocol": "udp", "description": "Port client Source Engine"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./srcds_run -game garrysmod -console -port {{SERVER_PORT}} +maxplayers {{MAX_PLAYERS}} +map {{SRCDS_MAP}} +gamemode {{GAMEMODE}}",
        "variables": [
            {"name": "Nom de la carte de départ", "env_variable": "SRCDS_MAP", "description": "Carte initiale", "default_value": "gm_construct", "input_type": "text", "options": None},
            {"name": "Mode de jeu (Gamemode)", "env_variable": "GAMEMODE", "description": "Mode de jeu", "default_value": "sandbox", "input_type": "select", "options": ["sandbox", "terrortown", "darkrp", "prop_hunt"]},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Joueurs max", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "team-fortress-2",
        "name": "Team Fortress 2 Dedicated Server",
        "author": "Valve & Noos NAS",
        "category": "FPS Compétitif",
        "icon": "🎩",
        "tagline": "Le FPS par équipes légendaire de Valve aux 9 classes emblématiques",
        "description": "Serveur dédié officiel Source Engine pour Team Fortress 2. Compatible avec les modes de jeu occasionnels, compétitifs 6v6/Highlander, MvM (Mann vs Machine) et plugins SourceMod.",
        "steam_app_id": "232250",
        "store_app_id": 440,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [
            {"port": 27005, "protocol": "udp", "description": "Port client Source"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 1024,
        "startup_cmd": "./srcds_run -game tf -console -port {{SERVER_PORT}} +maxplayers {{MAX_PLAYERS}} +map {{SRCDS_MAP}}",
        "variables": [
            {"name": "Carte initiale", "env_variable": "SRCDS_MAP", "description": "Carte de démarrage", "default_value": "cp_badlands", "input_type": "text", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité max", "default_value": "24", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "left-4-dead-2",
        "name": "Left 4 Dead 2 Dedicated Server",
        "author": "Valve & Noos NAS",
        "category": "Horreur / Coopératif",
        "icon": "🧟‍♂️",
        "tagline": "Survivez à l'apocalypse zombie à 4 en coopération intense à travers le Sud des USA",
        "description": "Serveur dédié Valve SRCDS pour Left 4 Dead 2. Supporte les campagnes coopératives classiques, le mode Versus compétitif, Survival et Scavenge avec le Director IA.",
        "steam_app_id": "222860",
        "store_app_id": 550,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./srcds_run -game left4dead2 -console -port {{SERVER_PORT}} +maxplayers {{MAX_PLAYERS}} +map {{SRCDS_MAP}}",
        "variables": [
            {"name": "Carte de départ", "env_variable": "SRCDS_MAP", "description": "Campagne et chapitre initial", "default_value": "c1m1_hotel", "input_type": "text", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité joueurs (4 pour Coop, 8 pour Versus)", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "counter-strike-source",
        "name": "Counter-Strike: Source Dedicated Server",
        "author": "Valve & Noos NAS",
        "category": "FPS Compétitif",
        "icon": "💣",
        "tagline": "L'incontournable classique Source du combat terroristes contre antiterroristes",
        "description": "Serveur dédié classique Counter-Strike: Source pour des parties intenses en De_Dust2, GunGame, Zombie Escape ou Deathmatch avec intégration SourceMod / MetaMod.",
        "steam_app_id": "232330",
        "store_app_id": 240,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [],
        "default_memory_mb": 2048,
        "min_memory_mb": 1024,
        "startup_cmd": "./srcds_run -game cstrike -console -port {{SERVER_PORT}} +maxplayers {{MAX_PLAYERS}} +map {{SRCDS_MAP}}",
        "variables": [
            {"name": "Carte de démarrage", "env_variable": "SRCDS_MAP", "description": "Carte initiale", "default_value": "de_dust2", "input_type": "text", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité max de joueurs", "default_value": "20", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "conan-exiles",
        "name": "Conan Exiles Dedicated Server",
        "author": "Funcom & Noos NAS",
        "category": "Survie / Barbares",
        "icon": "⚔️",
        "tagline": "Survivez, bâtissez et dominez dans les Terres Exilées impitoyables de Conan",
        "description": "Serveur dédié multijoueur persistant Conan Exiles avec gestion des purges, esclaves, donjons, dieux colossaux et batailles sanglantes en monde ouvert.",
        "steam_app_id": "443030",
        "store_app_id": 440900,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 7778, "protocol": "udp", "description": "Port de jeu secondaire"},
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine ConanSandboxServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -log",
        "variables": [
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port de requête", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité max", "default_value": "40", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "sons-of-the-forest",
        "name": "Sons of the Forest Dedicated Server",
        "author": "Endnight Games & Noos NAS",
        "category": "Horreur / Survie",
        "icon": "🪓",
        "tagline": "Survivez aux cannibales et mutants sur une île isolée cauchemardesque",
        "description": "Serveur dédié officiel pour Sons of the Forest. Bâtissez des abris sophistiqués, explorez des grottes et survivez aux créatures mutantes en coop.",
        "steam_app_id": "2465200",
        "store_app_id": 1326470,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 8766,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port Steam Query"},
            {"port": 9700, "protocol": "udp", "description": "Port Blob"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine SonsOfTheForestDS.exe -userdataPath \"C:/users/steam/AppData/LocalLow/Endnight/SonsOfTheForestDS\"",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché aux joueurs", "default_value": "Serveur Sons of the Forest Noos NAS", "input_type": "text", "options": None},
            {"name": "Nombre de joueurs", "env_variable": "MAX_PLAYERS", "description": "Joueurs max (1-8)", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "the-forest",
        "name": "The Forest Dedicated Server",
        "author": "Endnight Games & Noos NAS",
        "category": "Horreur / Survie",
        "icon": "🌲",
        "tagline": "Construisez, explorez et survivez dans une forêt infestée de cannibales",
        "description": "Serveur dédié officiel pour The Forest. Après le crash de votre avion, coupez des arbres, bâtissez un camp fortifié et défendez-vous contre les cannibales de la péninsule.",
        "steam_app_id": "556450",
        "store_app_id": 242760,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 27016,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 8766, "protocol": "udp", "description": "Port communication"},
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "wine TheForestDedicatedServer.exe -batchmode -nographics -savefolderpath \"Saves\"",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "The Forest Noos NAS", "input_type": "text", "options": None},
            {"name": "Capacité maximale", "env_variable": "MAX_PLAYERS", "description": "Nombre max de survivants", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "unturned",
        "name": "Unturned Dedicated Server",
        "author": "Smartly Dressed Games & Noos NAS",
        "category": "Survie / Post-Apocalyptique",
        "icon": "🧟",
        "tagline": "Survie zombie voxel en monde ouvert avec artisanat, conduite et barricades",
        "description": "Serveur dédié officiel Unturned avec support des cartes officielles (PEI, Washington, Russia), mods du Workshop, conduite de véhicules et combats JcJ/JcE.",
        "steam_app_id": "1110100",
        "store_app_id": 304930,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port Query Steam"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./ServerHelper.sh -batchmode -nographics +LanServer/{{SERVER_NAME}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de l'instance serveur", "default_value": "Unturned Noos Server", "input_type": "text", "options": None},
            {"name": "Carte", "env_variable": "MAP_NAME", "description": "Carte du monde", "default_value": "PEI", "input_type": "select", "options": ["PEI", "Washington", "Russia", "Yukon", "Germany"]}
        ]
    },
    {
        "id": "core-keeper",
        "name": "Core Keeper Dedicated Server",
        "author": "Pugstorm & Noos NAS",
        "category": "Aventure / Sandbox 2D",
        "icon": "💎",
        "tagline": "Explorez une caverne sans fin de reliques, de créatures et de ressources en coop",
        "description": "Serveur dédié officiel Core Keeper pour explorer des cavernes procédurales souterraines, miner des minerais rares, terrasser des boss géants et bâtir une base souterraine florissante.",
        "steam_app_id": "1963720",
        "store_app_id": 1621690,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./_launch.sh -world 0 -port {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du monde", "env_variable": "WORLD_NAME", "description": "Nom de la sauvegarde", "default_value": "NoosWorld", "input_type": "text", "options": None},
            {"name": "Nombre max de joueurs", "env_variable": "MAX_PLAYERS", "description": "Joueurs max", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "dont-starve-together",
        "name": "Don't Starve Together Dedicated Server",
        "author": "Klei Entertainment & Noos NAS",
        "category": "Survie / Aventure",
        "icon": "🏕️",
        "tagline": "Explorez et survivez ensemble dans un univers hostile façonné à la main",
        "description": "Serveur dédié officiel Don't Starve Together avec prise en charge du clustering (Surface + Grottes simultanées), mods du Steam Workshop et saisons impitoyables.",
        "steam_app_id": "343050",
        "store_app_id": 322330,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 10999,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 11000, "protocol": "udp", "description": "Port de communication Cluster/Caves"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./dontstarve_dedicated_server_nullrenderer -console -cluster MyDediServer -shard Master",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du monde DST", "default_value": "Don't Starve Noos NAS", "input_type": "text", "options": None},
            {"name": "Mode de jeu", "env_variable": "GAME_MODE", "description": "Mode de survie", "default_value": "survival", "input_type": "select", "options": ["survival", "endless", "wilderness"]}
        ]
    },
    {
        "id": "barotrauma",
        "name": "Barotrauma Dedicated Server",
        "author": "FakeFish & Undertow Games & Noos NAS",
        "category": "Simulation / Sous-Marin",
        "icon": "🐙",
        "tagline": "Pilotez un sous-marin dans les profondeurs glaciales et hostiles d'Europe",
        "description": "Serveur dédié Barotrauma. En tant que membre d'équipage (capitaine, mécanicien, médecin ou traître), naviguez dans les profondeurs sous-marines d'une lune de Jupiter face aux monstres et aux fuites d'eau.",
        "steam_app_id": "1026340",
        "store_app_id": 602960,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./DedicatedServer -port {{SERVER_PORT}} -queryport {{QUERY_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché dans le lobby", "default_value": "Barotrauma Noos NAS Submarine", "input_type": "text", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port de requête", "default_value": "27016", "input_type": "number", "options": None},
            {"name": "Capacité équipage", "env_variable": "MAX_PLAYERS", "description": "Nombre max de marins", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "v-rising",
        "name": "V Rising Dedicated Server",
        "author": "Stunlock Studios & Noos NAS",
        "category": "Action RPG / Vampires",
        "icon": "🧛",
        "tagline": "Réveillez-vous en vampire, bâtissez votre château gothique et régnez sur Vardoran",
        "description": "Serveur dédié multijoueur officiel V Rising propulsé par Proton. Bâtissez une forteresse seigneuriale gothique, traquez les porteurs de sang V et combattez des rivaux sous la lune.",
        "steam_app_id": "1829350",
        "store_app_id": 1604030,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 9876,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 9877, "protocol": "udp", "description": "Port de requête Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine VRisingServer.exe -persistentDataPath \"Z:/home/container/save-data\" -serverName \"{{SERVER_NAME}}\" -saveName \"{{WORLD_NAME}}\" -logFile \"VRisingServer.log\"",
        "variables": [
            {"name": "Nom du serveur vampire", "env_variable": "SERVER_NAME", "description": "Nom du royaume", "default_value": "V Rising Noos NAS Realm", "input_type": "text", "options": None},
            {"name": "Nom de la sauvegarde", "env_variable": "WORLD_NAME", "description": "Nom du monde", "default_value": "world1", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe pour rejoindre", "default_value": "", "input_type": "password", "options": None}
        ]
    },
    {
        "id": "starbound",
        "name": "Starbound Dedicated Server",
        "author": "Chucklefish & Noos NAS",
        "category": "Sandbox Spatial 2D",
        "icon": "🌌",
        "tagline": "Explorez un univers procédural infini à bord de votre propre vaisseau spatial",
        "description": "Serveur dédié natif Linux pour Starbound. Visitez des milliers de planètes uniques, colonisez des mondes extraterrestres, affrontez des boss intergalactiques et échangez des artéfacts en multijoueur.",
        "steam_app_id": "211820",
        "store_app_id": 211820,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 21025,
        "port_protocol": "tcp",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./linux/starbound_server",
        "variables": [
            {"name": "Capacité maximale de joueurs", "env_variable": "MAX_PLAYERS", "description": "Nombre de passagers spatiaux", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "soulmask",
        "name": "Soulmask Dedicated Server",
        "author": "CampFire Studio & Noos NAS",
        "category": "Survie / Tribale",
        "icon": "🎭",
        "tagline": "Échappez au rituel sacrificiel et découvrez les secrets des masques ancestraux",
        "description": "Serveur dédié officiel Soulmask propulsé par Proton. Fondez une tribu, recrutez des guerriers indigènes avec des compétences spécialisées et maîtrisez la puissance des masques antiques.",
        "steam_app_id": "3017310",
        "store_app_id": 2646460,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 8777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port de requête Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine WSServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -EchoPort=18888 -log",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché", "default_value": "Soulmask Noos NAS Tribe", "input_type": "text", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Steam", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Mot de passe joueur", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe serveur", "default_value": "", "input_type": "password", "options": None}
        ]
    },
    {
        "id": "abiotic-factor",
        "name": "Abiotic Factor Dedicated Server",
        "author": "Deep Field Games & Noos NAS",
        "category": "Sci-Fi / Survie Coop",
        "icon": "☣️",
        "tagline": "Survivez en tant que scientifiques face à des anomalies paranormales en centre souterrain",
        "description": "Serveur dédié multijoueur Abiotic Factor propulsé par Proton. Fabriquez des gadgets scientifiques de fortune, repoussez les incursions interdimensionnelles et échappez-vous du complexe GATE.",
        "steam_app_id": "2857200",
        "store_app_id": 427410,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine AbioticFactor/Binaries/Win64/AbioticFactorServer-Win64-Shipping.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -MaxServerPlayers={{MAX_PLAYERS}} -WorldSaveName=\"{{WORLD_NAME}}\"",
        "variables": [
            {"name": "Nom du monde / sauvegarde", "env_variable": "WORLD_NAME", "description": "Nom de la partie", "default_value": "GateFacility", "input_type": "text", "options": None},
            {"name": "Port Query", "env_variable": "QUERY_PORT", "description": "Port Query Steam", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Nombre de scientifiques max", "env_variable": "MAX_PLAYERS", "description": "Joueurs max (1-6)", "default_value": "6", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "foundry",
        "name": "Foundry Dedicated Server",
        "author": "Channel 3 Entertainment & Noos NAS",
        "category": "Usine & Voxel",
        "icon": "🏭",
        "tagline": "Automatisez une usine colossale dans un monde voxel infini généré procéduralement",
        "description": "Serveur dédié officiel Foundry propulsé par Proton. Bâtissez des chaînes de convoyeurs automatisées géantes, minez des gisements massifs et optimisez des réseaux logistiques en coopération.",
        "steam_app_id": "2915550",
        "store_app_id": 983870,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 22500,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine FoundryDedicatedServer.exe -batchmode -nographics -port={{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de la manufacture", "default_value": "Foundry Noos NAS Factory", "input_type": "text", "options": None},
            {"name": "Capacité joueurs", "env_variable": "MAX_PLAYERS", "description": "Ingénieurs max", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "factorio",
        "name": "Factorio Headless Server",
        "author": "Wube Software & Noos NAS",
        "category": "Automatisation / Gestion",
        "icon": "⚙️",
        "tagline": "Construisez et défendez des usines automatisées géantes sur une planète hostile",
        "description": "Serveur dédié headless officiel haute performance pour Factorio. Automatisez chaînes d'assemblage, trains logistiques, raffinage de pétrole et défense contre les déchiqueteurs indigènes.",
        "steam_app_id": None,
        "store_app_id": 427520,
        "docker_image": "factoriotools/factorio:stable",
        "default_port": 34197,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "tcp", "description": "Port RCON pour commandes console"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./bin/x64/factorio --start-server-load-latest --port {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de votre usine", "default_value": "Factorio Noos NAS Server", "input_type": "text", "options": None},
            {"name": "Mot de passe joueur (Optionnel)", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None}
        ]
    },
    {
        "id": "space-engineers",
        "name": "Space Engineers Dedicated Server",
        "author": "Keen Software House & Noos NAS",
        "category": "Simulation Spatiale",
        "icon": "🚀",
        "tagline": "Construisez des vaisseaux, stations spatiales et avant-postes planétaires réalistes",
        "description": "Serveur dédié multijoueur Space Engineers propulsé par Proton. Physique réaliste des corps rigides, destruction volumétrique, saut hyperspatial et survie orbitale avec vos amis.",
        "steam_app_id": "298740",
        "store_app_id": 244850,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 27016,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 12288,
        "min_memory_mb": 6144,
        "startup_cmd": "wine DedicatedServer64/SpaceEngineersDedicated.exe -console -ignorelastsession",
        "variables": [
            {"name": "Nom du serveur spatial", "env_variable": "SERVER_NAME", "description": "Nom affiché dans le navigateur de serveurs", "default_value": "Space Engineers Noos NAS Station", "input_type": "text", "options": None},
            {"name": "Nombre maximum d'ingénieurs", "env_variable": "MAX_PLAYERS", "description": "Joueurs max", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "astroneer",
        "name": "Astroneer Dedicated Server",
        "author": "System Era Softworks & Noos NAS",
        "category": "Exploration Spatiale",
        "icon": "🧑‍🚀",
        "tagline": "Explorez et façonnez des mondes lointains à l'ère des grandes découvertes aérospatiales",
        "description": "Serveur dédié officiel Astroneer sous Proton. Déformez le terrain à volonté avec l'outil de terraformation, automatisez vos bases et construisez des fusées pour explorer les planètes du système solaire.",
        "steam_app_id": "728470",
        "store_app_id": 361420,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 8777,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "wine AstroServer.exe",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché", "default_value": "Astroneer Noos NAS Base", "input_type": "text", "options": None},
            {"name": "Capacité maximale", "env_variable": "MAX_PLAYERS", "description": "Astronautes max (1-8)", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "arma-3",
        "name": "Arma 3 Dedicated Server",
        "author": "Bohemia Interactive & Noos NAS",
        "category": "Simulation Militaire",
        "icon": "🪖",
        "tagline": "Simulation de combat militaire réaliste et tactique en monde ouvert gigantesque",
        "description": "Serveur dédié officiel Arma 3 Linux pour opérations militaires réalistes à grande échelle. Compatible avec Altis Life, Wasteland, Antistasi, Zeus et les mods communautaires ACE3 / TFAR.",
        "steam_app_id": "233780",
        "store_app_id": 107410,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 2302,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 2303, "protocol": "udp", "description": "Port de requête Steam Query"},
            {"port": 2304, "protocol": "udp", "description": "Port Steam"},
            {"port": 2305, "protocol": "udp", "description": "Port VoN (Voix)"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "./arma3server -port={{SERVER_PORT}} -config=server.cfg -world=empty",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur militaire", "default_value": "Arma 3 Noos NAS Battalion", "input_type": "text", "options": None},
            {"name": "Mot de passe administrateur", "env_variable": "ADMIN_PASSWORD", "description": "Mot de passe commande #login", "default_value": "NoosArmaAdmin123!", "input_type": "password", "options": None},
            {"name": "Nombre max de soldats", "env_variable": "MAX_PLAYERS", "description": "Capacité joueurs", "default_value": "32", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "dayz",
        "name": "DayZ Dedicated Server",
        "author": "Bohemia Interactive & Noos NAS",
        "category": "Survie Post-Apocalyptique",
        "icon": "☣️",
        "tagline": "Survivez à l'infection, aux autres survivants et à la famine en Tcherno",
        "description": "Serveur dédié multijoueur officiel DayZ propulsé par Proton. Carte gigantesque de Chernarus ou Livonia, gestion balistique réaliste, blessures, véhicules et survie sans concession.",
        "steam_app_id": "223350",
        "store_app_id": 221100,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 2302,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine DayZServer_x64.exe -config=serverDZ.cfg -port={{SERVER_PORT}} -profiles=profiles -BEpath=battleye",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur DayZ", "default_value": "DayZ Noos NAS Chernarus", "input_type": "text", "options": None},
            {"name": "Mot de passe Administrateur", "env_variable": "ADMIN_PASSWORD", "description": "Mot de passe RCON", "default_value": "NoosDayzAdmin123!", "input_type": "password", "options": None},
            {"name": "Nombre de survivants max", "env_variable": "MAX_PLAYERS", "description": "Capacité max", "default_value": "60", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "squad",
        "name": "Squad Dedicated Server",
        "author": "Offworld Industries & Noos NAS",
        "category": "FPS Tactique",
        "icon": "🎯",
        "tagline": "Combats tactiques par escouades combinées à grande échelle à 100 joueurs",
        "description": "Serveur dédié officiel pour Squad. Coopération obligatoire, communication radio locale/escouade, blindés lourds, logistique de bases avancées et combats d'infanterie réalistes.",
        "steam_app_id": "403240",
        "store_app_id": 393380,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7787,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27165, "protocol": "udp", "description": "Port de requête Steam Query"},
            {"port": 21114, "protocol": "tcp", "description": "Port de gestion RCON"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "./SquadGameServer.sh Port={{SERVER_PORT}} QueryPort={{QUERY_PORT}} RCONPORT={{RCON_PORT}} -log",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur Squad", "default_value": "Squad Noos NAS Community", "input_type": "text", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27165", "input_type": "number", "options": None},
            {"name": "Port RCON", "env_variable": "RCON_PORT", "description": "Port RCON", "default_value": "21114", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "mordhau",
        "name": "Mordhau Dedicated Server",
        "author": "Triternion & Noos NAS",
        "category": "Combat Médiéval",
        "icon": "⚔️",
        "tagline": "Combats médiévaux sanglants et précis à la première personne à grande échelle",
        "description": "Serveur dédié officiel pour Mordhau. Maîtrisez le système de combat directionnel au corps-à-corps, participez à des batailles médiévales intenses en Frontline et Invasion jusqu'à 64 joueurs.",
        "steam_app_id": "887010",
        "store_app_id": 868520,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"},
            {"port": 10000, "protocol": "tcp", "description": "Port RCON console"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "./MordhauServer.sh -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -RCONPort={{RCON_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de l'arène", "default_value": "Mordhau Noos NAS Duel & Battle", "input_type": "text", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Port RCON", "env_variable": "RCON_PORT", "description": "Port RCON", "default_value": "10000", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "killing-floor-2",
        "name": "Killing Floor 2 Dedicated Server",
        "author": "Tripwire Interactive & Noos NAS",
        "category": "Horreur / Coopératif",
        "icon": "🩸",
        "tagline": "Affrontez des vagues incessantes de spécimens mutants Zeds à 6 joueurs en coop",
        "description": "Serveur dédié multijoueur Killing Floor 2 Linux natif. Survivez à des vagues de monstres génétiquement modifiés avec vos amis, accumulez du Dosh et achetez de l'armement lourd.",
        "steam_app_id": "232130",
        "store_app_id": 232090,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"},
            {"port": 8080, "protocol": "tcp", "description": "Port WebAdmin d'administration"},
            {"port": 20560, "protocol": "udp", "description": "Port Steam Client"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./Binaries/Win64/KFGameSteamServer.bin.x86_64 KF-BioticsLab?Port={{SERVER_PORT}}?QueryPort={{QUERY_PORT}}?WebAdminPort={{WEBADMIN_PORT}}",
        "variables": [
            {"name": "Port WebAdmin", "env_variable": "WEBADMIN_PORT", "description": "Interface web de configuration", "default_value": "8080", "input_type": "number", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27015", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "insurgency-sandstorm",
        "name": "Insurgency: Sandstorm Dedicated Server",
        "author": "New World Interactive & Noos NAS",
        "category": "FPS Tactique",
        "icon": "🎯",
        "tagline": "FPS tactique hardcore en combats urbains au Moyen-Orient axé sur le jeu d'équipe",
        "description": "Serveur dédié Linux natif pour Insurgency: Sandstorm. Balistique mortelle en un tir, gestion des munitions par chargeurs, frappes d'artillerie et coopération tactique contre l'IA ou d'autres joueurs.",
        "steam_app_id": "581330",
        "store_app_id": 581320,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27102,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27131, "protocol": "udp", "description": "Port de requête Steam Query"},
            {"port": 27015, "protocol": "tcp", "description": "Port RCON"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "./Insurgency/Binaries/Linux/InsurgencyServer-Linux-Shipping Oilfield?Scenario=Scenario_Oilfield_Push_Security -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -RconPort={{RCON_PORT}} -log",
        "variables": [
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27131", "input_type": "number", "options": None},
            {"name": "Port RCON", "env_variable": "RCON_PORT", "description": "Port RCON", "default_value": "27015", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "assetto-corsa",
        "name": "Assetto Corsa Dedicated Server",
        "author": "Kunos Simulazioni & Noos NAS",
        "category": "Course / Simulation",
        "icon": "🏎️",
        "tagline": "Simulation de course automobile ultra-réaliste avec physique de pointe",
        "description": "Serveur dédié officiel Assetto Corsa propulsé par Proton. Organisez des championnats GT3, courses de drift, sessions de trackday multijoueur sur les circuits les plus réputés au monde.",
        "steam_app_id": "302550",
        "store_app_id": 244210,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 9600,
        "port_protocol": "both",
        "extra_ports": [
            {"port": 8081, "protocol": "tcp", "description": "Port HTTP Server AC"},
            {"port": 9601, "protocol": "udp", "description": "Port plugin UDP"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "wine acServer.exe",
        "variables": [
            {"name": "Nom de la session de course", "env_variable": "SERVER_NAME", "description": "Nom affiché dans le lobby", "default_value": "Assetto Corsa Noos NAS Trackday", "input_type": "text", "options": None},
            {"name": "Nombre max de pilotes", "env_variable": "MAX_PLAYERS", "description": "Pilotes simultanés", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "humanitz",
        "name": "HumanitZ Dedicated Server",
        "author": "Yodubzz Studios & Noos NAS",
        "category": "Survie Post-Apocalyptique",
        "icon": "🧟‍♀️",
        "tagline": "Survie en vue isométrique dans un monde ouvert envahi par les Zeeks",
        "description": "Serveur dédié multijoueur HumanitZ sous Proton. Fouillez les ruines des villes, réparez des véhicules, cultivez des terres et repoussez les hordes de zombies Zeeks.",
        "steam_app_id": "2595080",
        "store_app_id": 1774380,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "wine HumanitZServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -log",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "HumanitZ Noos NAS Outpost", "input_type": "text", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27015", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "icarus",
        "name": "Icarus Dedicated Server",
        "author": "RocketWerkz & Noos NAS",
        "category": "Survie Sci-Fi",
        "icon": "🪐",
        "tagline": "Survivez sur une planète terraformée hostile lors de missions chronométrées",
        "description": "Serveur dédié multijoueur Icarus sous Proton. Descendez en capsule orbitale sur une planète sauvage toxique, récoltez des matières exotiques et extrayez-vous avant la tempête.",
        "steam_app_id": "2089300",
        "store_app_id": 1149460,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 17777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 12288,
        "min_memory_mb": 6144,
        "startup_cmd": "wine IcarusServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -Log",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de la mission Icarus", "default_value": "Icarus Noos NAS Expedition", "input_type": "text", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27015", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "no-more-room-in-hell",
        "name": "No More Room in Hell Dedicated Server",
        "author": "Lever Games & Noos NAS",
        "category": "Horreur / Survie Coop",
        "icon": "💀",
        "tagline": "Survie réaliste et désespérée face à la mort vivante inspirée des films de Romero",
        "description": "Serveur dédié officiel Source Engine pour No More Room in Hell (NMRiH). Gestion réaliste sans viseur écran, munitions rares, morsures infectieuses mortelles et entraide vitale.",
        "steam_app_id": "317670",
        "store_app_id": 224260,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [],
        "default_memory_mb": 2048,
        "min_memory_mb": 1024,
        "startup_cmd": "./srcds_run -game nmrih -console -port {{SERVER_PORT}} +maxplayers {{MAX_PLAYERS}} +map {{SRCDS_MAP}}",
        "variables": [
            {"name": "Carte de départ", "env_variable": "SRCDS_MAP", "description": "Carte initiale", "default_value": "nmo_broadway", "input_type": "text", "options": None},
            {"name": "Nombre max de survivants", "env_variable": "MAX_PLAYERS", "description": "Capacité max (1-8)", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "eco",
        "name": "Eco Dedicated Server",
        "author": "Strange Loop Games & Noos NAS",
        "category": "Écologie & Civilisation",
        "icon": "🌱",
        "tagline": "Bâtissez une civilisation florissante pour détruire un météore sans ruiner l'écosystème",
        "description": "Serveur dédié officiel Eco Linux natif. Simulez une économie complète avec monnaie, lois démocratiques, pollution environnementale en temps réel et recherche technologique de pointe.",
        "steam_app_id": "739590",
        "store_app_id": 382310,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 3000,
        "port_protocol": "both",
        "extra_ports": [
            {"port": 3001, "protocol": "both", "description": "Port Web d'administration et d'écologie"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "./EcoServer -nogui",
        "variables": [
            {"name": "Nom du monde Eco", "env_variable": "SERVER_NAME", "description": "Nom de la planète", "default_value": "Eco Noos NAS Planet", "input_type": "text", "options": None}
        ]
    },
    {
        "id": "empyrion",
        "name": "Empyrion: Galactic Survival Dedicated Server",
        "author": "Eleon Game Studios & Noos NAS",
        "category": "Survie Galactique",
        "icon": "🚀",
        "tagline": "Aventure spatiale 3D avec exploration planétaire, construction et combats",
        "description": "Serveur dédié multijoueur Empyrion propulsé par Proton. Construisez des vaisseaux de combat de classe capitale (CV), des hovercrafts (HV), explorez des systèmes stellaires et colonisez des planètes aliens.",
        "steam_app_id": "530870",
        "store_app_id": 383120,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 30000,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 30001, "protocol": "udp", "description": "Port secondaire"},
            {"port": 30002, "protocol": "udp", "description": "Port Steam"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine EmpyrionDedicated.exe -batchmode -nographics -logFile logs/server.log",
        "variables": [
            {"name": "Nom de la partie galactique", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "Empyrion Noos NAS Galaxy", "input_type": "text", "options": None}
        ]
    },
    {
        "id": "stationeers",
        "name": "Stationeers Dedicated Server",
        "author": "RocketWerkz & Noos NAS",
        "category": "Ingénierie Spatiale",
        "icon": "🛰️",
        "tagline": "Gérez la pression, l'atmosphère et les circuits d'une station spatiale complexe",
        "description": "Serveur dédié officiel Stationeers Linux natif. Simulation détaillée de thermodynamique des gaz, réseau électrique, plomberie industrielle, logique programmable et survie sur la Lune ou Mars.",
        "steam_app_id": "600760",
        "store_app_id": 544550,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27016,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "./rocketstation_DedicatedServer.x86_64 -batchmode -nographics -load",
        "variables": [
            {"name": "Nom de la station", "env_variable": "SERVER_NAME", "description": "Nom affiché", "default_value": "Stationeers Noos NAS Outpost", "input_type": "text", "options": None},
            {"name": "Planète / Monde", "env_variable": "WORLD_TYPE", "description": "Environnement", "default_value": "Moon", "input_type": "select", "options": ["Moon", "Mars", "Europa", "Mimas", "Vulcan"]}
        ]
    },
    {
        "id": "stormworks",
        "name": "Stormworks: Build and Rescue Dedicated Server",
        "author": "Geometa & Noos NAS",
        "category": "Sauvetage / Véhicules",
        "icon": "🚁",
        "tagline": "Concevez hélicoptères, bateaux et sous-marins pour des missions de sauvetage héroïques",
        "description": "Serveur dédié Stormworks sous Proton. Concevez vos véhicules personnalisés de sauvetage maritime et aérien avec logique modulaire, moteurs thermiques réalistes et pilotez dans les tempêtes violentes.",
        "steam_app_id": "1247090",
        "store_app_id": 573090,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 25564,
        "port_protocol": "both",
        "extra_ports": [],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "wine server64.exe +server_dir \"server-data\"",
        "variables": [
            {"name": "Nom du serveur de sauvetage", "env_variable": "SERVER_NAME", "description": "Nom affiché", "default_value": "Stormworks Noos NAS Coastguard", "input_type": "text", "options": None}
        ]
    },
    {
        "id": "myth-of-empires",
        "name": "Myth of Empires Dedicated Server",
        "author": "Angela Game & Noos NAS",
        "category": "Sandbox Multijoueur Médiéval",
        "icon": "🏯",
        "tagline": "Bâtissez un empire oriental féodal, recrutez des armées et menez des sièges colossaux",
        "description": "Serveur dédié officiel Myth of Empires propulsé par Proton. Bâtissez des forteresses asiatiques monumentales, dressez des étalons de guerre, fabriquez des engins de siège et unifiez les contrées déchirées.",
        "steam_app_id": "1794810",
        "store_app_id": 1371580,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 12288,
        "min_memory_mb": 6144,
        "startup_cmd": "wine MOEServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -log",
        "variables": [
            {"name": "Nom de l'empire", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "Myth of Empires Noos NAS Kingdom", "input_type": "text", "options": None},
            {"name": "Port Query", "env_variable": "QUERY_PORT", "description": "Port Query Steam", "default_value": "27015", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "night-of-the-dead",
        "name": "Night of the Dead Dedicated Server",
        "author": "jacktostudios & Noos NAS",
        "category": "Tower Defense / Survie",
        "icon": "🧟‍♂️",
        "tagline": "Construisez une forteresse bardée de pièges mécaniques pour repousser les hordes nocturnes",
        "description": "Serveur dédié multijoueur Night of the Dead sous Proton. Bâtissez un bastion défensif automatisé (guillotine, pendule géant, lance-flammes) et survivez aux vagues de mutants nocturnes terrifiantes.",
        "steam_app_id": "1420710",
        "store_app_id": 1377360,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine LFServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}} -log",
        "variables": [
            {"name": "Nom du camp", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "Night of the Dead Noos NAS Stronghold", "input_type": "text", "options": None},
            {"name": "Port Query", "env_variable": "QUERY_PORT", "description": "Port Query Steam", "default_value": "27015", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "black-mesa",
        "name": "Black Mesa Dedicated Server",
        "author": "Crowbar Collective & Noos NAS",
        "category": "FPS Multijoueur",
        "icon": "☢️",
        "tagline": "Le remake officiel et modernisé du mythique Half-Life en affrontement multijoueur",
        "description": "Serveur dédié Linux SRCDS pour Black Mesa Multiplayer (BM:DM). Combattez au pied-de-biche, fusil à pompe et canon à gluons dans les laboratoires emblématiques du complexe Black Mesa.",
        "steam_app_id": "346680",
        "store_app_id": 362890,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "both",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./srcds_run -game bms -console -port {{SERVER_PORT}} +maxplayers {{MAX_PLAYERS}} +map {{SRCDS_MAP}}",
        "variables": [
            {"name": "Carte initiale", "env_variable": "SRCDS_MAP", "description": "Carte de départ", "default_value": "dm_bounce", "input_type": "text", "options": None},
            {"name": "Capacité joueurs", "env_variable": "MAX_PLAYERS", "description": "Nombre max de combattants", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "vintage-story",
        "name": "Vintage Story Dedicated Server",
        "author": "Anego Studios & Noos NAS",
        "category": "Survie / Voxel Réaliste",
        "icon": "⛏️",
        "tagline": "Survie hardcore intransigeante dans un monde voxel axée sur la géologie et l'artisanat",
        "description": "Serveur dédié multijoueur officiel pour Vintage Story. Prospérez à travers les âges (pierre, cuivre, bronze, fer), maîtrisez l'agriculture saisonnière, le travail de l'argile et la forge minutieuse.",
        "steam_app_id": None,
        "store_app_id": None,
        "docker_image": "ghcr.io/parkervcp/games:vintage-story",
        "default_port": 42420,
        "port_protocol": "tcp",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "mono VintagestoryServer.exe --dataPath /home/container/data",
        "variables": [
            {"name": "Nom du monde Vintage Story", "env_variable": "SERVER_NAME", "description": "Nom affiché aux pionniers", "default_value": "Vintage Story Noos NAS World", "input_type": "text", "options": None}
        ]
    }
]

def fetch_image(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return resp.read()
    except Exception as e:
        pass
    return None

def process_banner(game, egg_dir):
    banner_path = os.path.join(egg_dir, "banner.jpg")
    store_id = game.get("store_app_id")
    img_data = None
    
    if store_id:
        urls = [
            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{store_id}/library_hero.jpg",
            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{store_id}/header.jpg",
            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{store_id}/capsule_616x353.jpg",
        ]
        for u in urls:
            img_data = fetch_image(u)
            if img_data:
                break
    elif game["id"] == "vintage-story":
        # Official Vintage Story hero/screenshot
        urls = [
            "https://media.vintagestory.at/monthly_2024_12/2024-12-04_18-33-17.jpg.1d9a95995179fbf21292b3184ca44f63.jpg",
            "https://media.vintagestory.at/monthly_2024_12/2022-12-29_21-16-00.jpg.2891475dc036dbf5190cd09cc9812402.jpg"
        ]
        for u in urls:
            img_data = fetch_image(u)
            if img_data:
                break

    if not img_data:
        raise RuntimeError(f"Could not fetch banner for {game['id']}")

    # Convert / resize to 1920x620 JPEG
    img = Image.open(io.BytesIO(img_data)).convert("RGB")
    target_width, target_height = 1920, 620
    
    # Crop to ratio 1920:620 then resize
    target_ratio = target_width / target_height
    img_ratio = img.width / img.height
    
    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        offset = (img.width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img = img.crop((0, offset, img.width, offset + new_height))
        
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    img.save(banner_path, "JPEG", quality=90)
    print(f"✓ Saved banner for {game['id']}: 1920x620")

def process_icon(game, egg_dir):
    icon_path = os.path.join(egg_dir, "icon.png")
    store_id = game.get("store_app_id")
    img_data = None
    
    if store_id:
        urls = [
            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{store_id}/logo.png",
            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{store_id}/capsule_616x353.jpg",
            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{store_id}/header.jpg",
        ]
        for u in urls:
            img_data = fetch_image(u)
            if img_data:
                break
    elif game["id"] == "vintage-story":
        urls = [
            "https://media.vintagestory.at/monthly_2018_02/gamelogo-vintagestory-square.png.d938fbc6101feaae3bbc38019e392ff0.png",
            "https://media.vintagestory.at/monthly_2019_07/android-chrome-512x512.png?v=1711633522"
        ]
        for u in urls:
            img_data = fetch_image(u)
            if img_data:
                break

    if not img_data:
        raise RuntimeError(f"Could not fetch icon for {game['id']}")

    img = Image.open(io.BytesIO(img_data))
    if img.mode not in ("RGBA", "RGB"):
        img = img.convert("RGBA")
        
    # Resize keeping aspect ratio or standard 640x360 / 256x256
    # Let's save standard PNG
    img.save(icon_path, "PNG", optimize=True)
    print(f"✓ Saved icon for {game['id']}: {img.size}")

def build_all():
    # Load existing catalog.json
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    existing_eggs = {e["id"]: e for e in catalog.get("eggs", [])}
    print(f"Loaded {len(existing_eggs)} existing eggs from catalog.json")

    for g in NEW_GAMES:
        egg_id = g["id"]
        egg_dir = os.path.join(EGGS_DIR, egg_id)
        os.makedirs(egg_dir, exist_ok=True)

        process_banner(g, egg_dir)
        process_icon(g, egg_dir)

        egg_dict = {
            "id": g["id"],
            "name": g["name"],
            "author": g["author"],
            "category": g["category"],
            "icon": g["icon"],
            "tagline": g["tagline"],
            "description": g["description"],
            "icon_url": f"https://raw.githubusercontent.com/Chomiam/noos_nas_eggs/main/eggs/{egg_id}/icon.png",
            "banner_url": f"https://raw.githubusercontent.com/Chomiam/noos_nas_eggs/main/eggs/{egg_id}/banner.jpg",
            "steam_app_id": g["steam_app_id"],
            "docker_image": g["docker_image"],
            "default_port": g["default_port"],
            "port_protocol": g["port_protocol"],
            "extra_ports": g["extra_ports"],
            "default_memory_mb": g["default_memory_mb"],
            "min_memory_mb": g["min_memory_mb"],
            "startup_cmd": g["startup_cmd"],
            "variables": g["variables"],
            "is_custom": False
        }

        # Write egg.json
        egg_json_path = os.path.join(egg_dir, "egg.json")
        with open(egg_json_path, "w", encoding="utf-8") as ef:
            json.dump(egg_dict, ef, indent=2, ensure_ascii=False)
            ef.write("\n")

        existing_eggs[egg_id] = egg_dict

    # Reassemble catalog
    all_eggs_sorted = sorted(existing_eggs.values(), key=lambda x: x["name"])
    catalog["version"] = "1.2.0"
    catalog["last_updated"] = "2026-10-06T12:00:00Z"
    catalog["total_eggs"] = len(all_eggs_sorted)
    catalog["eggs"] = all_eggs_sorted

    with open(CATALOG_PATH, "w", encoding="utf-8") as cf:
        json.dump(catalog, cf, indent=2, ensure_ascii=False)
        cf.write("\n")

    print(f"\n🎉 Successfully updated catalog.json with {len(all_eggs_sorted)} total eggs!")

if __name__ == "__main__":
    build_all()
