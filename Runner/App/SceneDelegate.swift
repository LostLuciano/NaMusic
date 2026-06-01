import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    
    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        
        window = UIWindow(windowScene: windowScene)
        
        let tabBarController = MainTabBarController()
        window?.rootViewController = tabBarController
        window?.makeKeyAndVisible()
        
        Logger.shared.log("🔗 Scene connected", level: .info)
    }
    
    func sceneDidDisconnect(_ scene: UIScene) {
        Logger.shared.log("Scene disconnected", level: .info)
    }
    
    func sceneDidBecomeActive(_ scene: UIScene) {
        Logger.shared.log("Scene became active", level: .info)
    }
    
    func sceneWillResignActive(_ scene: UIScene) {
        Logger.shared.log("Scene will resign active", level: .info)
    }
    
    func sceneWillEnterForeground(_ scene: UIScene) {
        Logger.shared.log("Scene entering foreground", level: .info)
    }
    
    func sceneDidEnterBackground(_ scene: UIScene) {
        Logger.shared.log("Scene entered background", level: .info)
    }
}
