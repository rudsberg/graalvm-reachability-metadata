import json

def generate_proguard_config_str(json_metadata):
    # Required entries that are always present
    # For now we disable everything NOT REQUIRED for classnames
    config_entries = [
        "-keepattributes *Annotation*,Signature,EnclosingMethod,InnerClasses",
        # Skip resource files and module-info
        "-keep class !**.resources.** { *; }",
        "-keep class !META-INF.** { *; }",
        "-keep class !**.txt { *; }",
        "-keep class !**.properties { *; }",
        "-keep class !**.xml { *; }",
        "-keep class !**.dtd { *; }",
        "-keep class !**.xsd { *; }",
        "-keep class !module-info { *; }",
        "-keepparameternames",
        "-dontoptimize",
        "-dontpreverify", 
        "-dontshrink",
        "-adaptclassstrings",
        "-keepclassmembers class * { *** *(...); }"
    ]

    # Add class keep rules if we have any
    if json_metadata:
        config_entries.extend([
            "",
            "# Keep classes from reflect-config.json"
        ])
        
        for entry in json_metadata:
            if "name" in entry:
                config_entries.append(f"-keep class {entry['name']}")

    return "\n".join(config_entries)

def generate_proguard_config_file(json_metadata, output_path):
    proguard_config_str = generate_proguard_config_str(json_metadata)
    with open(output_path, "w") as f:
        f.write(proguard_config_str)
        
def generate_proguard_config_from_file(input_json_path, output_path):
    with open(input_json_path) as f:
        json_metadata = json.load(f)
    generate_proguard_config_file(json_metadata, output_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: proguard_mapper.py <input_json> <output_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    generate_proguard_config_from_file(input_file, output_file)