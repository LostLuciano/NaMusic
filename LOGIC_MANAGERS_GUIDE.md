# Logic Managers Quick Reference Guide

## Audio Processing

### AudioEngineManager
**File:** `Runner/Audio/AudioEngineManager.swift`

Multi-channel stem playback with AVAudioEngine.

```swift
let audioEngine = AudioEngineManager()

// Load 6 stems
try audioEngine.loadStemFiles([
    "vocals": vocalsURL,
    "drums": drumsURL,
    "bass": bassURL,
    "guitar": guitarURL,
    "piano": pianoURL,
    "other": otherURL
])

// Playback control
try audioEngine.play()
audioEngine.pause()
audioEngine.stop()

// Volume control per stem (0.0 - 1.0)
audioEngine.setStemVolume(stem: "vocals", volume: 0.8)

// Mute/Solo
audioEngine.muteStem("drums", muted: true)
audioEngine.soloStem("vocals")

// Tempo & Pitch
audioEngine.setPlaybackSpeed(1.5)  // 1.5x speed
audioEngine.setPitchShift(-2.0)    // -2 semitones

// Seek to position
audioEngine.seek(to: 30.0)  // 30 seconds

// Export mix
try await audioEngine.exportStemMix(
    volumes: ["vocals": 1.0, "drums": 0.8],
    outputURL: exportURL
)
```

### MetronomeManager
**File:** `Runner/Audio/MetronomeManager.swift`

Click-track metronome with 3 sounds.

```swift
let metronome = MetronomeManager()

// Start metronome
metronome.start(bpm: 120, beatsPerBar: 4, subdivisions: 1)

// Update BPM
metronome.updateBPM(140)

// Volume control
metronome.setVolume(0.5)

// Stop
metronome.stop()
```

### RecordingManager
**File:** `Runner/Audio/RecordingManager.swift`

Audio recording with real-time level monitoring.

```swift
let recorder = RecordingManager()

// Start recording
try recorder.startRecording(to: recordingURL)

// Monitor levels (update UI in timer)
let leftLevel = recorder.currentLevelLeft
let rightLevel = recorder.currentLevelRight

// Get duration string
let durationStr = recorder.getRecordingDuration()  // "00:01:23"

// Stop recording
recorder.stopRecording()
let duration = recorder.recordingDuration
```

### ExportManager
**File:** `Runner/Audio/ExportManager.swift`

Export stems to M4A with quality settings.

```swift
let exporter = ExportManager()

try await exporter.exportMix(
    stems: stemURLDictionary,
    volumes: volumeSettings,
    outputURL: outputURL,
    quality: 192,  // kbps
    onProgress: { message, progress in
        print("\(message): \(progress * 100)%")
    }
)
```

---

## AI & Machine Learning

### ModelManager
**File:** `Runner/AI/ModelManager.swift`

CoreML model status tracking.

```swift
let models = ModelManager.shared

// Check all models
models.checkAllModels()

// Get status
let statuses = models.getAllModelStatuses()
// Returns: ["Stem Separation": "Ready", "Chord Detection": "Ready", ...]

// Get individual models (for inference)
if let stemModel = models.getStemSeparationModel() {
    // Run inference...
}
```

### CoreMLStemSeparator
**File:** `Runner/AI/CoreMLStemSeparator.swift`

6-stem source separation with CoreML.

```swift
let separator = CoreMLStemSeparator()

let stems = try await separator.separate(
    audioURL: mixtureAudioURL,
    processingMode: nil,  // or "CPU Only", "GPU Accel"
    modelQuality: "Model Ringan",  // or "Model Standar"
    onProgress: { stage, progress in
        print("[\(Int(progress * 100))%] \(stage)")
        // Update UI with progress ring
    }
)
// Returns: ["vocals": url, "drums": url, "bass": url, ...]
```

### ChordDetectionManager
**File:** `Runner/AI/ChordDetectionManager.swift`

Chord extraction from audio.

