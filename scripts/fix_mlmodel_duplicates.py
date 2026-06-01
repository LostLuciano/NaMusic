#!/usr/bin/env python3
"""
Fix duplicate metadata.json warnings in Xcode project.
CoreML models (.mlmodelc) should be added as folder references, not individual file contents.
"""

import re
from pathlib import Path

def fix_pbxproj_mlmodels():
    """Remove individual file references from .mlmodelc folders and keep only folder references."""
    
    pbx_path = Path("MusicXNA.xcodeproj/project.pbxproj")
    pbx_content = pbx_path.read_text()
    
    print("🔧 Fixing CoreML model references in pbxproj...")
    
    # List of CoreML model folders
    mlmodels = [
        "Chordcrnn.mlmodelc",
        "convtcn20_2048_fp16.mlmodelc",
        "dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc",
        "dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc"
    ]
    
    # Remove metadata.json, *.espresso.*, and other internal files from these models
    # Keep only the folder reference itself
    files_to_remove = []
    
    for model in mlmodels:
        # Find all internal files that should not be individually referenced
        internal_files = [
            f"metadata.json",
            f"model.espresso.net",
            f"model.espresso.shape",
            f"model.espresso.weights",
            f"coremldata.bin",
            f"analytics/coremldata.bin",
            f"model/coremldata.bin",
            f"neural_network_optionals/coremldata.bin",
        ]
        
        for internal_file in internal_files:
            # Create patterns to find and remove these file references
            path_pattern = f"Runner/Resources/Models/{model}/{internal_file}"
            files_to_remove.append(path_pattern)
    
    original_size = len(pbx_content)
    
    # Remove PBXFileReference entries for internal model files
    for file_path in files_to_remove:
        # Pattern: /* filename */ = {isa = PBXFileReference; ... path = "Runner/Resources/Models/..."; ...};
        pattern = rf'[A-F0-9]{{24}}\s*/\*\s*{re.escape(file_path.split("/")[-1])}\s*\*/\s*=\s*\{{[^}}]*path\s*=\s*"{re.escape(file_path)}"[^}}]*\}};?\n?'
        pbx_content = re.sub(pattern, '', pbx_content)
    
    # Remove PBXBuildFile entries for internal model files
    for file_path in files_to_remove:
        filename = file_path.split("/")[-1]
        pattern = rf'[A-F0-9]{{24}}\s*/\*\s*{re.escape(filename)}\s*in Resources\s*\*/\s*=\s*\{{[^}}]*\}};?\n?'
        pbx_content = re.sub(pattern, '', pbx_content)
    
    # Clean up extra newlines
    pbx_content = re.sub(r'\n\n\n+', '\n\n', pbx_content)
    
    new_size = len(pbx_content)
    removed_chars = original_size - new_size
    
    if removed_chars > 0:
        pbx_path.write_text(pbx_content)
        print(f"✅ Removed {removed_chars} characters of duplicate file references")
        print(f"✅ CoreML models now use folder references only")
    else:
        print("ℹ️  No duplicate references found")
    
    return True

def verify_mlmodel_refs():
    """Verify that CoreML models are folder references."""
    
    pbx_path = Path("MusicXNA.xcodeproj/project.pbxproj")
    pbx_content = pbx_path.read_text()
    
    print("\n📋 Verifying CoreML model references...")
    
    models = [
        "Chordcrnn.mlmodelc",
        "convtcn20_2048_fp16.mlmodelc",
        "dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc",
        "dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc"
    ]
    
    for model in models:
        # Check for folder reference
        if f'lastKnownFileType = folder.mlmodelc; path = "Runner/Resources/Models/{model}"' in pbx_content:
            print(f"  ✓ {model} - folder reference")
        else:
            print(f"  ⚠️  {model} - check reference type")

if __name__ == '__main__':
    fix_pbxproj_mlmodels()
    verify_mlmodel_refs()
    print("\n✅ Fix complete!")
