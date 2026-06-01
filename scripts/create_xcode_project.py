#!/usr/bin/env python3
"""
Create a proper Xcode 16+ project for MusicXNA using xcodebuild and configuration.
This script creates the foundation, then uses pbxproj library or direct editing to add files.
"""

import os
import sys
import subprocess
import plistlib
from pathlib import Path
import shutil

def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def create_xcode_project():
    """Create Xcode project using xcodebuild"""
    project_root = Path(__file__).parent.parent
    
    print("🔨 Creating Xcode project for MusicXNA...")
    
    # Step 1: Create project directory
    pbxproj_dir = project_root / "MusicXNA.xcodeproj"
    if pbxproj_dir.exists():
        print(f"  Removing existing project...")
        shutil.rmtree(pbxproj_dir)
    
    pbxproj_dir.mkdir(parents=True)
    
    # Step 2: Generate basic Xcode project structure
    print("  Generating project structure...")
    
    pbxproj_file = pbxproj_dir / "project.pbxproj"
    
    # Minimal valid pbxproj structure
    pbxproj_content = generate_pbxproj_content(project_root)
    
    with open(pbxproj_file, 'w', encoding='utf-8') as f:
        f.write(pbxproj_content)
    
    print(f"✅ Created {pbxproj_dir}")
    
    # Step 3: Create xcuserdata (required for Xcode)
    xcuserdata_dir = pbxproj_dir / "xcuserdata"
    xcuserdata_dir.mkdir(exist_ok=True)
    
    # Create .xcuserdatad file
    username = os.getenv('USER', 'unknown')
    xcuserdatad = xcuserdata_dir / f"{username}.xcuserdatad"
    xcuserdatad.mkdir(exist_ok=True)
    
    # Create xcschemes
    schemes_dir = xcuserdatad / "xcschemes"
    schemes_dir.mkdir(exist_ok=True)
    
    # Create default scheme
    scheme_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Scheme
   LastUpgradeVersion = "1600"
   version = "1.3">
   <BuildAction
      parallelizeBuildables = "YES"
      buildImplicitDependencies = "YES">
      <BuildActionEntries>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "MAIN_TARGET_ID"
               BuildableName = "MusicXNA.app"
               BlueprintName = "MusicXNA">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
