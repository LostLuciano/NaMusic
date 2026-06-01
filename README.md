# MusicXNative - iOS 18+ Stem Separation & Music Analysis App

A native iOS Swift/UIKit application for AI-powered music stem separation, chord detection, and beat analysis with liquid glass design.

## Project Overview

**App Name:** MusicX Native  
**Bundle ID:** `com.musicx.native`  
**Deployment Target:** iOS 18.0+  
**Language:** Swift 5+  
**UI Framework:** UIKit (native, no SwiftUI)

## Key Features

- 🎵 **Stem Separation** - Isolate vocals, drums, bass, guitar, piano, and other stems
- 🎼 **Chord Detection** - Real-time chord recognition with confidence scores
- ♩ **Beat & Tempo** - Automatic BPM and time signature detection
- 🎤 **Audio Recording** - Record and analyze custom audio
- 🎚 **Studio Mixer** - Individual stem volume, pan, mute, solo controls
- 📱 **File Import** - Support for MP3, WAV, M4A, AAC, AIFF, CAF, FLAC, MP4, MOV
- 💾 **Export** - Mix and export stems to M4A, WAV, FLAC
- 🌙 **Liquid Glass UI** - Dark purple gradient with translucent glass cards
- ⚡ **Neural Engine** - Uses Apple Neural Engine for CoreML acceleration

## Project Structure

```
MusicXNative/
├── Runner/
│   ├── App/
│   │   ├── AppDelegate.swift
│   │   └── SceneDelegate.swift
│   ├── UI/
│   │   ├── Theme/
│   │   │   ├── StudioColors.swift
│   │   │   ├── StudioTheme.swift
│   │   │   ├── Typography.swift
│   │   │   └── GlassEffect.swift
│   │   ├── Components/
│   │   │   ├── LiquidBackgroundView.swift
│   │   │   ├── GlassCardView.swift
│   │   │   ├── PurpleGlowButton.swift
│   │   │   ├── FloatingTabBar.swift
│   │   │   ├── FloatingActionButton.swift
│   │   │   ├── WaveformView.swift
│   │   │   ├── AudioLevelMeterView.swift
│   │   │   ├── StemChannelView.swift
│   │   │   ├── ProcessingRingView.swift
│   │   │   ├── ChordPatternView.swift
│   │   │   ├── ChordTimelineView.swift
│   │   │   ├── BeatGridView.swift
│   │   │   ├── LyricsKaraokeView.swift
│   │   │   └── EmptyStateView.swift
│   │   └── Screens/
│   │       ├── MainTabBarController.swift
│   │       ├── HomeViewController.swift
│   │       ├── LibraryViewController.swift
│   │       ├── ImportSourceViewController.swift
│   │       ├── ProcessingViewController.swift
│   │       ├── ResultViewController.swift
│   │       ├── MixerViewController.swift
│   │       ├── AnalyzerViewController.swift
│   │       ├── RecordingViewController.swift
│   │       ├── ProfileViewController.swift
│   │       ├── StudioSettingsViewController.swift
│   │       └── ExportViewController.swift
│   ├── Audio/
│   │   ├── AudioEngineManager.swift
│   │   ├── MetronomeManager.swift
│   │   ├── RecordingManager.swift
│   │   └── ExportManager.swift
│   ├── AI/
│   │   ├── ModelManager.swift
│   │   ├── CoreMLStemSeparator.swift
│   │   ├── ChordDetectionManager.swift
│   │   └── BeatDetectionManager.swift
│   ├── DSP/
│   │   ├── WaveformGenerator.swift
│   │   ├── AudioFeatureExtractor.swift
│   │   ├── STFTProcessor.swift
│   │   └── ISTFTProcessor.swift
│   ├── Data/
│   │   ├── ProjectStore.swift
│   │   ├── StemProject.swift
│   │   ├── LyricsManager.swift
│   │   ├── TrackMetadata.swift
│   │   ├── ChordSegment.swift
│   │   └── BeatTempoResult.swift
│   ├── System/
│   │   ├── Logger.swift
│   │   ├── ProcessingGate.swift
│   │   ├── PerformanceGuard.swift
│   │   ├── CacheManager.swift
│   │   └── FileImportManager.swift
│   ├── Resources/
│   │   ├── Models/
│   │   │   ├── Chordcrnn.mlmodelc/
│   │   │   ├── convtcn20_2048_fp16.mlmodelc/
│   │   │   ├── dun_tfc_tdf_b9_l3_w_6stems_32_fp32_v2.0.1.mlmodelc/
│   │   │   └── dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0.mlmodelc/
│   │   ├── Audio/ (demo tracks)
│   │   └── DemoAnalysis/ (pre-computed analysis)
│   ├── Assets.xcassets/
│   ├── Base.lproj/
│   ├── Info.plist
│   └── Runner-Bridging-Header.h
├── RunnerTests/
├── .github/
│   └── workflows/
│       └── build-ios-ipa.yml
├── .gitattributes (Git LFS config)
├── .gitignore
├── Podfile
└── README.md
```

## Core Technologies

### Audio & DSP
- **AVAudioEngine** - Multi-channel playback, mixing, real-time effects
- **AVAudioSession** - Audio session management dengan Neural Engine
- **Accelerate/vDSP** - Fast signal processing
- **AVAudioRecorder** - High-quality recording

