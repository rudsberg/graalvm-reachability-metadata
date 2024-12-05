import unittest
import json
import tempfile
import os 
from proguard_mapper.proguard_mapper import generate_proguard_config_str, generate_proguard_config_file

class TestProguardMapper(unittest.TestCase):
    def setUp(self):
        # Common proguard config entries that should always be present
        self.required_entries = [
            "-dontoptimize",
            "-dontshrink",
            "-dontusemixedcaseclassnames",
            "-verbose"
        ]

    def assertContainsAll(self, content, expected_entries):
        """Helper method to check if all expected entries are in the content"""
        content_lines = set(line.strip() for line in content.split('\n') if line.strip())
        for entry in expected_entries:
            self.assertIn(entry, content_lines, f"Missing expected entry: {entry}")

    def test_basic_class_mapping(self):
        input_json = '''[
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
        ]'''
        
        expected_entries = self.required_entries + [
            "-keep class ch.qos.logback.classic.BasicConfigurator"
        ]

        result = generate_proguard_config_str(json.loads(input_json))
        self.assertContainsAll(result, expected_entries)

    def test_multiple_classes(self):
        input_json = '''[
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
        ]'''
        
        expected_entries = self.required_entries + [
            "-keep class com.example.First",
            "-keep class com.example.Second"
        ]

        result = generate_proguard_config_str(json.loads(input_json))
        self.assertContainsAll(result, expected_entries)

    def test_empty_input(self):
        input_json = '[]'
        result = generate_proguard_config_str(json.loads(input_json))
        self.assertContainsAll(result, self.required_entries)
        
    def test_generate_proguard_config_file(self):
        input_json = '''[
            {
                "name": "com.example.Test",
                "condition": {
                    "typeReachable": "com.example.Main"
                }
            }
        ]'''
        
        expected_entries = self.required_entries + [
            "-keep class com.example.Test"
        ]

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file = '/Users/joelrudsberg/dev/graalvm-reachability-metadata/proguard_mapper/tests/proguard-config.pro'
            generate_proguard_config_file(json.loads(input_json), file)
            
            with open(file) as f:
                content = f.read()
            
            # os.unlink(tmp.name)
            self.assertContainsAll(content, expected_entries)

if __name__ == '__main__':
    unittest.main()