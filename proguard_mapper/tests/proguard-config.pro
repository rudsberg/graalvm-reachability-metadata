# Turn off optimization and shrinking, we only want obfuscation
-dontoptimize
-dontshrink

# Basic options
-dontusemixedcaseclassnames
-verbose

# Keep classes from reflect-config.json
-keep class com.example.Test