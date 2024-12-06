import unittest
import json
import tempfile
import os 
from proguard_mapper.proguard_mapper import generate_proguard_config_str, generate_proguard_config_file

class TestProguardMapper(unittest.TestCase):
    def setUp(self):
        # Common proguard config entries that should always be present
        self.required_entries = [
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

    def assertContainsAll(self, content, expected_entries):
        """Helper method to check if all expected entries are in the content"""
        content_lines = set(line.strip() for line in content.split('\n') if line.strip())
        for entry in expected_entries:
            self.assertIn(entry, content_lines, f"Missing expected entry: {entry}")

    def create_test_directory(self, reflect_config=None, resource_config=None):
        """Helper to create a test directory with config files"""
        test_dir = tempfile.mkdtemp()
        
        if reflect_config:
            with open(os.path.join(test_dir, "reflect-config.json"), "w") as f:
                json.dump(reflect_config, f)
                
        if resource_config:
            with open(os.path.join(test_dir, "resource-config.json"), "w") as f:
                json.dump(resource_config, f)
                
        return test_dir

    def test_basic_class_mapping(self):
        reflect_config = [
            {
                "name": "ch.qos.logback.classic.BasicConfigurator",
                "condition": {
                    "typeReachable": "ch.qos.logback.classic.util.ContextInitializer"
                },
                "methods": [
                    {
                        "name": "<init>",
                        "parameterTypes": []
                    }
                ]
            }
        ]
        
        test_dir = self.create_test_directory(reflect_config=reflect_config)
        
        expected_entries = self.required_entries + [
            "-keep class ch.qos.logback.classic.BasicConfigurator"
        ]

        result = generate_proguard_config_str(test_dir)
        self.assertContainsAll(result, expected_entries)

    def test_multiple_classes(self):
        reflect_config = [
            {
                "name": "com.example.First",
                "condition": {
                    "typeReachable": "com.example.Main"
                }
            },
            {
                "name": "com.example.Second",
                "condition": {
                    "typeReachable": "com.example.Main"
                }
            }
        ]
        
        test_dir = self.create_test_directory(reflect_config=reflect_config)
        
        expected_entries = self.required_entries + [
            "-keep class com.example.First",
            "-keep class com.example.Second"
        ]

        result = generate_proguard_config_str(test_dir)
        self.assertContainsAll(result, expected_entries)

    def test_empty_directory(self):
        test_dir = self.create_test_directory()
        result = generate_proguard_config_str(test_dir)
        self.assertContainsAll(result, self.required_entries)
        
    def test_resource_config(self):
        resource_config = {
            "resources": {
                "includes": [
                    {"pattern": "\\Qchangelog.yaml\\E"},
                    {"pattern": "\\Qchangelog.xml\\E"}
                ]
            }
        }
        
        test_dir = self.create_test_directory(resource_config=resource_config)
        
        expected_entries = self.required_entries + [
            "-keepresources changelog.yaml",
            "-keepresources changelog.xml"
        ]

        result = generate_proguard_config_str(test_dir)
        self.assertContainsAll(result, expected_entries)
        
    def test_generate_proguard_config_file(self):
        reflect_config = [
            {
                "name": "com.example.Test",
                "condition": {
                    "typeReachable": "com.example.Main"
                }
            }
        ]
        
        test_dir = self.create_test_directory(reflect_config=reflect_config)
        
        expected_entries = self.required_entries + [
            "-keep class com.example.Test"
        ]

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            generate_proguard_config_file(test_dir, tmp.name)
            
            with open(tmp.name) as f:
                content = f.read()
            
            os.unlink(tmp.name)
            self.assertContainsAll(content, expected_entries)

if __name__ == '__main__':
    unittest.main()