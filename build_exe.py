#!/usr/bin/env python3
"""
Build script for OPIC Learning App
Creates standalone executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for spec_file in Path('.').glob('*.spec'):
        print(f"Removing {spec_file}...")
        spec_file.unlink()

def check_dependencies():
    """Check if required tools are available"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found. Install with: pip install PyInstaller")
        return False
    
    try:
        from PyQt5 import QtCore
        print(f"✓ PyQt5 {QtCore.PYQT_VERSION_STR} found")
    except ImportError:
        print("✗ PyQt5 not found. Install with: pip install PyQt5")
        return False
    
    return True

def create_version_file():
    """Create version info file for Windows executable"""
    version_info = """
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'OPIC Learning Team'),
        StringStruct(u'FileDescription', u'OPIC Learning Application'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'OPIC Master'),
        StringStruct(u'LegalCopyright', u'Copyright © 2024 OPIC Learning Team'),
        StringStruct(u'OriginalFilename', u'OPIC_Master.exe'),
        StringStruct(u'ProductName', u'OPIC Master'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✓ Version info file created")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building OPIC Master executable...")
    
    # Determine platform-specific settings
    icon_file = "resources/icons/app_icon.ico" if os.name == 'nt' else "resources/icons/app_icon.png"
    
    # PyInstaller arguments
    args = [
        'main.py',
        '--name=OPIC_Master',
        '--windowed',  # No console window
        '--onefile',   # Single executable file
        f'--icon={icon_file}',
        
        # Add data files
        '--add-data=resources;resources',
        '--add-data=data;data',
        '--add-data=config;config',
        
        # Hidden imports (modules that PyInstaller might miss)
        '--hidden-import=sqlite3',
        '--hidden-import=requests',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui', 
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=json',
        '--hidden-import=logging',
        
        # Exclude unnecessary modules to reduce size
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=scipy',
        '--exclude-module=pandas',
        '--exclude-module=PIL.ImageQt',
        
        # Other options
        '--clean',
        '--noconfirm',
        '--optimize=2',
    ]
    
    # Add Windows-specific options
    if os.name == 'nt':
        args.extend([
            '--version-file=version_info.txt',
            '--uac-admin',  # Request admin privileges if needed
        ])
    
    # Add macOS-specific options
    elif sys.platform == 'darwin':
        args.extend([
            '--osx-bundle-identifier=com.opiclearning.master',
        ])
    
    # Run PyInstaller
    try:
        import PyInstaller.__main__
        PyInstaller.__main__.run(args)
        print("✓ Build completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Build failed: {e}")
        return False

def post_build_tasks():
    """Perform post-build tasks"""
    dist_dir = Path('dist')
    
    if not dist_dir.exists():
        print("✗ Dist directory not found")
        return False
    
    # Create additional directories in dist
    resources_dist = dist_dir / 'resources'
    if not resources_dist.exists() and Path('resources').exists():
        shutil.copytree('resources', resources_dist)
        print("✓ Resources copied to dist")
    
    # Create README for distribution
    readme_content = """
OPIC Master - Ứng dụng luyện thi OPIC

HƯỚNG DẪN CÀI ĐẶT:
1. Giải nén file zip vào thư mục bất kỳ
2. Chạy file OPIC_Master.exe (Windows) hoặc OPIC_Master (Linux/macOS)
3. Lần đầu chạy, vào menu Công cụ > Cài đặt để nhập API key

YÊU CẦU HỆ THỐNG:
- Windows 10/11, macOS 10.14+, hoặc Linux
- 4GB RAM
- 500MB dung lượng trống
- Kết nối internet để sử dụng AI

LIÊN HỆ HỖ TRỢ:
- Email: support@opiclearning.com
- Website: https://opiclearning.com

Phiên bản: 1.0.0
Copyright © 2024 OPIC Learning Team
"""
    
    readme_file = dist_dir / 'README.txt'
    readme_file.write_text(readme_content, encoding='utf-8')
    print("✓ README created")
    
    # Create sample config file
    sample_config = {
        "api": {
            "provider": "openrouter",
            "api_key": "",
            "api_url": "https://openrouter.ai/api/v1/chat/completions",
            "model": "openai/gpt-4o-mini"
        },
        "ui": {
            "theme": "default",
            "language": "vi",
            "font_size": 12
        }
    }
    
    import json
    config_file = dist_dir / 'config_sample.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, indent=2, ensure_ascii=False)
    print("✓ Sample config created")
    
    return True

def create_installer():
    """Create installer package (optional)"""
    print("Creating installer package...")
    
    # This would use tools like NSIS (Windows), pkgbuild (macOS), or dpkg (Linux)
    # For now, just create a zip file
    try:
        import zipfile
        
        zip_name = f"OPIC_Master_v1.0.0_{sys.platform}.zip"
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            dist_dir = Path('dist')
            for file_path in dist_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(dist_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"✓ Installer package created: {zip_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to create installer: {e}")
        return False

def get_build_info():
    """Get build information"""
    import platform
    import datetime
    
    info = {
        'timestamp': datetime.datetime.now().isoformat(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
    }
    
    # Save build info
    with open('dist/build_info.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    print("✓ Build info saved")

def main():
    """Main build process"""
    print("=" * 50)
    print("OPIC Master - Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('main.py').exists():
        print("✗ main.py not found. Please run from project root directory.")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        print("✗ Missing required dependencies. Please install them first.")
        return 1
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create version file for Windows
    if os.name == 'nt':
        create_version_file()
    
    # Build executable
    if not build_executable():
        return 1
    
    # Post-build tasks
    if not post_build_tasks():
        print("⚠ Some post-build tasks failed, but executable should work")
    
    # Get build info
    get_build_info()
    
    # Create installer (optional)
    create_installer()
    
    # Final message
    print("=" * 50)
    print("✓ Build process completed!")
    print(f"✓ Executable location: {Path('dist').absolute()}")
    print("✓ Ready for distribution")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
