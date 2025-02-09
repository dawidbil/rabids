from typing import Dict, Type
import importlib
import inspect
import os
from pathlib import Path


class ExtensionManager:
    def __init__(self):
        self.extensions: Dict[str, Any] = {}
        self.extension_dir = Path(__file__).parent.parent.parent / 'extensions'

    async def load_extensions(self) -> None:
        """Dynamically load all extensions from the extensions directory."""
        for item in os.listdir(self.extension_dir):
            if item.startswith('_'):
                continue

            extension_path = self.extension_dir / item
            if extension_path.is_dir() and (extension_path / 'extension.py').exists():
                try:
                    module = importlib.import_module(f'extensions.{item}.extension')
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and hasattr(obj, 'initialize'):
                            extension = obj()
                            await extension.initialize()
                            self.extensions[item] = extension
                except Exception as e:
                    print(f'Failed to load extension {item}: {e}')

    async def unload_extension(self, name: str) -> None:
        """Unload a specific extension."""
        if name in self.extensions:
            extension = self.extensions[name]
            if hasattr(extension, 'cleanup'):
                await extension.cleanup()
            del self.extensions[name]
