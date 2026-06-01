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
        
        Logger.shared.info("🔗 Scene connected")
    }
    
    func sceneDidDisconnect(_ scene: UIScene) {
        Logger.shared.info("Scene disconnected")
    }
    
    func sceneDidBecomeActive(_ scene: UIScene) {
        Logger.shared.info("Scene became active")
    }
    
    func sceneWillResignActive(_ scene: UIScene) {
        Logger.shared.info("Scene will resign active")
    }
    
    func sceneWillEnterForeground(_ scene: UIScene) {
        Logger.shared.info("Scene entering foreground")
    }
    
    func sceneDidEnterBackground(_ scene: UIScene) {
        Logger.shared.info("Scene entered background")
    }
}
