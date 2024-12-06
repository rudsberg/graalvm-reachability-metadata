import json
import os
import sys

# TODO: must keep all classes in the packages in which resources are kept 

def read_config_file(directory, filename):
    """Read a config file from directory, return empty list if not found."""
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath) as f:
            config = json.load(f)
            if filename == "reflect-config.json":
                return config
            elif filename == "resource-config.json":
                return config.get("resources", {}).get("includes", [])
    return []

def generate_proguard_config_str(input_dir):
    # Required entries that are always present
    config_entries = [
        "-dontwarn",
        "-dontnote",
        "-keepdirectories",
        "-dontusemixedcaseclassnames",
        "-keepattributes *Annotation*,Signature,EnclosingMethod,InnerClasses",
        "-keepparameternames",
        "-dontoptimize",
        "-dontpreverify", 
        "-dontshrink",
        "-adaptclassstrings",
        "-keepclassmembers class * { *** *(...); }"
    ]

    # Read reflect-config.json
    reflect_entries = read_config_file(input_dir, "reflect-config.json")
    if reflect_entries:
        config_entries.extend([
            "",
            "# Keep classes from reflect-config.json"
        ])
        for entry in reflect_entries:
            if "name" in entry:
                config_entries.append(f"-keep class {entry['name']}")
    else: 
        print('No file found in ' + os.path.join(input_dir, "reflect-config.json"))

    # Read resource-config.json
    resource_entries = read_config_file(input_dir, "resource-config.json")
    if resource_entries:
        config_entries.extend([
            "",
            "# Keep resources from resource-config.json"
        ])
        for entry in resource_entries:
            if "pattern" in entry:
                # Strip \Q and \E from pattern
                pattern = entry["pattern"].replace("\\Q", "").replace("\\E", "")
                config_entries.append(f"-keepresources {pattern}")
    else:
        print('No file found in ' + os.path.join(input_dir, "resource-config.json"))

    return "\n".join(config_entries)

def generate_proguard_config_file(input_dir, output_path):
    proguard_config_str = generate_proguard_config_str(input_dir)
    with open(output_path, "w") as f:
        f.write(proguard_config_str)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: proguard_mapper.py <input_directory> <output_file>")
        sys.exit(1)
        
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    generate_proguard_config_file(input_dir, output_file)