### AI & Machine Learning
- **CoreML** - On-device ML model inference
- **Neural Engine** - Hardware-accelerated inference
- **Models:**
  - Stem Separation: `dunlight_tfc_tdf_b9_l3_w_subv1_cirm_6stems_64_fp16_v2.0.0` (Light FP16)
  - Chord Detection: `Chordcrnn`
  - Beat Detection: `convtcn20_2048_fp16`

### File Management
- **FileManager** - Audio file import/export
- **UniformTypeIdentifiers** - File type handling
- **Git LFS** - Large binary file storage

### UI & Design
- **UIKit** - Native UI framework (no SwiftUI)
- **Liquid Glass** - Dark purple gradient with translucent effects
- **Purple Accent** - #BF66FF color theme

## Building for iOS 18.0+

### Prerequisites
- Xcode 16.0+
- macOS 14+
- iOS 18.0+ device or simulator

### Build Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/musicx/musicx-native.git
   cd MusicXNative
   ```

2. **Install Dependencies**
   ```bash
   pod install
   ```

3. **Open Workspace**
   ```bash
   open Runner.xcworkspace
   ```

4. **Build**
   - Select target: `Runner`
   - Select scheme: `Runner`
   - Build for iOS (⌘B)

5. **Run on Device**
   ```bash
   xcodebuild -scheme Runner -configuration Release \
     -derivedDataPath build -destination generic/platform=ios
   ```

### Create Unsigned IPA

```bash
xcodebuild archive \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Release \
  -archivePath build/Runner.xcarchive

xcodebuild -exportArchive \
  -archivePath build/Runner.xcarchive \
  -exportPath build/ipa \
  -exportOptionsPlist ExportOptions-unsigned.plist
```

## GitHub Actions Build

Automatic build triggers on push to `main` or `develop`:

```bash
git push origin main
# Workflow: .github/workflows/build-ios-ipa.yml
# Output: MusicXNative-unsigned.ipa + ZIP
```

## Configuration

### Info.plist
- Min iOS: 18.0
- Bundle ID: `com.musicx.native`
- Portrait orientation (iPhone), all orientations (iPad)
- Microphone permission required

### Audio Session
- Category: `.playAndRecord`
- Mode: `.default`
- Options: speaker, duck others, Bluetooth support
- Preferred buffer: 256 samples @ 44.1kHz

### CoreML Configuration
- Compute Units: `.allComputeUnits` (defaults to Neural Engine if available)
- Model Format: FP16 (Light) & FP32 (Standard)

## Usage Guide

### Import Audio
1. Tap "Impor Audio" or FAB
2. Select file from iPhone Files
3. Wait for copy to sandbox
4. Automatically opens Processing screen

### Stem Separation
1. Select imported audio
2. Choose Model: Light (FP16) or Standard (FP32)
3. Start separation
4. Monitor stages: Decode → STFT → Inference → Reconstruction → Export
5. View stems in Result screen

### Mixer Controls
1. Open "Studio Mixer" from Result
2. Adjust individual stem volumes (sliders)
3. Mute/Solo specific stems
4. Adjust tempo & pitch
5. Export mix to M4A

### AI Analysis
1. Open "View AI Analyzer"
2. View Chords: progression, confidence, key
3. View Beat: BPM, time signature, grid
4. View Lyrics: karaoke-style highlighting

## Performance & Optimization

### ProcessingGate
Prevents multiple CPU-intensive operations:
- Only one operation at a time (separation, recording, export)
- Throws error if operation conflicts
- Prevents 98% CPU spike

### PerformanceGuard
Monitors device health:
- Thermal state monitoring
- Memory usage tracking
- Stage timing logs
- Stops processing if device overheating

### CacheManager
Reduces reprocessing:
- Caches waveforms
- Caches analysis results
- 1GB cache directory limit
- Auto-cleanup on disk pressure

## Troubleshooting

### Models Not Loading
```swift
ModelManager.shared.checkAllModels()
// Check logs for missing .mlmodelc files in bundle
```

### Audio Playback Issues
- Check AVAudioSession configuration in AppDelegate
- Verify Audio Frameworks in Build Phases
- Test with multiple stem files

### High CPU Usage
- ProcessingGate will prevent overlapping operations
- PerformanceGuard monitors thermal state
- Consider using Light model (FP16) for efficiency

## API Reference

### Key Classes

#### AudioEngineManager
```swift
AudioEngineManager.shared.loadStemFiles([
    "vocals": vocalsURL,
    "drums": drumsURL
])
AudioEngineManager.shared.play()
AudioEngineManager.shared.setStemVolume(stem: "vocals", volume: 0.8)
```

#### ModelManager
```swift
ModelManager.shared.checkAllModels()
let model = try ModelManager.shared.loadModel(.stemSeparation_Light)
```

#### ProjectStore
```swift
try ProjectStore.shared.saveProject(project)
let projects = ProjectStore.shared.listProjects()
```

#### FileImportManager
```swift
let project = try FileImportManager.shared.importAudioFile(from: url)
```

## License

Internal Project - MusicX Studio  
© 2026 All Rights Reserved

## Support

For issues and feature requests, contact development team.

---

**Built for iOS 18.0+** | **Swift 5+** | **Native UIKit**
