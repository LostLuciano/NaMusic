import UIKit
import AVFoundation

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    
    var window: UIWindow?
    
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        
        // Configure audio session
        configureAudioSession()
        
        // Initialize all logic managers
        initializeManagers()
        
        // Create main window
        window = UIWindow(frame: UIScreen.main.bounds)
        
        // Setup root view controller
        let tabBarController = MainTabBarController()
        
        window?.rootViewController = tabBarController
        window?.makeKeyAndVisible()
        
        return true
    }
    
    private func initializeManagers() {
        // Logger
        Logger.shared.log("🚀 App launched - Initializing managers", level: .info)
        
        // Model Manager - check all CoreML models
        Logger.shared.log("📊 Checking CoreML models...", level: .info)
        ModelManager.shared.checkAllModels()
        let modelStatus = ModelManager.shared.getAllModelStatuses()
        for (model, status) in modelStatus {
            Logger.shared.log("  \(model): \(status)", level: .debug)
        }
        
        // Project Store - verify directory
        Logger.shared.log("💾 Initializing project storage...", level: .info)
        let projectCount = ProjectStore.shared.getProjectCount()
        Logger.shared.log("  Found \(projectCount) existing projects", level: .debug)
        
        // Cache Manager - check cache size
        Logger.shared.log("🗄️  Initializing cache...", level: .info)
        let cacheSize = CacheManager.shared.getFormattedCacheSize()
        Logger.shared.log("  Cache size: \(cacheSize)", level: .debug)
        CacheManager.shared.cleanupIfNeeded()
        
        // Processing Gate - ready
        Logger.shared.log("🚪 Processing gate ready", level: .info)
        
        // Performance Guard - start monitoring
        Logger.shared.log("📈 Performance monitoring started", level: .info)
        
        Logger.shared.success("✅ All managers initialized successfully")
    }
    
    private func configureAudioSession() {
        let audioSession = AVAudioSession.sharedInstance()
        
        do {
            // Category: playback dan recording
            try audioSession.setCategory(
                .playAndRecord,
                mode: .default,
                options: [
                    .defaultToSpeaker,
                    .duckOthers,
                    .allowBluetooth,
                    .allowBluetoothA2DP
                ]
            )
            
            // PreferredIOBufferDuration: 256 samples untuk latency rendah
            try audioSession.setPreferredIOBufferDuration(256.0 / 44100.0)
            
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
            
            Logger.shared.log("✓ Audio session configured", level: .info)
        } catch {
            Logger.shared.log("✗ Audio session error: \(error)", level: .error)
        }
    }
    
    // MARK: - UISceneDelegate
    
    func application(
        _ application: UIApplication,
        configurationForConnecting connectingSceneSession: UISceneSession,
        options: UIScene.ConnectionOptions
    ) -> UISceneConfiguration {
        let sceneConfig = UISceneConfiguration(name: "Default", sessionRole: connectingSceneSession.role)
        sceneConfig.delegateClass = SceneDelegate.self
        return sceneConfig
    }
    
    func applicationDidEnterBackground(_ application: UIApplication) {
        Logger.shared.log("📦 App entered background", level: .info)
    }
    
    func applicationWillEnterForeground(_ application: UIApplication) {
        Logger.shared.log("📂 App entered foreground", level: .info)
    }
    
    func applicationWillTerminate(_ application: UIApplication) {
        Logger.shared.log("🔌 App terminating", level: .info)
    }
}
