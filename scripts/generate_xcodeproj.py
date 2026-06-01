#!/usr/bin/env python3
"""
Generate MusicXNA.xcodeproj with all required files properly configured.
Creates project.pbxproj with all Swift sources, resources, CoreML models, etc.
"""

import os
import sys
import json
import uuid
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set

class XcodeProjGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.runner_dir = self.project_root / "Runner"
        self.xcodeproj_dir = self.project_root / "MusicXNA.xcodeproj"
        self.pbxproj_path = self.xcodeproj_dir / "project.pbxproj"
        
        # Xcode file references
        self.file_refs = {}  # Maps file path to UUID
        self.build_files = {}  # Maps file path to UUID
        self.groups = {}  # Maps group name to UUID
        
        # Generated IDs
        self.id_counter = 0
        
    def gen_id(self):
        """Generate a pseudo-unique ID for Xcode"""
        # Xcode uses 24-character hex IDs
        self.id_counter += 1
        base = hex(self.id_counter)[2:].upper().zfill(8)
        return f"{base}000000000000000000000000"[-24:]
    
    def create_pbxproj_structure(self):
        """Create the basic pbxproj structure"""
        return {
            'archiveVersion': '1',
            'classes': {},
            'objectVersion': '55',
            'objects': {},
            'rootObject': self.gen_id()
        }
    
    def scan_swift_files(self) -> List[str]:
        """Scan all Swift files in Runner directory"""
        swift_files = []
        for swift_file in self.runner_dir.rglob("*.swift"):
            if swift_file.is_file():
                relative = swift_file.relative_to(self.runner_dir)
                swift_files.append(str(relative).replace('\\', '/'))
        return sorted(swift_files)
    
    def scan_resource_files(self) -> Dict[str, List[str]]:
        """Scan all resource files"""
        resources = {
            'json': [],
            'plist': [],
            'mlmodelc': [],
            'audio': [],
            'xcassets': []
        }
        
        # JSON files in DemoAnalysis and other locations
        for json_file in self.runner_dir.rglob("*.json"):
            if json_file.is_file():
                relative = json_file.relative_to(self.runner_dir)
                resources['json'].append(str(relative).replace('\\', '/'))
        
        # Plist files
        for plist_file in self.runner_dir.rglob("*.plist"):
            if plist_file.is_file():
                relative = plist_file.relative_to(self.runner_dir)
                resources['plist'].append(str(relative).replace('\\', '/'))
        
        # CoreML models (directories)
        for item in self.runner_dir.rglob("*.mlmodelc"):
            if item.is_dir():
                relative = item.relative_to(self.runner_dir)
                resources['mlmodelc'].append(str(relative).replace('\\', '/'))
        
        # Audio files
        for audio_file in self.runner_dir.rglob("*"):
            if audio_file.is_file() and audio_file.suffix in ['.m4a', '.mp3', '.wav', '.caf', '.flac']:
                relative = audio_file.relative_to(self.runner_dir)
                resources['audio'].append(str(relative).replace('\\', '/'))
        
        # Asset catalogs
        for xcassets in self.runner_dir.rglob("*.xcassets"):
            if xcassets.is_dir():
                relative = xcassets.relative_to(self.runner_dir)
                resources['xcassets'].append(str(relative).replace('\\', '/'))
        
        return resources
    
    def generate_pbxproj_text(self, swift_files: List[str], resources: Dict[str, List[str]]) -> str:
        """Generate pbxproj file content as text"""
        
        # Build file references section
        file_refs_section = self._generate_file_references(swift_files, resources)
        
        # Build build files section
        build_files_section = self._generate_build_files(swift_files, resources)
        
        # Build groups/folders
        groups_section = self._generate_groups(swift_files, resources)
        
        # Build phases
        compile_sources = self._generate_compile_sources(swift_files)
        bundle_resources = self._generate_bundle_resources(resources)
        frameworks = self._generate_frameworks()
        
        # Main target configuration
        target_id = self.gen_id()
        project_id = self.gen_id()
        main_group_id = self.gen_id()
        
        pbxproj = f"""// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 55;
	objects = {{
{file_refs_section}
{build_files_section}
{groups_section}
{compile_sources}
{bundle_resources}
{frameworks}
		{target_id} /* PBXNativeTarget "MusicXNA" */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = SOME_CONFIG_LIST;
			buildPhases = (
				COMPILE_SOURCES_ID,
				BUNDLE_RESOURCES_ID,
				FRAMEWORKS_ID,
			);
			buildRules = ();
			dependencies = ();
			name = MusicXNA;
			productName = MusicXNA;
			productReference = PRODUCT_ID;
			productType = "com.apple.product-type.application";
		}};
		{project_id} /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastUpgradeCheck = 1600;
				TargetAttributes = {{
					{target_id} = {{
						CreatedOnToolsVersion = 16.0;
						ProvisioningStyle = Automatic;
					}};
				}};
			}};
			buildConfigurationList = BUILD_CONFIG_LIST;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {main_group_id};
			productRefGroup = PRODUCT_GROUP;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{target_id},
			);
		}};
	}};
	rootObject = {project_id};
}}
"""
        return pbxproj
    
    def _generate_file_references(self, swift_files: List[str], resources: Dict[str, List[str]]) -> str:
        """Generate PBXFileReference entries"""
        lines = []
        
        # Swift files
        for swift_file in swift_files:
            file_id = self.gen_id()
            filename = swift_file.split('/')[-1]
            # Ensure forward slashes for Xcode
            swift_path = swift_file.replace('\\', '/')
            lines.append(f'\t\t{file_id} /* {filename} */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = "Runner/{swift_path}"; sourceTree = SOURCE_ROOT; }};')
            self.file_refs[swift_file] = file_id
        
        # Resource files
        for resource_type, files in resources.items():
            for res_file in files:
                file_id = self.gen_id()
                filename = res_file.split('/')[-1]
                
                if resource_type == 'json':
                    file_type = "text.json"
                elif resource_type == 'plist':
                    file_type = "text.plist"
                elif resource_type == 'mlmodelc':
                    file_type = "folder"
                elif resource_type == 'audio':
                    if res_file.endswith('.m4a'):
                        file_type = "audio.mp4"
                    elif res_file.endswith('.mp3'):
                        file_type = "audio.mp3"
                    elif res_file.endswith('.wav'):
                        file_type = "audio.wav"
                    else:
                        file_type = "audio"
                elif resource_type == 'xcassets':
                    file_type = "folder.assetcatalog"
                else:
                    file_type = "file"
                
                lines.append(f'\t\t{file_id} /* {filename} */ = {{isa = PBXFileReference; lastKnownFileType = {file_type}; path = "{res_file}"; sourceTree = SOURCE_ROOT; }};')
                self.file_refs[res_file] = file_id
        
        # Header files
        header_files = ['Info.plist', 'Runner-Bridging-Header.h', 'ExportOptions-unsigned.plist']
        for header in header_files:
            header_path = f"Runner/{header}"
            if (self.runner_dir / header).exists():
                file_id = self.gen_id()
                file_type = "text.plist" if header.endswith('.plist') else "sourcecode.c.h"
                lines.append(f'\t\t{file_id} /* {header} */ = {{isa = PBXFileReference; lastKnownFileType = {file_type}; path = "{header_path}"; sourceTree = SOURCE_ROOT; }};')
                self.file_refs[header_path] = file_id
        
        return "\n".join(lines)
    
    def _generate_build_files(self, swift_files: List[str], resources: Dict[str, List[str]]) -> str:
        """Generate PBXBuildFile entries for Compile Sources"""
        lines = []
        
        for swift_file in swift_files:
            file_ref_id = self.file_refs.get(swift_file)
            if file_ref_id:
                build_file_id = self.gen_id()
                lines.append(f'\t\t{build_file_id} /* {swift_file.split("/")[-1]} in Sources */ = {{isa = PBXBuildFile; fileRef = {file_ref_id}; }};')
                self.build_files[swift_file] = build_file_id
        
        return "\n".join(lines)
    
    def _generate_groups(self, swift_files: List[str], resources: Dict[str, List[str]]) -> str:
        """Generate PBXGroup entries for folder structure"""
        lines = []
        
        # Group for main Runner directory
        runner_group_id = self.gen_id()
        lines.append(f'\t\t{runner_group_id} /* Runner */ = {{')
        lines.append(f'\t\t\tisa = PBXGroup;')
        lines.append(f'\t\t\tchildren = (')
        
        # Add child groups/files
        for category in ['App', 'Audio', 'AI', 'DSP', 'Data', 'System', 'UI', 'Resources']:
            group_id = self.gen_id()
            lines.append(f'\t\t\t\t{group_id} /* {category} */,')
        
        lines.append(f'\t\t\t);')
        lines.append(f'\t\t\tpath = Runner;')
        lines.append(f'\t\t\tsourceTree = SOURCE_ROOT;')
        lines.append(f'\t\t}};')
        
        return "\n".join(lines)
    
    def _generate_compile_sources(self, swift_files: List[str]) -> str:
        """Generate Compile Sources build phase"""
        lines = []
        compile_id = self.gen_id()
        
        lines.append(f'\t\tCOMPILE_SOURCES_ID /* Sources */ = {{')
        lines.append(f'\t\t\tisa = PBXSourcesBuildPhase;')
        lines.append(f'\t\t\tbuildActionMask = 2147483647;')
        lines.append(f'\t\t\tfiles = (')
        
        for swift_file in swift_files:
            build_file_id = self.build_files.get(swift_file)
            if build_file_id:
                filename = swift_file.split('/')[-1]
                lines.append(f'\t\t\t\t{build_file_id} /* {filename} in Sources */,')
        
        lines.append(f'\t\t\t);')
        lines.append(f'\t\t\trunOnlyForDeploymentPostprocessing = 0;')
        lines.append(f'\t\t}};')
        
        return "\n".join(lines)
    
    def _generate_bundle_resources(self, resources: Dict[str, List[str]]) -> str:
        """Generate Copy Bundle Resources phase"""
        lines = []
        
        lines.append(f'\t\tBUNDLE_RESOURCES_ID /* Resources */ = {{')
        lines.append(f'\t\t\tisa = PBXResourcesBuildPhase;')
        lines.append(f'\t\t\tbuildActionMask = 2147483647;')
        lines.append(f'\t\t\tfiles = (')
        
        # Add all resources
        for resource_type, files in resources.items():
            for res_file in files:
                file_ref_id = self.file_refs.get(res_file)
                if file_ref_id:
                    filename = res_file.split('/')[-1]
                    lines.append(f'\t\t\t\t{file_ref_id} /* {filename} in Resources */,')
        
        # Add Info.plist
        info_plist_id = self.file_refs.get('Runner/Info.plist')
        if info_plist_id:
            lines.append(f'\t\t\t\t{info_plist_id} /* Info.plist in Resources */,')
        
        lines.append(f'\t\t\t);')
        lines.append(f'\t\t\trunOnlyForDeploymentPostprocessing = 0;')
        lines.append(f'\t\t}};')
        
        return "\n".join(lines)
    
    def _generate_frameworks(self) -> str:
        """Generate Link Binary With Libraries phase"""
        lines = []
        
        lines.append(f'\t\tFRAMEWORKS_ID /* Frameworks */ = {{')
        lines.append(f'\t\t\tisa = PBXFrameworksBuildPhase;')
        lines.append(f'\t\t\tbuildActionMask = 2147483647;')
        lines.append(f'\t\t\tfiles = (')
        lines.append(f'\t\t\t);')
        lines.append(f'\t\t\trunOnlyForDeploymentPostprocessing = 0;')
        lines.append(f'\t\t}};')
        
        return "\n".join(lines)
    
    def generate(self):
        """Generate the complete Xcode project"""
        print("🔨 Generating MusicXNA.xcodeproj...\n")
        
        # Create xcodeproj directory
        print(f"📁 Creating {self.xcodeproj_dir}")
        self.xcodeproj_dir.mkdir(parents=True, exist_ok=True)
        
        # Scan files
        print("🔍 Scanning Swift files...")
        swift_files = self.scan_swift_files()
        print(f"  Found {len(swift_files)} Swift files")
        
        print("🔍 Scanning resources...")
        resources = self.scan_resource_files()
        print(f"  Found {len(resources['json'])} JSON files")
        print(f"  Found {len(resources['plist'])} Plist files")
        print(f"  Found {len(resources['mlmodelc'])} CoreML models")
        print(f"  Found {len(resources['audio'])} audio files")
        
        # Generate pbxproj
        print("✍️  Generating project.pbxproj...")
        pbxproj_content = self.generate_pbxproj_text(swift_files, resources)
        
        # Write pbxproj
        try:
            with open(self.pbxproj_path, 'w', encoding='utf-8') as f:
                f.write(pbxproj_content)
            print(f"✅ Created {self.pbxproj_path}")
        except Exception as e:
            print(f"❌ Failed to write pbxproj: {e}")
            return False
        
        # Create pbxproj directory structure
        pbx_dir = self.xcodeproj_dir / "xcuserdata"
        pbx_dir.mkdir(exist_ok=True)
        
        print("\n✅ Xcode project generated successfully!")
        print(f"   Project: {self.xcodeproj_dir}")
        print(f"   Swift files: {len(swift_files)}")
        print(f"   Total resources: {sum(len(f) for f in resources.values())}")
        
        return True


def main():
    project_root = Path(__file__).parent.parent
    
    generator = XcodeProjGenerator(str(project_root))
    if generator.generate():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
