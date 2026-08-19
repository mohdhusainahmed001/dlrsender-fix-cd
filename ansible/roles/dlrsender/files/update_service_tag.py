#!/usr/bin/env python3
"""
Update the `image` field of exactly one service inside a docker-compose.yml,
preserving comments, key ordering, and every other service untouched.

Usage: update_service_tag.py <compose_file> <service_name> <new_image:tag>
"""
import sys
from ruamel.yaml import YAML

def main():
    if len(sys.argv) != 4:
        print("usage: update_service_tag.py <compose_file> <service_name> <new_image>")
        sys.exit(2)

    compose_file, service_name, new_image = sys.argv[1:4]

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096

    with open(compose_file, "r") as f:
        data = yaml.load(f)

    services = data.get("services", {})
    if service_name not in services:
        print(f"ERROR: service '{service_name}' not found in {compose_file}")
        sys.exit(1)

    old_image = services[service_name].get("image")
    if old_image == new_image:
        print("unchanged")
        return

    services[service_name]["image"] = new_image

    with open(compose_file, "w") as f:
        yaml.dump(data, f)

    print(f"updated {service_name}: {old_image} -> {new_image}")

if __name__ == "__main__":
    main()
