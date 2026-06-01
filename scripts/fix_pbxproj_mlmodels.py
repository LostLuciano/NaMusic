#!/usr/bin/env python3
"""
Fix pbxproj to prevent duplicate metadata.json warnings.
CoreML models (.mlmodelc) must be added as folder references ONLY, not file references.
"""

import re
from pathlib import Path

def remove_mlmodel_internal_files():
    """Remove all internal file references from .mlmodelc folders."""
    
    pbx_path = Path("MusicXNA.xcodeproj/project.pbxproj")
    content = pbx_path.read_text()
    
    print("🔧 Removing CoreML model internal file references...")
    
    # Pattern to find and remove file references for files inside .mlmodelc folders
    # These should never be individual files in Xcode - only folder references
    
    mlmodel_internal_patterns = [
        # metadata.json files
        r'[A-F0-9]{24}\s*/\*\s*metadata\.json\s*\*/\s*=\s*\{[^}]*path\s*=\s*"[^"]*\.mlmodelc/metadata\.json"[^}]*\};?\n?',
        # .espresso files
        r'[A-F0-9]{24}\s*/\*\s*model\.espresso\.[^"]*\s*\*/\s*=\s*\{[^}]*path\s*=\s*"[^"]*\.mlmodelc/model\.espresso\.[^"]*"[^}]*\};?\n?',
        # .weights files
        r'[A-F0-9]{24}\s*/\*\s*[^"]*\.weights\s*\*/\s*=\s*\{[^}]*path\s*=\s*"[^"]*\.mlmodelc/[^"]*\.weights"[^}]*\};?\n?',
        # coremldata.bin
        r'[A-F0-9]{24}\s*/\*\s*coremldata\.bin\s*\*/\s*=\s*\{[^}]*path\s*=\s*"[^"]*\.mlmodelc/[^"]*coremldata\.bin"[^}]*\};?\n?',
    ]
    
    original_len = len(content)
    
    for pattern in mlmodel_internal_patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Also remove corresponding PBXBuildFile entries for these files
    buildfile_patterns = [
        r'[A-F0-9]{24}\s*/\*\s*[^"]*\.mlmodelc/metadata\.json\s*in Resources\s*\*/\s*=\s*\{[^}]*\};?\n?',
        r'[A-F0-9]{24}\s*/\*\s*[^"]*\.mlmodelc/model\.espresso\.[^"]*\s*in Resources\s*\*/\s*=\s*\{[^}]*\};?\n?',
        r'[A-F0-9]{24}\s*/\*\s*[^"]*\.mlmodelc/[^"]*\.weights\s*in Resources\s*\*/\s*=\s*\{[^}]*\};?\n?',
        r'[A-F0-9]{24}\s*/\*\s*[^"]*\.mlmodelc/[^"]*coremldata\.bin\s*in Resources\s*\*/\s*=\s*\{[^}]*\};?\n?',
    ]
    
    for pattern in buildfile_patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Clean up multiple newlines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    removed = original_len - len(content)
    pbx_path.write_text(content)
    
    print(f"✅ Removed {removed} bytes of duplicate file references")
    return True

def verify_mlmodel_references():
    """Verify that only folder references remain for .mlmodelc files."""
    
    pbx_path = Path("MusicXNA.xcodeproj/project.pbxproj")
    content = pbx_path.read_text()
    
    print("\n📋 Verifying CoreML model setup...")
    
    mlmodels = {
        "Chordcrnn.mlmodelc": "Chord detection model",
        "convtcn20_2048_fp16.mlmodelc": "Beat detection model",
        "dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc": "Stem separation (standard)",
        "dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc": "Stem separation (light)",
    }
    
    all_good = True
    
    for model_name, description in mlmodels.items():
        # Check for folder reference (only way .mlmodelc should appear)
        if f'folder.mlmodelc; path = "Runner/Resources/Models/{model_name}"' in content:
            print(f"  ✓ {model_name}")
            print(f"    └─ {description}")
        else:
            print(f"  ⚠️  {model_name} - verify reference")
            all_good = False
        
        # Check for internal files that should NOT be there
        internal_files = ['metadata.json', '.espresso.', '.weights', 'coremldata.bin']
        for internal in internal_files:
            if f'{model_name}/{internal}' in content:
                print(f"      ✗ ERROR: Found {internal} file reference (should be folder only)")
                all_good = False
    
    if all_good:
        print("\n✅ All CoreML models are correctly configured as folder references!")
    else:
        print("\n⚠️  Some issues found - see above")
    
    return all_good

if __name__ == '__main__':
    print("=" * 70)
    print("FIXING COREML MODEL REFERENCES IN XCODE PROJECT")
    print("=" * 70)
    
    remove_mlmodel_internal_files()
    verify_mlmodel_references()
    
    print("\n" + "=" * 70)
    print("✅ Fix complete! Rebuild should no longer show duplicate metadata.json")
    print("=" * 70)