```swift
let chordDetector = ChordDetectionManager()

let chords = try await chordDetector.analyzeChords(audioURL: audioURL)

for chord in chords {
    print("\(chord.name) @ \(chord.startTime)s - \(chord.endTime)s")
    // "Am" @ 0.0s - 4.2s
    // "C:maj" @ 4.2s - 8.5s
}
```

### BeatDetectionManager
**File:** `Runner/AI/BeatDetectionManager.swift`

Beat/tempo extraction from audio.

```swift
let beatDetector = BeatDetectionManager()

let result = try await beatDetector.analyzeBeats(audioURL: audioURL)

print("BPM: \(result.tempo)")  // 120.0
print("Time Signature: \(result.timeSignature)")  // "4/4"
print("Confidence: \(result.confidence)")  // 0.96

for beat in result.beatTimings {
    print("Beat \(beat.index) @ \(beat.time)s")
}
```

---

## DSP & Audio Processing

### AudioFeatureExtractor
**File:** `Runner/DSP/AudioFeatureExtractor.swift`

STFT, iSTFT, chroma extraction.

```swift
let extractor = AudioFeatureExtractor()

// Resample to target sample rate
if let resampled = extractor.resampleAudio(inputBuffer: buffer, targetSampleRate: 44100) {
    // Use resampled buffer
}

// Extract chroma (12-bin chromagram)
let chroma = extractor.computeChroma(
    pcmBuffer: buffer,
    nFFT: 4096,
    hopSize: 2048
)
// Returns: [[Float]] - each frame has 12 pitch classes

// Reconstruct stereo signal from STFT
if let reconstructed = extractor.computeISTFTStereo(
    realL: leftRealFrames,
    imagL: leftImagFrames,
    realR: rightRealFrames,
    imagR: rightImagFrames,
    nFFT: 4096,
    hopSize: 1024,
    sampleRate: 44100.0
) {
    // Use reconstructed PCM buffer
}
```

### WaveformGenerator
**File:** `Runner/DSP/WaveformGenerator.swift`

Waveform visualization data.

```swift
let waveformGen = WaveformGenerator()

let waveform = try waveformGen.generateWaveform(
    from: audioURL,
    channelCount: 2,
    samplesPerPixel: 512
)
// Returns: [Float] normalized to 0.0-1.0 for display
```

### STFTProcessor
**File:** `Runner/DSP/STFTProcessor.swift`

Forward STFT computation.

```swift
let stft = STFTProcessor(nFFT: 4096, hopSize: 1024)
let (real, imag) = stft.computeSTFT(pcmBuffer: audioBuffer)
```

### ISTFTProcessor
**File:** `Runner/DSP/ISTFTProcessor.swift`

Inverse STFT reconstruction.

```swift
let istft = ISTFTProcessor(nFFT: 4096, hopSize: 1024)
if let reconstructed = istft.reconstructFromSTFT(
    real: realFrames,
    imag: imagFrames,
    sampleRate: 44100.0
) {
    // Use reconstructed audio buffer
}
```

---

## Data & Persistence

### ProjectStore
**File:** `Runner/Data/ProjectStore.swift`

Project save/load/list operations.

```swift
let store = ProjectStore.shared

// Save project
var project = StemProject(...)
try store.save(project)

// Load project
let loaded = try store.load(projectID)

// List all projects
let allProjects = store.listProjects()
let count = store.getProjectCount()

// Delete project
try store.delete(projectID)
```

### LyricsManager
**File:** `Runner/Data/LyricsManager.swift`

Time-synced lyrics from JSON files.

```swift
let lyrics = LyricsManager()

// Load lyrics for song
lyrics.loadLyrics(for: "classical")

// Get active line at playback position
if let line = lyrics.activeLine(at: currentTime) {
    print(line.text)
    print("\(line.startTime)s - \(line.endTime)s")
}

// Get next line
if let nextLine = lyrics.nextLine(after: currentTime) {
    // Preload next lyric
}

// Access all lines
for line in lyrics.lines {
    // Display in UI
}
```

---

## System Utilities

### FileImportManager
**File:** `Runner/System/FileImportManager.swift`

File import with format validation.

