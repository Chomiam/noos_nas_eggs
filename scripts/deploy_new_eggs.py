#!/usr/bin/env python3
"""
deploy_new_eggs.py - Scrapes, formats, validates and registers 21 new game eggs
into the noos_nas_eggs repository and catalog.json.
Ensures official Steam CDN / publisher assets (1920x620 banner.jpg, icon.png) are retrieved.
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

NEW_GAMES_BATCH = [
    {
        "id": "beamng-beammp",
        "name": "BeamNG.drive (BeamMP Dedicated Server)",
        "author": "BeamMP & BeamNG GmbH",
        "category": "Simulation / Automobile",
        "icon": "🚗",
        "tagline": "Serveur multijoueur officiel BeamMP pour BeamNG.drive avec physique ultra-réaliste",
        "description": "Serveur dédié multijoueur haute performance BeamMP pour BeamNG.drive permettant d'héberger des sessions de conduite libre, courses et crashs synchronisés entre amis.",
        "steam_app_id": None,
        "store_app_id": 284160,
        "docker_image": "ghcr.io/parkervcp/yolks:debian",
        "default_port": 8999,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 8999, "protocol": "tcp", "description": "Port d'authentification BeamMP"}
        ],
        "default_memory_mb": 2048,
        "min_memory_mb": 512,
        "startup_cmd": "./BeamMP-Server",
        "variables": [
            {"name": "Clé d'authentification AuthKey (obtenue sur beammp.com)", "env_variable": "AUTH_KEY", "description": "Clé secrète d'enregistrement BeamMP", "default_value": "", "input_type": "password", "options": None},
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché dans la liste des serveurs", "default_value": "Serveur BeamMP Noos NAS", "input_type": "text", "options": None},
            {"name": "Carte par défaut", "env_variable": "MAP", "description": "Chemin de la carte", "default_value": "/levels/gridmap_v2/info.json", "input_type": "text", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité max de joueurs", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "truck-simulator",
        "name": "Euro Truck Simulator 2 & ATS Dedicated Server",
        "author": "SCS Software & Noos NAS",
        "category": "Simulation / Convois",
        "icon": "🚛",
        "tagline": "Serveur de convoi persistant officiel pour Euro Truck Simulator 2 et American Truck Simulator",
        "description": "Serveur dédié officiel SCS Software pour héberger des sessions de convoi multijoueur permanentes sans dépendre d'un joueur hôte.",
        "steam_app_id": "1948160",
        "store_app_id": 227300,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27015,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port de requête secondaire Steam"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./bin/linux_x64/eurotrucks2_server",
        "variables": [
            {"name": "Nom du convoi", "env_variable": "SERVER_NAME", "description": "Nom du convoi affiché en jeu", "default_value": "Convoi Noos NAS", "input_type": "text", "options": None},
            {"name": "Mot de passe de session", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès (optionnel)", "default_value": "", "input_type": "password", "options": None},
            {"name": "Code de connexion Logon Code", "env_variable": "LOGON_CODE", "description": "Code généré depuis la console Steam de l'hôte", "default_value": "", "input_type": "text", "options": None},
            {"name": "Nombre maximum de camions", "env_variable": "MAX_PLAYERS", "description": "Nombre de camions dans le convoi", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "wreckfest",
        "name": "Wreckfest Dedicated Server",
        "author": "Bugbear Entertainment & Noos NAS",
        "category": "Course / Destruction",
        "icon": "🏁",
        "tagline": "Courses de banger et derbies de démolition avec gestion de dégâts poussée",
        "description": "Serveur dédié multijoueur officiel pour Wreckfest avec rotation de circuits, modes derby, gestion des collisions et bots personnalisables.",
        "steam_app_id": "361580",
        "store_app_id": 228380,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 27015,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port de requête Steam Query"},
            {"port": 33540, "protocol": "udp", "description": "Port local de communication"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 4096,
        "startup_cmd": "wine Wreckfest.exe -s server_config.cfg",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur affiché", "default_value": "Serveur Wreckfest Noos NAS", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Nombre max de pilotes", "default_value": "24", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "scpsl",
        "name": "SCP: Secret Laboratory Dedicated Server",
        "author": "Northwood Studios & Noos NAS",
        "category": "Horreur / Survie Multijoueur",
        "icon": "👁️",
        "tagline": "Survivez aux anomalies du site de confinement ou éliminez les intrus",
        "description": "Serveur dédié officiel pour SCP: Secret Laboratory sous Linux natif avec gestion des rôles (Classe D, Scientifiques, FIM, Chaos Insurgency et entités SCP).",
        "steam_app_id": "996560",
        "store_app_id": 700330,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./LocalAdmin {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché sur la liste publique SCP", "default_value": "Serveur SCP:SL Noos NAS", "input_type": "text", "options": None},
            {"name": "Nombre maximum de joueurs", "env_variable": "MAX_PLAYERS", "description": "Capacité max de joueurs", "default_value": "20", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "mount-and-blade-bannerlord",
        "name": "Mount & Blade II: Bannerlord Dedicated Server",
        "author": "TaleWorlds Entertainment & Noos NAS",
        "category": "Action / Médiéval & Stratégie",
        "icon": "⚔️",
        "tagline": "Affrontements et sièges de châteaux massifs dans l'univers de Calradia",
        "description": "Serveur dédié multijoueur pour Mount & Blade II: Bannerlord supportant les modes Siège, Capitaine, Escarmouche et Bataille avec des dizaines de combattants.",
        "steam_app_id": "1863440",
        "store_app_id": 261550,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7210,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine TaleWorlds.MountAndBlade.DedicatedCustomServer.exe _MODULES_*Native*Multiplayer*_MODULES_",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de la bataille dans le lobby", "default_value": "Serveur Bannerlord Noos NAS", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité de joueurs", "default_value": "64", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "necesse",
        "name": "Necesse Dedicated Server",
        "author": "Mads Skovgaard & FairPlay Studios",
        "category": "Aventure / Action-RPG",
        "icon": "🗡️",
        "tagline": "Explorez des îles infinies, recrutez des colons et battez des boss légendaires",
        "description": "Serveur dédié officiel pour Necesse avec monde procédural infini, gestion de colonies de PNJ automatisées et combats coopératifs.",
        "steam_app_id": "1169370",
        "store_app_id": 1169040,
        "docker_image": "ghcr.io/pterodactyl/yolks:java_21",
        "default_port": 14159,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 3072,
        "min_memory_mb": 1024,
        "startup_cmd": "java -jar Server.jar -port {{SERVER_PORT}} -world {{WORLD_NAME}}",
        "variables": [
            {"name": "Nom du monde", "env_variable": "WORLD_NAME", "description": "Nom du fichier de sauvegarde", "default_value": "MondeNoos", "input_type": "text", "options": None},
            {"name": "Mot de passe serveur", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe de protection", "default_value": "", "input_type": "password", "options": None},
            {"name": "Nombre maximum de colons/joueurs", "env_variable": "MAX_PLAYERS", "description": "Nombre de joueurs autorisés", "default_value": "10", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "lotr-return-to-moria",
        "name": "The Lord of the Rings: Return to Moria Dedicated Server",
        "author": "Free Range Games & North Beach Games",
        "category": "Survie / Fantasy & Co-op",
        "icon": "⛏️",
        "tagline": "Reconquérez et reconstruisez le royaume perdu de la Moria avec vos compagnons nains",
        "description": "Serveur dédié officiel pour Return to Moria avec génération procédurale des profondeurs de Khazad-dûm, minage, forge et combats contre les orques.",
        "steam_app_id": "3087260",
        "store_app_id": 2933400,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine MoriaServer.exe -Port={{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché dans la liste des serveurs", "default_value": "Moria Noos NAS", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Nombre max de nains", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "the-front",
        "name": "The Front Dedicated Server",
        "author": "Samar Studio & Noos NAS",
        "category": "Survie / Militaire & Sandbox",
        "icon": "🛡️",
        "tagline": "Guerre post-apocalyptique, véhicules blindés, tourelles et défense de base contre les vagues",
        "description": "Serveur dédié officiel pour The Front sous Unreal Engine permettant de concevoir des bases imprenables, fabriquer des chars/hélicoptères et repousser des hordes hostiles.",
        "steam_app_id": "2612550",
        "store_app_id": 2285150,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port de requête Steam Query"}
        ],
        "default_memory_mb": 10240,
        "min_memory_mb": 6144,
        "startup_cmd": "wine TheFrontServer.exe -Port={{SERVER_PORT}} -QueryPort={{QUERY_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur The Front", "default_value": "Serveur The Front Noos NAS", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Port Query Steam", "env_variable": "QUERY_PORT", "description": "Port Query", "default_value": "27015", "input_type": "number", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max de joueurs", "default_value": "32", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "avorion",
        "name": "Avorion Dedicated Server",
        "author": "Boxelware & Noos NAS",
        "category": "Espace / Bac à Sable",
        "icon": "🚀",
        "tagline": "Construisez votre vaisseau spatial voxel, formez des flottes et conquérez la galaxie",
        "description": "Serveur dédié natif Linux pour Avorion avec simulation spatiale dynamique, économie procédurale, combats de factions et commerce galactique multijoueur.",
        "steam_app_id": "565060",
        "store_app_id": 445220,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 27000,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27003, "protocol": "udp", "description": "Port Steam Query"},
            {"port": 27020, "protocol": "tcp", "description": "Port RCON"}
        ],
        "default_memory_mb": 6144,
        "min_memory_mb": 2048,
        "startup_cmd": "./server.sh --galaxy-name {{GALAXY_NAME}} --port {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom de la galaxie", "env_variable": "GALAXY_NAME", "description": "Nom de la galaxie sauvegardée", "default_value": "GalaxieNoos", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe de connexion", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité maximale de capitaines", "default_value": "10", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "subnautica-nitrox",
        "name": "Subnautica (Nitrox Multiplayer Server)",
        "author": "Nitrox Team & Unknown Worlds",
        "category": "Survie / Exploration Sous-Marine",
        "icon": "🌊",
        "tagline": "Explorez les fonds marins de la planète 4546B en coopération avec le mod Nitrox",
        "description": "Serveur dédié pour le mod multijoueur Nitrox de Subnautica permettant la construction conjointe de bases sous-marines et l'exploration synchronisée.",
        "steam_app_id": None,
        "store_app_id": 264710,
        "docker_image": "ghcr.io/parkervcp/yolks:debian",
        "default_port": 11000,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "./NitroxServer --port {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom de la partie", "default_value": "Monde Sous-Marin Noos", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Plongeurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Nombre de joueurs", "default_value": "4", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "veloren",
        "name": "Veloren Dedicated Server",
        "author": "Veloren Community (100% Rust)",
        "category": "RPG / Voxel Open-Source (Rust)",
        "icon": "🌲",
        "tagline": "RPG multijoueur open-source développé en Rust dans un monde féérique en voxels",
        "description": "Serveur officiel pour Veloren, le magnifique jeu de rôle open-source écrit en Rust inspiré de Cube World, Dwarf Fortress et Breath of the Wild.",
        "steam_app_id": None,
        "store_app_id": None,
        "custom_icon_url": "https://veloren.net/images/Logo_Square.png",
        "custom_banner_url": "https://veloren.net/processed_images/gallery-0.50cacb0aa6b9efab.jpg",
        "docker_image": "ghcr.io/parkervcp/yolks:debian",
        "default_port": 14004,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 3072,
        "min_memory_mb": 1024,
        "startup_cmd": "./veloren-server-cli",
        "variables": [
            {"name": "Description du serveur", "env_variable": "SERVER_NAME", "description": "Nom du monde Veloren", "default_value": "Monde Veloren Noos NAS (Rust)", "input_type": "text", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max d'aventuriers", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "mindustry",
        "name": "Mindustry Dedicated Server",
        "author": "Anuken & Noos NAS",
        "category": "Stratégie / Logistique & Usines",
        "icon": "⚙️",
        "tagline": "Gestion de convoyeurs, production industrielle et défense de base multijoueur",
        "description": "Serveur dédié officiel pour Mindustry, le hit de gestion logistique et de tower defense open-source avec crossplay total PC et mobiles.",
        "steam_app_id": None,
        "store_app_id": 1127400,
        "docker_image": "ghcr.io/pterodactyl/yolks:java_21",
        "default_port": 6567,
        "port_protocol": "tcp",
        "extra_ports": [
            {"port": 6567, "protocol": "udp", "description": "Port de découverte réseau Mindustry"}
        ],
        "default_memory_mb": 1536,
        "min_memory_mb": 512,
        "startup_cmd": "java -jar server.jar port {{SERVER_PORT}} host {{MAP}}",
        "variables": [
            {"name": "Nom du secteur/serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "Usine Mindustry Noos", "input_type": "text", "options": None},
            {"name": "Carte de départ", "env_variable": "MAP", "description": "Nom de la carte", "default_value": "groundZero", "input_type": "text", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Nombre de joueurs", "default_value": "16", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "spacestation-14",
        "name": "Space Station 14 Dedicated Server",
        "author": "Space Wizards Federation",
        "category": "Simulation / Jeu de Rôle Spatial",
        "icon": "🛸",
        "tagline": "Remake moderne et chaotique en C# de Space Station 13 à bord d'une station de recherche",
        "description": "Serveur dédié pour Space Station 14 avec simulation physique d'atmosphère, gestion de réacteur, chimie, traîtres infiltrés et rôles de bord complets.",
        "steam_app_id": None,
        "store_app_id": 1255460,
        "docker_image": "ghcr.io/parkervcp/yolks:debian",
        "default_port": 1212,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 3072,
        "min_memory_mb": 1024,
        "startup_cmd": "./Robust.Server --config cvars.cfg",
        "variables": [
            {"name": "Nom de la station", "env_variable": "SERVER_NAME", "description": "Nom du vaisseau/station", "default_value": "Station Noos-14", "input_type": "text", "options": None},
            {"name": "Membres d'équipage maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max", "default_value": "32", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "openttd",
        "name": "OpenTTD Dedicated Server",
        "author": "OpenTTD Team",
        "category": "Gestion / Transports & Trains",
        "icon": "🚆",
        "tagline": "Le simulateur de réseau ferroviaire et de transport de marchandises légendaire",
        "description": "Serveur dédié multijoueur pour OpenTTD pour créer des réseaux de trains, camions, bateaux et avions en compétition ou coopération économique permanente.",
        "steam_app_id": None,
        "store_app_id": 1536610,
        "docker_image": "ghcr.io/parkervcp/yolks:debian",
        "default_port": 3979,
        "port_protocol": "tcp",
        "extra_ports": [
            {"port": 3979, "protocol": "udp", "description": "Port de découverte réseau OpenTTD"}
        ],
        "default_memory_mb": 1024,
        "min_memory_mb": 256,
        "startup_cmd": "openttd -D -p {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom de la compagnie/serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur", "default_value": "Réseau Ferré Noos", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Nombre max d'entreprises", "env_variable": "MAX_PLAYERS", "description": "Nombre max d'entreprises", "default_value": "15", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "pavlov-vr",
        "name": "Pavlov VR Dedicated Server",
        "author": "Vankrupt Games & Noos NAS",
        "category": "VR / Tir Tactique",
        "icon": "🥽",
        "tagline": "Le FPS tactique compétitif numéro 1 en réalité virtuelle",
        "description": "Serveur dédié multijoueur officiel pour Pavlov VR avec support des modes Recherche & Destruction, Deathmatch, TTT et cartes personnalisées du Workshop.",
        "steam_app_id": "622970",
        "store_app_id": 555160,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 6144,
        "min_memory_mb": 3072,
        "startup_cmd": "./PavlovServer.sh -PORT={{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom affiché dans la liste des serveurs VR", "default_value": "Pavlov VR Noos NAS", "input_type": "text", "options": None},
            {"name": "Carte par défaut", "env_variable": "MAP", "description": "Nom de la carte de départ", "default_value": "datacenter", "input_type": "text", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Nombre max de casques", "default_value": "10", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "sunkenland",
        "name": "Sunkenland Dedicated Server",
        "author": "Vector3 Studio & Noos NAS",
        "category": "Survie / Océan & Exploration",
        "icon": "🤿",
        "tagline": "Survie post-apocalyptique dans un monde submergé : plongée, bases flottantes et raids",
        "description": "Serveur dédié pour Sunkenland avec exploration de villes englouties, confection d'armes, véhicules maritimes et défense contre les pirates.",
        "steam_app_id": "2631960",
        "store_app_id": 2080690,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 27015,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27016, "protocol": "udp", "description": "Port de requête Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine SunkenlandServer.exe -Port={{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du monde aquatique", "env_variable": "WORLD_NAME", "description": "Nom du monde", "default_value": "AtollNoos", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max de survivants", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "bellwright",
        "name": "Bellwright Dedicated Server",
        "author": "Donkey Crew & Snail Games",
        "category": "Survie / Médiéval & Gestion",
        "icon": "🏰",
        "tagline": "Fondez votre village, libérez le royaume et menez vos villageois au combat",
        "description": "Serveur dédié officiel pour Bellwright avec gestion de colonie médiévale, chaîne logistique, construction modulaire et batailles de libération.",
        "steam_app_id": "2984920",
        "store_app_id": 1812450,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "wine BellwrightServer.exe -Port={{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du village/serveur", "env_variable": "SERVER_NAME", "description": "Nom du royaume", "default_value": "Royaume Noos", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "raft",
        "name": "Raft Dedicated Server",
        "author": "Redbeet Interactive & Axolot Games",
        "category": "Survie / Océan & Co-op",
        "icon": "🦈",
        "tagline": "Survivez sur un radeau de fortune, pêchez les débris et découvrez les secrets de l'océan",
        "description": "Serveur dédié persistant pour Raft permettant à une équipe d'aventuriers de maintenir leur radeau et leurs expéditions sans interruption.",
        "steam_app_id": "648800",
        "store_app_id": 648800,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 27015,
        "port_protocol": "udp",
        "extra_ports": [],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "wine Raft.exe -batchmode -nographics",
        "variables": [
            {"name": "Nom du radeau/sauvegarde", "env_variable": "WORLD_NAME", "description": "Nom de la sauvegarde", "default_value": "RadeauNoos", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Nombre de naufragés", "default_value": "8", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "arma-reforger",
        "name": "Arma Reforger Dedicated Server",
        "author": "Bohemia Interactive & Noos NAS",
        "category": "MilSim / Tir Tactique",
        "icon": "🎖️",
        "tagline": "Guerre froide sur l'île d'Everon propulsée par le tout nouveau moteur Enfusion",
        "description": "Serveur dédié officiel pour Arma Reforger sous moteur Enfusion avec simulation militaire réaliste, capture de zones et support des mods Workshop.",
        "steam_app_id": "1874900",
        "store_app_id": 1874880,
        "docker_image": "ghcr.io/parkervcp/steamcmd:debian",
        "default_port": 2001,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 17777, "protocol": "udp", "description": "Port de requête Steam Query"}
        ],
        "default_memory_mb": 8192,
        "min_memory_mb": 4096,
        "startup_cmd": "./ArmaReforgerServer -config ./server.json -port {{SERVER_PORT}}",
        "variables": [
            {"name": "Nom de l'opération/serveur", "env_variable": "SERVER_NAME", "description": "Nom dans le navigateur de serveurs", "default_value": "Opération Noos Reforger", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe d'accès", "default_value": "", "input_type": "password", "options": None},
            {"name": "Nombre de soldats max", "env_variable": "MAX_PLAYERS", "description": "Capacité max", "default_value": "32", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "scum",
        "name": "SCUM Dedicated Server",
        "author": "Gamepires & Jagex",
        "category": "Survie / Réalisme Extrême",
        "icon": "🩸",
        "tagline": "Survie pénitentiaire hyper-réaliste sur une île impitoyable avec métabolisme poussé",
        "description": "Serveur dédié officiel pour SCUM avec gestion détaillée de la nutrition, balistique avancée, crafting et affrontements PvP/PvE intenses.",
        "steam_app_id": "2765340",
        "store_app_id": 513710,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 7777,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 27015, "protocol": "udp", "description": "Port de requête Steam Query"}
        ],
        "default_memory_mb": 10240,
        "min_memory_mb": 6144,
        "startup_cmd": "wine SCUMServer.exe -Port={{SERVER_PORT}}",
        "variables": [
            {"name": "Nom du serveur", "env_variable": "SERVER_NAME", "description": "Nom du serveur pénitentiaire", "default_value": "Prison de l'Île Noos SCUM", "input_type": "text", "options": None},
            {"name": "Mot de passe", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe", "default_value": "", "input_type": "password", "options": None},
            {"name": "Joueurs Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max de détenus", "default_value": "32", "input_type": "number", "options": None}
        ]
    },
    {
        "id": "assetto-corsa-competizione",
        "name": "Assetto Corsa Competizione (GT3) Dedicated Server",
        "author": "Kunos Simulazioni & 505 Games",
        "category": "Simulation / Course GT3",
        "icon": "🏎️",
        "tagline": "La simulation officielle des championnats GT World Challenge avec météo dynamique",
        "description": "Serveur dédié officiel pour Assetto Corsa Competizione avec physique de pointe GT3/GT4, gestion météo dynamique, arrêts aux stands et règlements officiels.",
        "steam_app_id": "805550",
        "store_app_id": 805550,
        "docker_image": "ghcr.io/parkervcp/steamcmd:proton",
        "default_port": 9231,
        "port_protocol": "udp",
        "extra_ports": [
            {"port": 9232, "protocol": "tcp", "description": "Port TCP de gestion"},
            {"port": 9232, "protocol": "udp", "description": "Port UDP de télémétrie"}
        ],
        "default_memory_mb": 4096,
        "min_memory_mb": 2048,
        "startup_cmd": "wine accServer.exe",
        "variables": [
            {"name": "Nom du salon GT3", "env_variable": "SERVER_NAME", "description": "Nom du salon", "default_value": "Championnat GT3 Noos NAS", "input_type": "text", "options": None},
            {"name": "Mot de passe pilote", "env_variable": "SERVER_PASSWORD", "description": "Mot de passe de session", "default_value": "", "input_type": "password", "options": None},
            {"name": "Mot de passe administrateur", "env_variable": "ADMIN_PASSWORD", "description": "Mot de passe admin", "default_value": "NoosAccAdmin123!", "input_type": "password", "options": None},
            {"name": "Pilotes Maximum", "env_variable": "MAX_PLAYERS", "description": "Capacité max de la grille", "default_value": "24", "input_type": "number", "options": None}
        ]
    }
]

def fetch_image(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
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
    elif game.get("custom_banner_url"):
        img_data = fetch_image(game["custom_banner_url"])

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
    elif game.get("custom_icon_url"):
        img_data = fetch_image(game["custom_icon_url"])

    if not img_data:
        raise RuntimeError(f"Could not fetch icon for {game['id']}")

    img = Image.open(io.BytesIO(img_data))
    if img.mode not in ("RGBA", "RGB"):
        img = img.convert("RGBA")
        
    img.save(icon_path, "PNG", optimize=True)
    print(f"✓ Saved icon for {game['id']}: {img.size}")

def deploy():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    existing_eggs = {e["id"]: e for e in catalog.get("eggs", [])}
    print(f"Starting deployment. Currently {len(existing_eggs)} eggs in catalog.")

    for g in NEW_GAMES_BATCH:
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

        egg_json_path = os.path.join(egg_dir, "egg.json")
        with open(egg_json_path, "w", encoding="utf-8") as ef:
            json.dump(egg_dict, ef, indent=2, ensure_ascii=False)
            ef.write("\n")

        existing_eggs[egg_id] = egg_dict

    all_eggs_sorted = sorted(existing_eggs.values(), key=lambda x: x["name"])
    catalog["version"] = "1.3.0"
    catalog["last_updated"] = "2026-10-06T17:00:00Z"
    catalog["total_eggs"] = len(all_eggs_sorted)
    catalog["eggs"] = all_eggs_sorted

    with open(CATALOG_PATH, "w", encoding="utf-8") as cf:
        json.dump(catalog, cf, indent=2, ensure_ascii=False)
        cf.write("\n")

    print(f"\n🎉 Successfully deployed {len(NEW_GAMES_BATCH)} new eggs! Catalog now has {len(all_eggs_sorted)} total eggs.")

if __name__ == "__main__":
    deploy()
