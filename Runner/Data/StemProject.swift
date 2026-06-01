import Foundation

enum ProjectStatus: String, Codable {
    case imported = "Imported"
    case separating = "Separating"
    case separated = "Separated"
    case analyzing = "Analyzing"
    case analyzed = "Analyzed"
    case recording = "Recording"
    case exporting = "Exporting"
    case failed = "Failed"
    case cancelled = "Cancelled"
}

struct ChordSegment: Codable {
    let timestamp: TimeInterval
    let chord: String
    let confidence: Float
    let startTime: TimeInterval
    let endTime: TimeInterval
}

struct BeatTempoResult: Codable {
    let bpm: Double
    let confidence: Float
    let timeSignature: String
    let beatTimings: [TimeInterval]
}

struct StemProject: Codable, Identifiable {
    let id: UUID
    var name: String  // Alias for title
    var title: String
    var createdAt: Date
    var createdDate: Date { createdAt }  // For compatibility
    var originalAudioURL: URL
    var importedFileName: String
    var duration: Double
    var format: String
    var sampleRate: Double
    var bpm: Double?
    var key: String?
    var status: ProjectStatus
    var stemPaths: [String: URL]          // "vocals", "drums", "bass", "guitar", "piano", "others"
    var chordSegments: [ChordSegment]
    var beatResult: BeatTempoResult?
    var lyricsPath: URL?
    var waveformCachePath: URL?
    
    // Aliases for stem-specific URLs
    var vocalsURL: URL? { stemPaths["vocals"] }
    var drumsURL: URL? { stemPaths["drums"] }
    var bassURL: URL? { stemPaths["bass"] }
    var guitarURL: URL? { stemPaths["guitar"] }
    var pianoURL: URL? { stemPaths["piano"] }
    var otherURL: URL? { stemPaths["other"] }
    
    // MARK: - Computed Properties
    var displayDuration: String {
        let minutes = Int(duration) / 60
        let seconds = Int(duration) % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
    
    var projectDirectory: URL {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        return documentsPath.appendingPathComponent("Projects/\(id.uuidString)")
    }
    
    var stemDirectory: URL {
        projectDirectory.appendingPathComponent("stems")
    }
    
    var analysisDirectory: URL {
        projectDirectory.appendingPathComponent("analysis")
    }
    
    // MARK: - Methods
    mutating func setStemPath(_ stem: String, url: URL) {
        stemPaths[stem] = url
    }
    
    func getStemPath(_ stem: String) -> URL? {
        return stemPaths[stem]
    }
    
    func allStemsAvailable() -> Bool {
        let requiredStems = ["vocals", "drums", "bass", "guitar", "piano", "others"]
        return requiredStems.allSatisfy { stemPaths[$0] != nil }
    }
}