```swift
let importer = FileImportManager.shared

// Check if format is supported
if importer.isFormatSupported(fileURL) {
    // Supported formats: mp3, wav, m4a, aac, aiff, caf, flac, mov, mp4, m4v, mkv
}

// Import file to sandbox
let importedURL = try importer.importFile(sourceURL, to: destinationDir)

// Get supported extensions
let supported = importer.getSupportedExtensions()
```

### Logger
**File:** `Runner/System/Logger.swift`

Centralized logging with emoji indicators.

```swift
Logger.shared.log("Processing started", level: "ℹ️")
Logger.shared.success("Audio loaded successfully")
Logger.shared.warning("Low battery detected")
Logger.shared.error("Failed to load model")
Logger.shared.debug("Buffer size: 4096 samples")

// Get all logs
let allLogs = Logger.shared.getBufferedLogs()
Logger.shared.clearBuffer()
```

### CacheManager
**File:** `Runner/System/CacheManager.swift`

Smart caching with automatic cleanup.

```swift
let cache = CacheManager.shared

// Check if cached
if cache.hasCached(forKey: "waveform_classical") {
    let cachedURL = cache.getCacheURL(forKey: "waveform_classical")
}

// Get cache size
let sizeMB = cache.getCacheSizeMB()
let formatted = cache.getFormattedCacheSize()  // "125 MB" or "1.23 GB"

// Cleanup if needed (removes oldest files)
cache.cleanupIfNeeded()

// Clear all
cache.clearAllCache()
```

### ProcessingGate
**File:** `Runner/System/ProcessingGate.swift`

One-at-a-time processing lock.

```swift
let gate = ProcessingGate.shared

// Check if currently processing
if gate.isActive {
    print("Already processing, please wait")
    return
}

// Try to acquire lock
if gate.tryAcquire() {
    // Do expensive operation
    gate.release()
} else {
    // Already processing
}

// Or use convenience method
let executed = gate.execute {
    // CPU-intensive operation
    // Automatically released after completion
}
```

### PerformanceGuard
**File:** `Runner/System/PerformanceGuard.swift`

Thermal & memory monitoring.

```swift
let guard = PerformanceGuard.shared

// Check thermal state
print("Thermal: \(guard.currentThermalState)")

// Check memory usage
print("Memory: \(guard.memoryUsageMB) MB")

// Time a processing stage
guard.startStage("Stem Separation")
// ... do work ...
guard.endStage()

// Get all stage timings
let timings = guard.getStageTiming()
// ["Stem Separation": 45.3, "STFT": 2.1, ...]
```

---

## Typical Usage Flow

### Import & Separate
```swift
// 1. Import file
let imported = try FileImportManager.shared.importFile(userURL, to: projectDir)

// 2. Separate stems
let stems = try await CoreMLStemSeparator().separate(
    audioURL: imported,
    onProgress: { msg, progress in updateUI() }
)

// 3. Save project
var project = StemProject(...)
try ProjectStore.shared.save(project)
```

### Playback & Mixing
```swift
// 1. Load stems
try audioEngine.loadStemFiles(stems)

// 2. Adjust levels
audioEngine.setStemVolume(stem: "vocals", volume: 0.9)

// 3. Play
try audioEngine.play()

// 4. Export
try await audioEngine.exportStemMix(volumes: [...], outputURL: ...)
```

### Analysis
```swift
// 1. Detect chords
let chords = try await ChordDetectionManager().analyzeChords(audioURL: url)

// 2. Detect beat
let beat = try await BeatDetectionManager().analyzeBeats(audioURL: url)

// 3. Load lyrics
LyricsManager().loadLyrics(for: "classical")

// 4. Generate waveform
let waveform = try WaveformGenerator().generateWaveform(from: url)
```

---

## Error Handling

All managers throw NSError with descriptive messages:

```swift
do {
    try audioEngine.loadStemFiles(stems)
} catch let error as NSError {
    print("Error: \(error.userInfo[NSLocalizedDescriptionKey])")
    Logger.shared.error(error.localizedDescription)
}
```

Common errors:
- 404: File not found
- 400: Invalid format or parameters
- 500: Processing/encoding failure

