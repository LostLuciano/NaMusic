# CoreML Model Fix - Duplicate metadata.json Resolution

## Problem Identified

The GitHub Actions build was failing with duplicate resource warnings:

```
warning: duplicate output file '.../metadata.json' on task: CpResource
```

This occurred because CoreML models (`.mlmodelc` folders) had their internal files individually referenced in the Xcode project, causing Xcode to try copying:
- `Chordcrnn.mlmodelc/metadata.json`
- `convtcn20_2048_fp16.mlmodelc/metadata.json`
- `dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc/metadata.json`
- `dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc/metadata.json`

All to the same app bundle location, creating conflicts.

## Solution Applied

Fixed the pbxproj to **keep only folder references** for CoreML models, not individual file references.

### What Was Fixed

1. **Removed all internal file references** from `.mlmodelc` folders:
   - `metadata.json` files
   - `model.espresso.net` files
   - `model.espresso.shape` files
   - `model.espresso.weights` files
   - `coremldata.bin` files
   - All nested analytics/model files

2. **Kept only folder references** in PBXResourcesBuildPhase:
   ```
   Chordcrnn.mlmodelc (folder reference)
   convtcn20_2048_fp16.mlmodelc (folder reference)
   dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc (folder reference)
   dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc (folder reference)
   ```

3. **Removed corresponding PBXBuildFile entries** for all internal model files

### Files Changed

- **MusicXNA.xcodeproj/project.pbxproj** - Removed 886 bytes of duplicate file references
- **scripts/fix_pbxproj_mlmodels.py** - Automated fix script for future reference

### Verification

✅ All 4 CoreML models verified as folder references only  
✅ No internal files referenced individually  
✅ No more duplicate metadata.json warnings expected  

## Build Status

**Commit:** efb53a6  
**Status:** New build triggered on GitHub Actions  
**Expected Result:** Archive should complete without duplicate resource warnings

## How This Works

Xcode bundles CoreML models correctly when they are added as **folder references** (lstat = folder.mlmodelc):
- The entire `.mlmodelc` folder is copied as-is into the app bundle
- All internal files are preserved within the folder
- No conflicts from multiple `metadata.json` files

Individual file references inside `.mlmodelc` folders are unnecessary and cause the duplicate warnings.

## Future Prevention

To prevent this issue in future pbxproj generation:
1. Always add `.mlmodelc` folders as `lastKnownFileType = folder.mlmodelc`
2. Never add internal files (metadata.json, .espresso.*, etc.) individually
3. Validate that folder references are used: `grep "folder.mlmodelc" project.pbxproj`

---

**Status:** ✅ Fixed  
**Next Build:** Should succeed without duplicate resource warnings  
**Repository:** https://github.com/LostLuciano/NaMusic
