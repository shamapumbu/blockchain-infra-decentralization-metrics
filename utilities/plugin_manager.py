# utilities/plugin_manager.py

import os
import importlib
from classes.Blockchain import Blockchain

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, plugin_folder='plugins'):
        for plugin_dir in os.listdir(plugin_folder):
            plugin_path = os.path.join(plugin_folder, plugin_dir)
            if os.path.isdir(plugin_path):
                try:
                    plugin_module = importlib.import_module(f"{plugin_folder}.{plugin_dir}")
                    for name, obj in plugin_module.__dict__.items():
                        if isinstance(obj, type) and issubclass(obj, Blockchain) and obj is not Blockchain:
                            self.plugins.append(obj)
                except ImportError as e:
                    print(f"Error loading plugin {plugin_dir}: {e}")

    def get_plugin(self, plugin_name):
        for plugin in self.plugins:
            if plugin.__name__ == plugin_name:
                return plugin
        return None
