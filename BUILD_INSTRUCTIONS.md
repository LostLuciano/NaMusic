# MusicXNative - Build Instructions for iOS 18.0+

## Quick Summary

**Phase 1 Complete:** 54 Swift files, full UI system, audio engine, AI integration, data persistence  
**Status:** Ready to create Xcode project  
**Target:** iOS 18.0+ Native Swift/UIKit App  
**Bundle ID:** `com.musicx.native`

## Pre-Build Setup

### 1. Create Xcode Project

```bash
# Open Xcode and create new project
File > New > Project
- Platform: iOS
- Template: App
- Product Name: Runner
- Organization Identifier: com
- Interface: Storyboard
- Deployment Target: iOS 18.0
- ✓ Include Unit Tests
- Language: Swift
```

### 2. Copy All Files

All source files are in: `d:\IPA Project\StemzNa\New\MusicXNA\Runner\`

Copy to your Xcode project:
- `App/` → Project/App/
- `UI/` → Project/UI/
- `Audio/` → Project/Audio/
- `AI/` → Project/AI/
- `DSP/` → Project/DSP/
- `Data/` → Project/Data/
- `System/` → Project/System/
- `Resources/` → Project/Resources/

### 3. Add Files to Xcode

In Xcode:
```
1. Select target "Runner"
2. Build Phases > Compile Sources
3. Add All Swift Files:
   - Click +
   - Select all .swift files
   - Confirm target membership "Runner"
```

### 4. Link Frameworks

Select target → Build Phases → Link Binary With Libraries:

- ✓ AVFoundation.framework
- ✓ CoreML.framework
- ✓ Accelerate.framework
- ✓ UIKit.framework
- ✓ Foundation.framework
- ✓ AVAudioKit.framework (iOS 18+)
- ✓ UniformTypeIdentifiers.framework

### 5. Add Resources

Build Phases → Copy Bundle Resources:

**Models (`.mlmodelc` folders):**
- Chordcrnn.mlmodelc
- convtcn20_2048_fp16.mlmodelc
- dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc
- dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc

**Audio Files:**
- Vocals.m4a, Drums.m4a, Guitar.m4a, Others.m4a
- click-*.m4a (3 files)
- *.caf (11 demo tracks)

**Analysis Data:**
- *-analysis-data.json (16 files)
- *-lyrics.json (16 files)

**Assets:**
- Assets.xcassets
- Base.lproj/ (Storyboards if using)

### 6. Configure Info.plist

Copy from: `Runner/Info.plist`

Key settings:
```xml
<key>MinimumOSVersion</key>
<string>18.0</string>

<key>NSMicrophoneUsageDescription</key>
<string>MusicX needs microphone access for recording and analysis</string>

<key>UIApplicationSceneManifest</key>
<!-- SceneDelegate config -->

<key>UISupportedInterfaceOrientations</key>
<array>
    <string>UIInterfaceOrientationPortrait</string>
</array>
```

### 7. Configure Build Settings

Select target → Build Settings:

**Search: "Deployment"**
- iOS Deployment Target: 18.0

**Search: "Swift"**
- Swift Version: 5.0 or later

**Search: "Bitcode"**
- Enable Bitcode: No

**Search: "Compiler"**
- Bridging Header: Runner/Runner-Bridging-Header.h

## Building

### Command Line Build

```bash
# Navigate to project directory
cd path/to/MusicXNative

# Install pods (if using CocoaPods)
pod install

# Build for iOS device
xcodebuild clean build \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -sdk iphoneos \
  -configuration Release \
  -derivedDataPath build

# Or build for simulator
xcodebuild clean build \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -sdk iphonesimulator \
  -configuration Debug \
  -derivedDataPath build
```

### Xcode GUI Build

1. Select Product > Scheme > Runner
2. Select Product > Destination > iOS Device (or Simulator)
3. Press ⌘B to build
4. Press ⌘R to run

## Creating Unsigned IPA

For ESign:

```bash
# Create archive
xcodebuild archive \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Release \
  -archivePath build/Runner.xcarchive \
  -derivedDataPath build

# Export as unsigned IPA
xcodebuild -exportArchive \
  -archivePath build/Runner.xcarchive \
  -exportPath build/ipa \
  -exportOptionsPlist Runner/ExportOptions-unsigned.plist

# Create ZIP
cd build/ipa
zip -r MusicXNative-unsigned.zip Payload/
```

## GitHub Actions Automatic Build

Workflow: `.github/workflows/build-ios-ipa.yml`

Triggered on:
- Push to `main` branch
- Push to `develop` branch
- Pull requests to `main`
- Manual workflow_dispatch

Output:
- MusicXNative-unsigned.ipa
- MusicXNative-unsigned.zip

## Verification

### Check Models Are Bundled

```swift
// In app, check:
ModelManager.shared.checkAllModels()

// Should log:
// ✓ Stem Separation Light: Ready
// ✓ Chord Detection: Ready
// ✓ Beat Detection: Ready
```

### Check Audio Files

```swift
// Check demo tracks available
let audioFiles = Bundle.main.urls(forResourcesWithExtension: "m4a", subdirectory: nil)
print("Audio files: \(audioFiles?.count ?? 0)") // Should be >= 7
```

### Run on Device

1. Connect iOS 18.0+ device
2. Trust developer certificate (if needed)
3. Select device in Xcode
4. Press ⌘R
5. Should see app launch with:
   - Studio home screen
   - Dark purple gradient background
   - Import buttons visible
   - Model status showing "Ready"

## Troubleshooting

### Build Fails: "Module not found"

**Solution:**
```bash
# Clean build folder
xcodebuild clean -workspace Runner.xcworkspace -scheme Runner

# Rebuild
xcodebuild build -workspace Runner.xcworkspace -scheme Runner
```

### Error: "File not found: *.mlmodelc"

**Solution:**
1. Verify `.mlmodelc` folders are in `Runner/Resources/Models/`
2. Add to Copy Bundle Resources build phase
3. Set target membership to "Runner"

### Error: "Deployment target too low"

**Solution:**
- Build Settings > iOS Deployment Target: Set to 18.0 or higher
- Minimum supported: iOS 18.0

### App Crashes on Launch

**Check:**
1. Logger output for errors
2. Verify AppDelegate.swift is main entry point
3. Check all ViewControllers are properly initialized
4. Verify no missing Framework dependencies

### Models Not Loading at Runtime

**Solution:**
```swift
// In AppDelegate.swift didFinishLaunchingWithOptions:
ModelManager.shared.checkAllModels()
Logger.shared.log("Model status: \(ModelManager.shared.getAllModelStatuses())", level: .info)
```

## Next Phase (Phase 2)

After successful build:
1. Implement AI inference (ChordDetectionManager, StemSeparator, etc.)
2. Implement DSP processing (STFT, Feature Extraction)
3. Implement ExportManager for stem mixing
4. Full UI testing and refinement
5. Performance optimization
6. Beta testing on real devices

## Support

For issues:
1. Check build logs: `build/Logs/Build/`
2. Review console output in Xcode
3. Verify all framework dependencies
4. Confirm iOS 18.0+ device/simulator

---

**iOS Deployment Target:** 18.0+  
**Swift Version:** 5.0+  
**UI Framework:** UIKit (Native)  
**Build Time:** ~2-5 minutes (depending on machine)