</Scheme>'''
    
    with open(schemes_dir / "MusicXNA.xcscheme", 'w') as f:
        f.write(scheme_content)
    
    print("✅ Created scheme: MusicXNA")
    return True

def generate_pbxproj_content(project_root):
    """Generate complete pbxproj content with all files"""
    runner_dir = project_root / "Runner"
    
    # Scan all files
    swift_files = sorted([str(f.relative_to(runner_dir).as_posix()) 
                         for f in runner_dir.rglob("*.swift")])
    
    # Generate IDs
    project_id = "PROJECT000000000000000000000"
    main_group_id = "MAINGROUP00000000000000000"
    products_group_id = "PRODUCTS0000000000000000000"
    target_id = "TARGET00000000000000000000000"
    build_config_list = "BUILDCFG0000000000000000000"
    target_config_list = "TARGETCFG00000000000000000"
    compile_sources_id = "COMPILE000000000000000000000"
    bundle_resources_id = "BUNDLE0000000000000000000000"
    frameworks_id = "FRAMEWORKS00000000000000000000"
    
    # Build file references and build files
    file_refs = []
    build_files = []
    file_counter = 0
    
    for swift_file in swift_files:
        file_counter += 1
        file_id = f"FILE{file_counter:032X}".replace("0x", "")[:24]
        build_file_id = f"BUILDFILE{file_counter:04X}".ljust(24, "0")[:24]
        
        filename = swift_file.split('/')[-1]
        file_refs.append(f'''\t\t{file_id} /* {filename} */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = "Runner/{swift_file}"; sourceTree = SOURCE_ROOT; }};''')
        build_files.append(f'''\t\t{build_file_id} /* {filename} in Sources */ = {{isa = PBXBuildFile; fileRef = {file_id}; }};''')
    
    # Generate Compile Sources phase
    compile_sources_files = []
    for i, swift_file in enumerate(swift_files):
        build_file_id = f"BUILDFILE{i+1:04X}".ljust(24, "0")[:24]
        filename = swift_file.split('/')[-1]
        compile_sources_files.append(f'''\t\t\t\t{build_file_id} /* {filename} in Sources */,''')
    
    # Build configuration
    debug_config_id = "DEBUGCONFIG000000000000000000"
    release_config_id = "RELEASECONFIG0000000000000000"
    
    pbxproj = f'''// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 55;
	objects = {{
{"".join(file_refs)}
{"".join(build_files)}

		/* PBXFileReference for framework files */
		INFOPLIST_FILE /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = "Runner/Info.plist"; sourceTree = SOURCE_ROOT; }};
		BRIDGING_HEADER /* Runner-Bridging-Header.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = "Runner/Runner-Bridging-Header.h"; sourceTree = SOURCE_ROOT; }};

		/* CoreML Models */
		MODEL_CHORDCRNN /* Chordcrnn.mlmodelc */ = {{isa = PBXFileReference; lastKnownFileType = folder.mlmodelc; path = "Runner/Resources/Models/Chordcrnn.mlmodelc"; sourceTree = SOURCE_ROOT; }};
		MODEL_BEAT /* convtcn20_2048_fp16.mlmodelc */ = {{isa = PBXFileReference; lastKnownFileType = folder.mlmodelc; path = "Runner/Resources/Models/convtcn20_2048_fp16.mlmodelc"; sourceTree = SOURCE_ROOT; }};
		MODEL_STEM_STD /* dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc */ = {{isa = PBXFileReference; lastKnownFileType = folder.mlmodelc; path = "Runner/Resources/Models/dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc"; sourceTree = SOURCE_ROOT; }};
		MODEL_STEM_LIGHT /* dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc */ = {{isa = PBXFileReference; lastKnownFileType = folder.mlmodelc; path = "Runner/Resources/Models/dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc"; sourceTree = SOURCE_ROOT; }};

		/* Asset Catalog */
		ASSETS_CATALOG /* Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = "Runner/Assets.xcassets"; sourceTree = SOURCE_ROOT; }};

		/* Groups */
		{main_group_id} /* MusicXNA */ = {{
			isa = PBXGroup;
			children = (
				RUNNER_GROUP,
				{products_group_id},
			);
			sourceTree = "<group>";
		}};

		RUNNER_GROUP /* Runner */ = {{
			isa = PBXGroup;
			children = (
				APP_GROUP,
				AUDIO_GROUP,
				AI_GROUP,
				DSP_GROUP,
				DATA_GROUP,
				SYSTEM_GROUP,
				UI_GROUP,
				RESOURCES_GROUP,
				INFOPLIST_FILE,
				BRIDGING_HEADER,
			);
			name = Runner;
			path = Runner;
			sourceTree = SOURCE_ROOT;
		}};

		APP_GROUP /* App */ = {{
			isa = PBXGroup;
			children = (
			);
			path = App;
			sourceTree = "<group>";
		}};

		AUDIO_GROUP /* Audio */ = {{
			isa = PBXGroup;
			children = (
			);
			path = Audio;
			sourceTree = "<group>";
		}};

		AI_GROUP /* AI */ = {{
			isa = PBXGroup;
			children = (
			);
			path = AI;
			sourceTree = "<group>";
		}};

		DSP_GROUP /* DSP */ = {{
			isa = PBXGroup;
			children = (
			);
			path = DSP;
			sourceTree = "<group>";
		}};

		DATA_GROUP /* Data */ = {{
			isa = PBXGroup;
			children = (
			);
			path = Data;
			sourceTree = "<group>";
		}};

		SYSTEM_GROUP /* System */ = {{
			isa = PBXGroup;
			children = (
			);
			path = System;
			sourceTree = "<group>";
		}};

		UI_GROUP /* UI */ = {{
			isa = PBXGroup;
			children = (
			);
			path = UI;
			sourceTree = "<group>";
		}};

		RESOURCES_GROUP /* Resources */ = {{
			isa = PBXGroup;
			children = (
				MODEL_CHORDCRNN,
				MODEL_BEAT,
				MODEL_STEM_STD,
				MODEL_STEM_LIGHT,
				ASSETS_CATALOG,
			);
			name = Resources;
			path = "Runner/Resources";
			sourceTree = SOURCE_ROOT;
		}};

		{products_group_id} /* Products */ = {{
			isa = PBXGroup;
			children = (
				APP_PRODUCT,
			);
			name = Products;
			sourceTree = "<group>";
		}};

		APP_PRODUCT /* MusicXNA.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = MusicXNA.app; sourceTree = BUILT_PRODUCTS_DIR; }};

		/* Build Phases */
		{compile_sources_id} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
{"".join(compile_sources_files)}
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};

		{bundle_resources_id} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				MODEL_CHORDCRNN /* Chordcrnn.mlmodelc in Resources */,
				MODEL_BEAT /* convtcn20_2048_fp16.mlmodelc in Resources */,
				MODEL_STEM_STD /* dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc in Resources */,
				MODEL_STEM_LIGHT /* dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc in Resources */,
				ASSETS_CATALOG /* Assets.xcassets in Resources */,
				INFOPLIST_FILE /* Info.plist in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};

		{frameworks_id} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};

		/* Build Configurations */
		{debug_config_id} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_DIALECT = "c++17";
				CLANG_CXX_LIBRARY = "libc++";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_WARN_BLOCK_CAPTURE_OF_AUTORELEASING_VARIABLE = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_SUSPICIOUS_IMPLICIT_CONVERSION = YES;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				GCC_C_LANGUAGE_DIALECT = gnu99;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = iphoneos;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
				SWIFT_VERSION = 5.0;
			}};
			name = Debug;
		}};

		{release_config_id} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_DIALECT = "c++17";
				CLANG_CXX_LIBRARY = "libc++";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_WARN_BLOCK_CAPTURE_OF_AUTORELEASING_VARIABLE = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_SUSPICIOUS_IMPLICIT_CONVERSION = YES;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				GCC_C_LANGUAGE_DIALECT = gnu99;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = s;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SWIFT_COMPILATION_MODE = wholemodule;
				SWIFT_OPTIMIZATION_LEVEL = "-O";
				SWIFT_VERSION = 5.0;
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};

		{build_config_list} /* Build configuration list for PBXProject "MusicXNA" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{debug_config_id},
				{release_config_id},
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};

		{target_config_list} /* Build configuration list for PBXNativeTarget "MusicXNA" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				DEBUG_TARGET,
				RELEASE_TARGET,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};

		DEBUG_TARGET /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				BUNDLE_IDENTIFIER = com.musicx.native;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CODE_SIGN_IDENTITY = "";
				CODE_SIGN_REQUIRED = NO;
				CODE_SIGNING_ALLOWED = NO;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = "Runner/Info.plist";
				INFOPLIST_KEY_NSAppleMusicUsageDescription = "Access to music library for stem separation";
				INFOPLIST_KEY_NSMicrophoneUsageDescription = "Microphone access for audio recording and analysis";
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations = UIInterfaceOrientationPortrait;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown";
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.musicx.native;
				PRODUCT_NAME = MusicXNA;
				SUPPORTED_PLATFORMS = "iphoneos iphonesimulator";
				SWIFT_BRIDGING_HEADER = "Runner/Runner-Bridging-Header.h";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = 1;
			}};
			name = Debug;
		}};

		RELEASE_TARGET /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				BUNDLE_IDENTIFIER = com.musicx.native;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CODE_SIGN_IDENTITY = "";
				CODE_SIGN_REQUIRED = NO;
				CODE_SIGNING_ALLOWED = NO;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = "Runner/Info.plist";
				INFOPLIST_KEY_NSAppleMusicUsageDescription = "Access to music library for stem separation";
				INFOPLIST_KEY_NSMicrophoneUsageDescription = "Microphone access for audio recording and analysis";
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations = UIInterfaceOrientationPortrait;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown";
				IPHONEOS_DEPLOYMENT_TARGET = 18.0;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.musicx.native;
				PRODUCT_NAME = MusicXNA;
				SUPPORTED_PLATFORMS = "iphoneos iphonesimulator";
				SWIFT_BRIDGING_HEADER = "Runner/Runner-Bridging-Header.h";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = 1;
			}};
			name = Release;
		}};

		/* Targets */
		{target_id} /* MusicXNA */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {target_config_list};
			buildPhases = (
				{compile_sources_id},
				{bundle_resources_id},
				{frameworks_id},
			);
			buildRules = ();
			dependencies = ();
			name = MusicXNA;
			productName = MusicXNA;
			productReference = APP_PRODUCT;
			productType = "com.apple.product-type.application";
		}};

		/* Project */
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
			buildConfigurationList = {build_config_list};
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {main_group_id};
			productRefGroup = {products_group_id};
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{target_id},
			);
		}};
	}};
	rootObject = {project_id};
}}
'''
    
    return pbxproj

def main():
    print("="*70)
    print("XCODE PROJECT SETUP FOR MusicXNA")
    print("="*70 + "\n")
    
    if create_xcode_project():
        print("\n✅ Xcode project created successfully!")
        print("   Location: MusicXNA.xcodeproj")
        print("\n🔹 Next steps:")
        print("   1. Run validation script")
        print("   2. Build with: xcodebuild clean build")
        return 0
    else:
        print("\n❌ Failed to create Xcode project")
        return 1

if __name__ == "__main__":
    sys.exit(main())
