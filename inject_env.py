#!/usr/bin/env python3
"""
Inject environment variables from .env file into Alfred workflow plist.
This is for development purposes only - allows testing without manually
setting environment variables in Alfred UI.
"""

import os
import sys
import plistlib
from pathlib import Path


def load_env_file(env_path: Path) -> dict:
    """Load environment variables from .env file."""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse KEY=value
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


def inject_variables_into_plist(plist_path: Path, env_vars: dict):
    """Inject environment variables into workflow plist."""
    if not env_vars:
        print("No environment variables to inject")
        return

    # Read plist
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)

    # Create or update the variables section
    if 'variables' not in plist_data:
        plist_data['variables'] = {}

    # Inject environment variables
    for key, value in env_vars.items():
        plist_data['variables'][key] = value
        print(f"  Injected: {key}={'*' * len(value)}")  # Mask the value for security

    # Write back
    with open(plist_path, 'wb') as f:
        plistlib.dump(plist_data, f)


def main():
    script_dir = Path(__file__).parent
    env_path = script_dir / '.env'
    plist_path = script_dir / 'info.plist'

    if not env_path.exists():
        print("No .env file found. Create one from .env.example")
        print("  cp .env.example .env")
        return 0

    print("Loading environment variables from .env...")
    env_vars = load_env_file(env_path)

    if not env_vars:
        print("No variables found in .env file")
        return 0

    print(f"Injecting {len(env_vars)} variable(s) into info.plist...")
    inject_variables_into_plist(plist_path, env_vars)
    print("✓ Environment variables injected")

    return 0


if __name__ == '__main__':
    sys.exit(main())
