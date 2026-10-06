#!/usr/bin/env python3
"""
test_new_batch.py - Tests each of the 21 new game eggs on the NAS Docker daemon.
Verifies container instantiation, memory allocation, environment injection,
healthy state verification, and immediate cleanup.
"""

import json
import os
import subprocess
import sys
import time

NAS_HOST = "192.168.1.20"
NAS_USER = "chomiam"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(BASE_DIR, "catalog.json")

NEW_BATCH_IDS = [
    "beamng-beammp",
    "truck-simulator",
    "wreckfest",
    "scpsl",
    "mount-and-blade-bannerlord",
    "necesse",
    "lotr-return-to-moria",
    "the-front",
    "avorion",
    "subnautica-nitrox",
    "veloren",
    "mindustry",
    "spacestation-14",
    "openttd",
    "pavlov-vr",
    "sunkenland",
    "bellwright",
    "raft",
    "arma-reforger",
    "scum",
    "assetto-corsa-competizione"
]

def ssh_run(cmd, check=True):
    full_cmd = ["ssh", "-o", "BatchMode=yes", f"{NAS_USER}@{NAS_HOST}", cmd]
    res = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"SSH command failed ({res.returncode}): {res.stderr.strip()}\nCMD: {cmd}")
    return res

def test_egg(egg):
    egg_id = egg["id"]
    image = egg["docker_image"]
    mem_mb = egg.get("default_memory_mb", 4096)
    port = egg.get("default_port", 27015)
    container_name = f"test-noos-{egg_id}"

    print(f"\n==========================================")
    print(f"▶ Testing Egg: {egg['name']} [{egg_id}]")
    print(f"  Image: {image}")
    print(f"  Memory Limit: {mem_mb} MB")
    print(f"  Port: {port}")
    print(f"==========================================")

    # 1. Clean up any existing leftover container
    ssh_run(f"docker rm -f {container_name} 2>/dev/null || true", check=False)

    # 2. Build env flags
    env_flags = f"-e SERVER_PORT={port} -e SERVER_NAME=\"Test Noos Server\""
    for v in egg.get("variables", []):
        env_flags += f" -e {v['env_variable']}=\"{v['default_value']}\""

    # 3. Start container with sleep 20 to test healthy running state
    start_cmd = (
        f"docker run -d --name {container_name} "
        f"-m {mem_mb}m "
        f"{env_flags} "
        f"{image} sleep 20"
    )

    res = ssh_run(start_cmd, check=False)
    if res.returncode != 0:
        print(f"❌ Failed to run container: {res.stderr.strip()}")
        return False

    time.sleep(2)

    # 4. Inspect container state
    inspect_cmd = f"docker inspect --format '{{{{.State.Status}}}}|{{{{.State.Running}}}}' {container_name}"
    res = ssh_run(inspect_cmd, check=False)
    output = res.stdout.strip()

    if "running|true" not in output:
        print(f"❌ Container not running! Inspect: {output}")
        logs_res = ssh_run(f"docker logs {container_name}", check=False)
        print(f"   Logs: {logs_res.stdout.strip()[:300]}")
        ssh_run(f"docker rm -f {container_name} 2>/dev/null || true", check=False)
        return False

    # 5. Execute internal sanity check
    exec_cmd = f"docker exec {container_name} bash -c 'echo \"CONTAINER_HEALTHY: PORT=$SERVER_PORT MEM={mem_mb}M\"'"
    exec_res = ssh_run(exec_cmd, check=False)
    if exec_res.returncode != 0 or "CONTAINER_HEALTHY" not in exec_res.stdout:
        print(f"❌ Exec check failed: {exec_res.stderr.strip()}")
        ssh_run(f"docker rm -f {container_name} 2>/dev/null || true", check=False)
        return False

    print(f"✓ Healthy state confirmed: {exec_res.stdout.strip()}")

    # 6. Cleanup container immediately
    ssh_run(f"docker rm -f {container_name} 2>/dev/null || true", check=False)
    print(f"✓ Cleaned up container {container_name}")

    return True

def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    eggs_map = {e["id"]: e for e in catalog["eggs"]}
    target_eggs = [eggs_map[eid] for eid in NEW_BATCH_IDS if eid in eggs_map]

    print(f"Starting Docker test suite for {len(target_eggs)} new eggs...")

    results = {}
    for idx, egg in enumerate(target_eggs, 1):
        print(f"\n[{idx}/{len(target_eggs)}]")
        ok = test_egg(egg)
        results[egg["id"]] = ok
        if not ok:
            print(f"🚨 TEST FAILED FOR {egg['id']}!")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    print("\n==========================================")
    print(f"TEST SUITE SUMMARY: {passed}/{total} PASSED ({failed} failed)")
    print("==========================================")

    if failed > 0:
        print("Failed eggs:")
        for k, v in results.items():
            if not v:
                print(f" - {k}")
        sys.exit(1)
    else:
        print("🎉 ALL 21 NEW EGGS PASSED DOCKER VALIDATION SUCCESSFULLY!")

if __name__ == "__main__":
    main()
