#!/usr/bin/env python3
"""
Verification script for NZ Address Checker Application
This script verifies that all required files and directories are in place.
"""

import os
import sys
from pathlib import Path

BASE_PATH = Path(r"c:\Users\jeffr\OneDrive\Desktop\Jeff\Python\Python Projects\Address-Checker-App")

def check_directory(path, name):
    """Check if a directory exists."""
    if path.exists() and path.is_dir():
        print(f"[OK] {name}: {path}")
        return True
    else:
        print(f"[MISSING] {name}: {path}")
        return False

def check_file(path, name):
    """Check if a file exists and has content."""
    if path.exists() and path.is_file():
        size = path.stat().st_size
        print(f"[OK] {name}: {size} bytes")
        return True
    else:
        print(f"[MISSING] {name}")
        return False

def main():
    print("=" * 70)
    print("NZ ADDRESS CHECKER - PROJECT VERIFICATION")
    print("=" * 70)
    
    checks_passed = 0
    checks_total = 0
    
    # Check directories
    print("\n[DIRECTORIES]")
    dirs_to_check = {
        "Frontend Source": BASE_PATH / "frontend/src",
        "Frontend Components": BASE_PATH / "frontend/src/components",
        "Frontend Context": BASE_PATH / "frontend/src/context",
        "Frontend Hooks": BASE_PATH / "frontend/src/hooks",
        "Frontend Services": BASE_PATH / "frontend/src/services",
        "Frontend Styles": BASE_PATH / "frontend/src/styles",
        "Frontend Public": BASE_PATH / "frontend/public",
        "Backend App": BASE_PATH / "backend/app",
        "Backend Routes": BASE_PATH / "backend/app/routes",
        "Backend Services": BASE_PATH / "backend/app/services",
    }
    
    for name, path in dirs_to_check.items():
        checks_total += 1
        if check_directory(path, name):
            checks_passed += 1
    
    # Check frontend files
    print("\n[FRONTEND FILES]")
    frontend_files = {
        "Package.json": BASE_PATH / "frontend/package.json",
        "Vite Config": BASE_PATH / "frontend/vite.config.js",
        "HTML Template": BASE_PATH / "frontend/public/index.html",
        "Env Example": BASE_PATH / "frontend/.env.example",
        "Env": BASE_PATH / "frontend/.env",
        "Index Entry": BASE_PATH / "frontend/src/index.jsx",
        "App Component": BASE_PATH / "frontend/src/App.jsx",
        "Global Styles": BASE_PATH / "frontend/src/styles/GlobalStyles.js",
        "Auth Context": BASE_PATH / "frontend/src/context/AuthContext.jsx",
        "useAuth Hook": BASE_PATH / "frontend/src/hooks/useAuth.js",
        "useApi Hook": BASE_PATH / "frontend/src/hooks/useApi.js",
        "API Client": BASE_PATH / "frontend/src/services/apiClient.js",
        "Login Component": BASE_PATH / "frontend/src/components/Login.jsx",
        "AddressChecker Component": BASE_PATH / "frontend/src/components/AddressChecker.jsx",
        "ProtectedRoute Component": BASE_PATH / "frontend/src/components/ProtectedRoute.jsx",
    }
    
    for name, path in frontend_files.items():
        checks_total += 1
        if check_file(path, name):
            checks_passed += 1
    
    # Check backend files
    print("\n[BACKEND FILES]")
    backend_files = {
        "Requirements": BASE_PATH / "backend/requirements.txt",
        "Env Example": BASE_PATH / "backend/.env.example",
        "Env": BASE_PATH / "backend/.env",
        "Config": BASE_PATH / "backend/app/config.py",
        "Models": BASE_PATH / "backend/app/models.py",
        "Main App": BASE_PATH / "backend/app/main.py",
        "Auth Routes": BASE_PATH / "backend/app/routes/auth.py",
        "Address Routes": BASE_PATH / "backend/app/routes/address.py",
        "Mock Service": BASE_PATH / "backend/app/services/nz_post_mock.py",
        "Real Service Template": BASE_PATH / "backend/app/services/nz_post_real.py",
    }
    
    for name, path in backend_files.items():
        checks_total += 1
        if check_file(path, name):
            checks_passed += 1
    
    # Check documentation
    print("\n[DOCUMENTATION FILES]")
    docs_files = {
        ".gitignore": BASE_PATH / ".gitignore",
        "README": BASE_PATH / "README.md",
        "SETUP Instructions": BASE_PATH / "SETUP.md",
        "API Documentation": BASE_PATH / "API.md",
        "Dev Plan": BASE_PATH / "FOCUSED_DEV_PLAN.md",
    }
    
    for name, path in docs_files.items():
        checks_total += 1
        if check_file(path, name):
            checks_passed += 1
    
    # Print summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"Total Checks: {checks_total}")
    print(f"Passed: {checks_passed}")
    print(f"Failed: {checks_total - checks_passed}")
    print(f"Success Rate: {(checks_passed/checks_total)*100:.1f}%")
    
    if checks_passed == checks_total:
        print("\n[SUCCESS] All checks passed! Project is ready.")
        return 0
    else:
        print(f"\n[WARNING] {checks_total - checks_passed} checks failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
