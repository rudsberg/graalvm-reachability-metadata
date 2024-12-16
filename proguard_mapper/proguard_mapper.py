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

def generate_proguard_config_str(root_dir):
    # Required entries that are always present
    config_entries = [
        "-dontnote",
        "-keepdirectories",
        "-dontusemixedcaseclassnames",
        "-keepattributes Exceptions,InnerClasses,Signature,Deprecated,SourceFile,LineNumberTable,RuntimeVisible*Annotations,EnclosingMethod,AnnotationDefault",
        
        # Temporary 
        "-keepparameternames",
        "-keeppackagenames **",
        
        "-dontoptimize",
        "-dontpreverify", 
        "-dontshrink",
        "-adaptclassstrings",
        "-keepclassmembers class * { *** *(...); }"
    ]
    
    # Search until any file matches 
    for _dir, _, _ in os.walk(root_dir):
        print("Searching for config files in " + _dir)
        reflect_entries = read_config_file(_dir, "reflect-config.json")
        if reflect_entries:
            print('Found reflect-config.json: ', os.path.join(_dir, "reflect-config.json"))
            config_entries.extend([
                "",
                "# Keep classes from reflect-config.json"
            ])
            for entry in reflect_entries:
                if "name" in entry:
                    config_entries.append(f"-keep class {entry['name']}")

        # Read resource-config.json
        resource_entries = read_config_file(_dir, "resource-config.json")
        if resource_entries:
            print('Found resource-config.json: ', os.path.join(_dir, "reflect-config.json"))
            config_entries.extend([
                "",
                "# Keep resources from resource-config.json"
            ])
            for entry in resource_entries:
                if "pattern" in entry:
                    # Strip \Q and \E from pattern
                    pattern = entry["pattern"].replace("\\Q", "").replace("\\E", "")
                    config_entries.append(f"-keepresources {pattern}")
            
        if reflect_entries or resource_entries:
            break

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