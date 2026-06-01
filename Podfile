# Podfile untuk MusicXNative
# Dependency management

platform :ios, '18.0'

target 'Runner' do
  # Core Audio/DSP
  pod 'Accelerate', '~> 5.0'
  
  # Tidak perlu external dependencies untuk CoreML, AVFoundation, dll
  # Semua built-in ke iOS 18+
  
  # Optional: untuk development
  post_install do |installer|
    installer.pods_project.targets.each do |target|
      flutter_additional_ios_build_settings(target)
      target.build_configurations.each do |config|
        config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] ||= [
          '$(inherited)',
          'FLUTTER_ROOT=#{File.expand_path(File.join(packages_path, 'flutter'))}',
        ]
      end
    end
  end
end

target 'RunnerTests' do
  inherit! :search_paths
end
