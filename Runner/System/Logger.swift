import Foundation

/// Centralized logging system with emoji indicators and file buffering.
public class Logger {
    
    public static let shared = Logger()
    
    private var logBuffer: [String] = []
    private let bufferLimit = 1000
    
    public init() {}
    
    /// Log with emoji and level indicator
    public func log(_ message: String, level: String = "ℹ️") {
        let timestamp = ISO8601DateFormatter().string(from: Date())
        let logEntry = "[\(timestamp)] \(level) \(message)"
        print(logEntry)
        bufferLog(logEntry)
    }
    
    /// Log success message
    public func success(_ message: String) {
        log(message, level: "✅")
    }
    
    /// Log warning message
    public func warning(_ message: String) {
        log(message, level: "⚠️")
    }
    
    /// Log error message
    public func error(_ message: String) {
        log(message, level: "❌")
    }
    
    /// Log debug message
    public func debug(_ message: String) {
        log(message, level: "🔍")
    }
    
    private func bufferLog(_ message: String) {
        logBuffer.append(message)
        if logBuffer.count > bufferLimit {
            logBuffer.removeFirst()
        }
    }
    
    /// Get all buffered logs
    public func getBufferedLogs() -> [String] {
        return logBuffer
    }
    
    /// Clear buffer
    public func clearBuffer() {
        logBuffer.removeAll()
    }
}
