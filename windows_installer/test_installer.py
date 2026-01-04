"""
Test script for Windows installer components
Verifies that all components are properly structured
"""

import sys
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    installer_dir = Path(__file__).parent
    required_files = [
        "launcher.py",
        "install_wizard.py",
        "uninstall.py",
        "facefusion_installer.iss",
        "launch_facefusion.bat",
        "setup_environment.bat",
        "dependency_installer.ps1",
        "README.md",
        "QUICK_START.md",
        "requirements.txt",
        "__init__.py",
        "build_exe.py",
    ]
    
    missing_files = []
    for file in required_files:
        file_path = installer_dir / file
        if not file_path.exists():
            missing_files.append(file)
            print(f"  ❌ Missing: {file}")
        else:
            print(f"  ✅ Found: {file}")
    
    if missing_files:
        print(f"\n❌ Test FAILED: {len(missing_files)} files missing")
        return False
    else:
        print("\n✅ All required files present")
        return True

def test_python_imports():
    """Test that Python scripts can be imported"""
    print("\nTesting Python script syntax...")
    
    installer_dir = Path(__file__).parent
    python_files = [
        "launcher.py",
        "install_wizard.py",
        "uninstall.py",
        "build_exe.py",
    ]
    
    errors = []
    for file in python_files:
        file_path = installer_dir / file
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            print(f"  ✅ {file} - syntax OK")
        except SyntaxError as e:
            errors.append((file, str(e)))
            print(f"  ❌ {file} - syntax error: {e}")
    
    if errors:
        print(f"\n❌ Test FAILED: {len(errors)} syntax errors")
        return False
    else:
        print("\n✅ All Python files have valid syntax")
        return True

def test_documentation():
    """Test that documentation files are not empty"""
    print("\nTesting documentation...")
    
    installer_dir = Path(__file__).parent
    doc_files = ["README.md", "QUICK_START.md"]
    
    errors = []
    for file in doc_files:
        file_path = installer_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            if size > 100:  # At least 100 bytes
                print(f"  ✅ {file} - {size} bytes")
            else:
                errors.append(file)
                print(f"  ❌ {file} - too small ({size} bytes)")
        else:
            errors.append(file)
            print(f"  ❌ {file} - not found")
    
    if errors:
        print(f"\n❌ Test FAILED: {len(errors)} documentation issues")
        return False
    else:
        print("\n✅ All documentation files valid")
        return True

def test_batch_scripts():
    """Test that batch scripts exist and are not empty"""
    print("\nTesting batch scripts...")
    
    installer_dir = Path(__file__).parent
    batch_files = [
        "launch_facefusion.bat",
        "setup_environment.bat",
    ]
    
    errors = []
    for file in batch_files:
        file_path = installer_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            if size > 50:  # At least 50 bytes
                print(f"  ✅ {file} - {size} bytes")
            else:
                errors.append(file)
                print(f"  ❌ {file} - too small ({size} bytes)")
        else:
            errors.append(file)
            print(f"  ❌ {file} - not found")
    
    if errors:
        print(f"\n❌ Test FAILED: {len(errors)} batch script issues")
        return False
    else:
        print("\n✅ All batch scripts valid")
        return True

def test_inno_setup():
    """Test that Inno Setup script exists"""
    print("\nTesting Inno Setup script...")
    
    installer_dir = Path(__file__).parent
    iss_file = installer_dir / "facefusion_installer.iss"
    
    if iss_file.exists():
        size = iss_file.stat().st_size
        print(f"  ✅ facefusion_installer.iss - {size} bytes")
        return True
    else:
        print(f"  ❌ facefusion_installer.iss - not found")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Windows Installer Component Tests")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("File Structure", test_file_structure()))
    results.append(("Python Syntax", test_python_imports()))
    results.append(("Documentation", test_documentation()))
    results.append(("Batch Scripts", test_batch_scripts()))
    results.append(("Inno Setup", test_inno_setup()))
    
    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("🎉 All tests passed!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test the launcher: python launcher.py")
        print("3. Test the installer: python install_wizard.py")
        print("4. Build executables: python build_exe.py (requires PyInstaller)")
        print("5. Compile Inno Setup installer (requires Inno Setup installed)")
        return 0
    else:
        print()
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
