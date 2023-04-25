#!/usr/bin/python3
############################################
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############################################
import sys
from utilities.setup import GetArguments
from utilities.plugin_manager import PluginManager
from utilities.usage import PrintCountryCompletion, PrintProviderCompletion, PrintUsage

def main(target_blockchain, providers_to_track, countries_to_track, output):
    print("\n-----RUNTIME-----")

    # Initialize the PluginManager and load plugins
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()

    # Get the specific plugin and create an instance
    BlockchainPlugin = plugin_manager.get_plugin(target_blockchain)
    if BlockchainPlugin:
        blockchain_obj = BlockchainPlugin(providers_to_track, countries_to_track)

        # Analyze all nodes for the provided blockchain (overwrites if flow)
        blockchain_obj = blockchain_obj.get_network_provider_distribution()

        # Output JSON for trackable providers and countries
        print("\n\nOutputting information to JSON files...")
        blockchain_obj.output_json_info()
        print("Done.", flush=True)

        # Output results flag passed
        if output:
            PrintProviderCompletion(blockchain_obj.providers_short_to_object_map, target_blockchain)
            PrintCountryCompletion(blockchain_obj.countries_short_to_object_map, target_blockchain, blockchain_obj)
    else:
        print(f"Error: The plugin for {target_blockchain} was not found. Please ensure it is correctly installed in the 'plugins' folder.")

if __name__ == "__main__":
    if len(sys.argv) > 6:
        print("ERROR: Too many parameters.\n")
        PrintUsage()
    else:
        exec_mode, providers_to_track, countries_to_track, output = GetArguments(sys.argv)
        main(exec_mode, providers_to_track, countries_to_track, output)
