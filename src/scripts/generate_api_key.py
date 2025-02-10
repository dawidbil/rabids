#!/usr/bin/env python3
import uuid


def generate_api_key() -> str:
    """Generate a random API key using UUID4."""
    return str(uuid.uuid4())


if __name__ == '__main__':
    api_key = generate_api_key()
    print('\nGenerated API Key:')
    print('-----------------')
    print(api_key)
    print('\nAdd this to your environment variables like this:')
    print(f"export ALLOWED_API_KEYS='{api_key}'")
    print('\nOr append to existing keys like this:')
    print(f"export ALLOWED_API_KEYS='existing_key1,existing_key2,{api_key}'")
