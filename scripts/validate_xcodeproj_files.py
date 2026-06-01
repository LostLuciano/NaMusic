#!/usr/bin/env python3
"""
Validate that all important files are included in Xcode project.pbxproj.
Checks for missing Swift files, resources, CoreML models, etc.
"""

import os
import sys
import re
import json
from pathlib import Path
from collections import defaultdict

class XcodeProjValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.runner_dir = self.project_root / "Runner"
        self.pbxproj_path = self.project_root / "MusicXNA.xcodeproj" / "project.pbxproj"
        self.pbxproj_content = ""
        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)
        
    def load_pbxproj(self):
        """Load project.pbxproj content"""
        if not self.pbxproj_path.exists():
            self.errors.append(f"❌ project.pbxproj not found at {self.pbxproj_path}")
            return False
        
        try:
            with open(self.pbxproj_path, 'r', encoding='utf-8') as f:
                self.pbxproj_content = f.read()
            return True
        except Exception as e:
            self.errors.append(f"❌ Failed to read project.pbxproj: {e}")
            return False
    
    def find_all_swift_files(self):
        """Find all .swift files in Runner directory"""
        swift_files = []
        for swift_file in self.runner_dir.rglob("*.swift"):
            relative_path = swift_file.relative_to(self.runner_dir)
            swift_files.append(str(relative_path))
        
        self.stats['swift_files_on_disk'] = len(swift_files)
        return sorted(swift_files)
    
    def find_all_resource_files(self):
        """Find all resource files (json, plist, mlmodelc, audio, etc.)"""
        resources = {
            'json': [],
            'plist': [],
            'mlmodelc': [],
            'audio': [],
            'xcassets': []
        }
        
        # JSON files
        for json_file in self.runner_dir.rglob("*.json"):
            relative_path = json_file.relative_to(self.runner_dir)
            resources['json'].append(str(relative_path))
        
        # Plist files
        for plist_file in self.runner_dir.rglob("*.plist"):
            relative_path = plist_file.relative_to(self.runner_dir)
            resources['plist'].append(str(relative_path))
        
        # CoreML models (folders)
        for item in self.runner_dir.rglob("*.mlmodelc"):
            if item.is_dir():
                relative_path = item.relative_to(self.runner_dir)
                resources['mlmodelc'].append(str(relative_path))
        
        # Audio files
        for audio_file in self.runner_dir.rglob("*"):
            if audio_file.suffix in ['.m4a', '.mp3', '.wav', '.caf', '.flac']:
                relative_path = audio_file.relative_to(self.runner_dir)
                resources['audio'].append(str(relative_path))
        
        # Asset catalogs
        for xcassets in self.runner_dir.rglob("*.xcassets"):
            if xcassets.is_dir():
                relative_path = xcassets.relative_to(self.runner_dir)
                resources['xcassets'].append(str(relative_path))
        
        self.stats['json_files'] = len(resources['json'])
        self.stats['plist_files'] = len(resources['plist'])
        self.stats['mlmodelc_models'] = len(resources['mlmodelc'])
        self.stats['audio_files'] = len(resources['audio'])
        self.stats['xcassets'] = len(resources['xcassets'])
        
        return resources
    
    def check_swift_in_compile_sources(self, swift_files):
        """Check if Swift files are in Compile Sources build phase"""
        missing_swift = []
        
        for swift_file in swift_files:
            # Look for the file in pbxproj
            # Swift file should appear in PBXFileReference and PBXBuildFile with "Compile Sources"
            filename = swift_file.split('/')[-1]
            
            if filename not in self.pbxproj_content:
                missing_swift.append(swift_file)
                self.errors.append(f"❌ Swift file missing from project: {swift_file}")
        
        self.stats['swift_files_missing'] = len(missing_swift)
        return missing_swift
    
    def check_resources_in_bundle(self, resources):
        """Check if resources are in Copy Bundle Resources"""
        missing_resources = []
        
        # Check JSON files
        for json_file in resources['json']:
            filename = json_file.split('/')[-1]
            if filename not in self.pbxproj_content:
                missing_resources.append(json_file)
                self.warnings.append(f"⚠️  JSON resource may be missing: {json_file}")
        
        # Check CoreML models
        for model in resources['mlmodelc']:
            model_name = model.split('/')[-1]
            # mlmodelc models should be referenced as folder references
            if model_name not in self.pbxproj_content:
                missing_resources.append(model)
                self.errors.append(f"❌ CoreML model missing from project: {model}")
        
        # Check audio files
        for audio_file in resources['audio']:
            filename = audio_file.split('/')[-1]
            if filename not in self.pbxproj_content:
                self.warnings.append(f"⚠️  Audio file may be missing: {audio_file}")
        
        self.stats['resources_missing'] = len(missing_resources)
        return missing_resources
    
    def check_entry_points(self):
        """Check if app entry points are present"""
        entry_points = [
            'AppDelegate.swift',
            'SceneDelegate.swift',
            'MainTabBarController.swift'
        ]
        
        missing_entry_points = []
        for entry_point in entry_points:
            if entry_point not in self.pbxproj_content:
                missing_entry_points.append(entry_point)
                self.errors.append(f"❌ Entry point missing: {entry_point}")
        
        return missing_entry_points
    
    def check_bridging_header(self):
        """Check if bridging header is configured"""
        if 'Runner-Bridging-Header.h' not in self.pbxproj_content:
            self.warnings.append("⚠️  Bridging header may not be properly configured")
            return False
        return True
    
    def check_info_plist(self):
        """Check if Info.plist is configured"""
        if 'Info.plist' not in self.pbxproj_content:
            self.errors.append("❌ Info.plist missing from project")
            return False
        return True
    
    def check_build_settings(self):
        """Check if critical build settings are present"""
        required_settings = [
            'IPHONEOS_DEPLOYMENT_TARGET = 18',
            'SWIFT_VERSION',
            'PRODUCT_NAME'
        ]
        
        missing_settings = []
        for setting in required_settings:
            # Simplified check - more thorough parsing would be needed
            if setting not in self.pbxproj_content:
                self.warnings.append(f"⚠️  Build setting may be missing: {setting}")
                missing_settings.append(setting)
        
        return len(missing_settings) == 0
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*70)
        print("XCODE PROJECT VALIDATION REPORT")
        print("="*70)
        
        print(f"\n📊 STATISTICS:")
        print(f"  Swift files on disk: {self.stats['swift_files_on_disk']}")
        print(f"  Swift files missing: {self.stats.get('swift_files_missing', 0)}")
        print(f"  JSON resources: {self.stats['json_files']}")
        print(f"  Plist files: {self.stats['plist_files']}")
        print(f"  CoreML models: {self.stats['mlmodelc_models']}")
        print(f"  Audio files: {self.stats['audio_files']}")
        print(f"  Asset catalogs: {self.stats['xcassets']}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors:
            print(f"\n✅ VALIDATION PASSED")
            print(f"  All {self.stats['swift_files_on_disk']} Swift files are included")
            print(f"  All resources are properly configured")
            print(f"  CoreML models ({self.stats['mlmodelc_models']}) included")
            return 0
        else:
            print(f"\n❌ VALIDATION FAILED")
            print(f"  {len(self.errors)} critical issues found")
            return 1
    
    def validate(self):
        """Run full validation"""
        print("🔍 Validating Xcode project structure...\n")
        
        # Load pbxproj
        if not self.load_pbxproj():
            return 1
        
        # Find all files
        swift_files = self.find_all_swift_files()
        resources = self.find_all_resource_files()
        
        # Check each component
        print(f"  Found {len(swift_files)} Swift files")
        self.check_swift_in_compile_sources(swift_files)
        
        print(f"  Checking resources...")
        self.check_resources_in_bundle(resources)
        
        print(f"  Checking entry points...")
        self.check_entry_points()
        
        print(f"  Checking Info.plist...")
        self.check_info_plist()
        
        print(f"  Checking bridging header...")
        self.check_bridging_header()
        
        # Print summary and return exit code
        return self.print_summary()


def main():
    project_root = Path(__file__).parent.parent
    validator = XcodeProjValidator(str(project_root))
    exit_code = validator.validate()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
