#!/usr/bin/env python3
"""
VWO GenAI Internship Assignment - CLI System Testing Script
Tests all components of the blood test analysis system
Run this to verify your system is properly configured before submission
"""

import os
import sys
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test required environment variables"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for AI agents'
    }
    
    optional_vars = {
        'SERPER_API_KEY': 'Serper API key for search functionality'
    }
    
    missing_required = []
    
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_required.append(f"  ❌ {var}: {description}")
        else:
            print(f"  ✅ {var}: Configured")
    
    for var, description in optional_vars.items():
        if not os.getenv(var):
            print(f"  ⚠️  {var}: Optional - {description}")
        else:
            print(f"  ✅ {var}: Configured")
    
    if missing_required:
        print("❌ Environment validation failed:")
        for error in missing_required:
            print(error)
        print("\n📋 Setup Instructions:")
        print("1. Create .env file in project root")
        print("2. Add: OPENAI_API_KEY=your_openai_api_key_here")
        print("3. Get API key from: https://platform.openai.com/api-keys")
        return False
    
    print("✅ Environment variables validated")
    return True

def test_dependencies():
    """Test required Python packages"""
    print("\n🔍 Testing Dependencies...")
    
    required_packages = [
        ('fastapi', 'FastAPI web framework'),
        ('crewai', 'Multi-agent AI framework'),
        ('langchain_openai', 'OpenAI integration'),
        ('dotenv', 'Environment variable loading'),
        ('pydantic', 'Data validation'),
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}: Available")
        except ImportError:
            missing_packages.append(f"  ❌ {package}: {description}")
    
    if missing_packages:
        print("❌ Dependency validation failed:")
        for error in missing_packages:
            print(error)
        print("\n📋 Install missing packages:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def test_directory_structure():
    """Test required directories"""
    print("\n🔍 Testing Directory Structure...")
    
    required_dirs = ['data', 'logs']
    created_dirs = []
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(exist_ok=True)
                created_dirs.append(dir_name)
                print(f"  ✅ {dir_name}/: Created")
            except Exception as e:
                print(f"  ❌ {dir_name}/: Failed to create - {e}")
                return False
        else:
            print(f"  ✅ {dir_name}/: Exists")
    
    if created_dirs:
        print(f"  📁 Auto-created directories: {', '.join(created_dirs)}")
    
    print("✅ Directory structure validated")
    return True

def test_agent_configuration():
    """Test AI agent setup"""
    print("\n🔍 Testing Agent Configuration...")
    
    try:
        from agents import doctor, verifier
        
        # Test doctor agent
        if hasattr(doctor, 'role') and hasattr(doctor, 'goal'):
            print("  ✅ Doctor agent: Properly configured")
        else:
            print("  ❌ Doctor agent: Missing role or goal")
            return False
        
        # Test verifier agent
        if hasattr(verifier, 'role') and hasattr(verifier, 'goal'):
            print("  ✅ Verifier agent: Properly configured")
        else:
            print("  ❌ Verifier agent: Missing role or goal")
            return False
        
        # Test tool integration
        if hasattr(doctor, 'tools') and doctor.tools:
            print(f"  ✅ Doctor tools: {len(doctor.tools)} tools configured")
        else:
            print("  ❌ Doctor agent: No tools configured")
            return False
        
        if hasattr(verifier, 'tools') and verifier.tools:
            print(f"  ✅ Verifier tools: {len(verifier.tools)} tools configured")
        else:
            print("  ❌ Verifier agent: No tools configured")
            return False
        
        print("✅ Agent configuration validated")
        return True
        
    except ImportError as e:
        print(f"  ❌ Agent import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Agent validation error: {e}")
        return False

def test_task_workflow():
    """Test task workflow configuration"""
    print("\n🔍 Testing Task Workflow...")
    
    try:
        from task import TASK_SEQUENCE, validate_task_dependencies
        
        # Test task sequence
        if len(TASK_SEQUENCE) >= 5:
            print(f"  ✅ Task sequence: {len(TASK_SEQUENCE)} tasks configured")
        else:
            print(f"  ❌ Task sequence: Only {len(TASK_SEQUENCE)} tasks (expected 5+)")
            return False
        
        # Test task dependencies
        try:
            validate_task_dependencies()
            print("  ✅ Task dependencies: Properly configured")
        except Exception as e:
            print(f"  ❌ Task dependencies: {e}")
            return False
        
        # Test task names
        for i, task in enumerate(TASK_SEQUENCE):
            if hasattr(task, 'description'):
                print(f"    ✅ Task {i+1}: Configured")
            else:
                print(f"    ❌ Task {i+1}: Missing description")
                return False
        
        print("✅ Task workflow validated")
        return True
        
    except ImportError as e:
        print(f"  ❌ Task import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Task validation error: {e}")
        return False

def test_tool_integration():
    """Test tool functionality"""
    print("\n🔍 Testing Tool Integration...")
    
    try:
        from tools import read_blood_test_report, search_tool
        
        # Test tool imports
        print("  ✅ Tools imported successfully")
        
        # Test search tool
        if hasattr(search_tool, 'name') or hasattr(search_tool, '_name'):
            print("  ✅ Search tool: Configured")
        else:
            print("  ❌ Search tool: Not properly configured")
            return False
        
        # Test blood test reading tool
        if callable(read_blood_test_report):
            print("  ✅ Blood test reader: Function available")
        else:
            print("  ❌ Blood test reader: Not callable")
            return False
        
        # Test with sample file (if exists)
        sample_file = Path("data/sample.txt")
        if sample_file.exists():
            try:
                result = read_blood_test_report(str(sample_file))
                if result and not result.startswith("Error"):
                    print("  ✅ Sample file processing: Working")
                else:
                    print("  ⚠️  Sample file processing: No content or error")
            except Exception as e:
                print(f"  ⚠️  Sample file test failed: {e}")
        else:
            print("  ℹ️  No sample file found (data/sample.txt)")
        
        print("✅ Tool integration validated")
        return True
        
    except ImportError as e:
        print(f"  ❌ Tool import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Tool validation error: {e}")
        return False

def run_all_tests():
    """Run comprehensive system validation"""
    print("🔬 VWO GenAI Internship Assignment - System Validation")
    print("=" * 60)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Dependencies", test_dependencies),
        ("Directory Structure", test_directory_structure),
        ("Agent Configuration", test_agent_configuration),
        ("Task Workflow", test_task_workflow),
        ("Tool Integration", test_tool_integration),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n❌ {test_name} test failed!")
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} test error: {e}")
            print(f"   Stack trace: {traceback.format_exc()}")
    
    print("\n" + "=" * 60)
    print(f"📊 SYSTEM VALIDATION RESULTS")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL SYSTEM CHECKS PASSED!")
        print("🚀 Your system is ready for blood test analysis!")
        print("📋 Next steps:")
        print("   1. Start the API: python main.py")
        print("   2. Test functionality: python test_cli_functionality.py")
        print("   3. Run integration: python test_integration.py")
        return True
    else:
        print(f"\n⚠️  {failed} TESTS FAILED")
        print("🔧 Please fix the issues above before proceeding")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)