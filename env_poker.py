#!/usr/bin/env python3
"""ENV Var Poker - Pokes your environment variables until they confess."""

import os
import sys
import json
from typing import Dict, List, Optional


def load_env_file(filepath: str) -> Dict[str, str]:
    """Loads .env file like a detective reading a suspect's diary."""
    env_vars = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"🔍 No .env file found at {filepath} - case closed (or never opened)")
    return env_vars


def check_variables(required: List[str], env_vars: Dict[str, str]) -> Dict[str, str]:
    """Checks which variables are missing or empty. Returns confession notes."""
    results = {}
    for var in required:
        value = env_vars.get(var) or os.environ.get(var)
        if not value:
            results[var] = "MISSING - This variable is on vacation"
        elif value.strip() == '':
            results[var] = "EMPTY - Like my motivation on Monday"
        else:
            results[var] = f"OK: {value[:20]}{'...' if len(value) > 20 else ''}"
    return results


def main():
    """Main interrogation routine."""
    if len(sys.argv) < 2:
        print("Usage: python env_poker.py <required_vars.json> [.env_file]")
        print("Example: python env_poker.py required.json .env.production")
        sys.exit(1)
    
    # Load required variables (the suspects)
    try:
        with open(sys.argv[1], 'r') as f:
            required_vars = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Failed to load requirements: {e}")
        sys.exit(1)
    
    # Load .env file if provided
    env_file = sys.argv[2] if len(sys.argv) > 2 else '.env'
    file_vars = load_env_file(env_file)
    
    # Combine file vars with system env (file wins)
    all_vars = {**os.environ, **file_vars}
    
    # Interrogate the variables
    print(f"\n🔍 Poking {len(required_vars)} environment variables...\n")
    results = check_variables(required_vars, all_vars)
    
    # Present the evidence
    issues = 0
    for var, status in results.items():
        if "OK" not in status:
            print(f"❌ {var}: {status}")
            issues += 1
        else:
            print(f"✅ {var}: {status}")
    
    print(f"\n📊 Summary: {issues} problem(s) found")
    sys.exit(1 if issues > 0 else 0)


if __name__ == "__main__":
    main()
