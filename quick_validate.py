#!/usr/bin/env python3
"""
VWO GenAI Internship Assignment - Quick Validation Script
Fast system check to verify basic functionality before running full tests
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

class QuickValidator:
    """Fast validation of essential system components"""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_total = 0
        self.start_time = time.time()
        
    def check(self, name: str, condition: bool, success_msg: str = "", failure_msg: str = ""):
        """Perform a validation check"""
        self.checks_total += 1
        
        if condition:
            self.checks_passed += 1
            print(f"  ✅ {name}: {success_msg}")
            return True
        else:
            print(f"  ❌ {name}: {failure_msg}")
            return False
    
    def run_quick_validation(self):
        """Run all quick validation checks"""
        print("⚡ VWO Assignment - Quick System Validation")
        print("=" * 50)
        print("🔍 Essential checks for system readiness")
        print("=" * 50)
        
        # Load environment
        load_dotenv()
        
        # Check 1: Python Version
        python_version = sys.version_info
        self.check(
            "Python Version",
            python_version >= (3, 8),
            f"{python_version.major}.{python_version.minor}.{python_version.micro} (Good)",
            f"{python_version.major}.{python_version.minor} (Need 3.8+)"
        )
        
        # Check 2: Core Files
        core_files = ['main.py', 'agents.py', 'task.py', 'tools.py']
        all_files_exist = all(Path(f).exists() for f in core_files)
        missing_files = [f for f in core_files if not Path(f).exists()]
        
        self.check(
            "Core Files",
            all_files_exist,
            "All core files present",
            f"Missing: {', '.join(missing_files)}"
        )
        
        # Check 3: Environment File
        env_exists = Path('.env').exists()
        self.check(
            "Environment File",
            env_exists,
            ".env file found",
            "Create .env from .env.example"
        )
        
        # Check 4: OpenAI API Key
        api_key = os.getenv('OPENAI_API_KEY')
        key_valid = api_key and api_key != 'your_openai_api_key_here' and len(api_key) > 20
        self.check(
            "OpenAI API Key",
            key_valid,
            f"Configured ({len(api_key) if api_key else 0} chars)",
            "Missing or placeholder key"
        )
        
        # Check 5: Required Dependencies
        try:
            import crewai
            import langchain_openai
            import dotenv
            deps_ok = True
            version_info = f"CrewAI available"
        except ImportError as e:
            deps_ok = False
            version_info = f"Import error: {str(e)[:30]}"
        
        self.check(
            "Core Dependencies",
            deps_ok,
            version_info,
            "Run: pip install -r requirements.txt"
        )
        
        # Check 6: Directory Structure
        try:
            Path('data').mkdir(exist_ok=True)
            Path('logs').mkdir(exist_ok=True)
            dirs_ok = True
        except Exception as e:
            dirs_ok = False
        
        self.check(
            "Directory Structure",
            dirs_ok,
            "data/ and logs/ ready",
            "Cannot create required directories"
        )
        
        # Check 7: Basic Import Test
        try:
            sys.path.insert(0, '.')
            from agents import doctor, verifier
            agents_ok = hasattr(doctor, 'role') and hasattr(verifier, 'role')
            agent_info = f"Doctor: {doctor.role[:20]}..."
        except Exception as e:
            agents_ok = False
            agent_info = f"Import failed: {str(e)[:30]}"
        
        self.check(
            "Agent Configuration",
            agents_ok,
            agent_info,
            "Check agents.py file"
        )
        
        # Check 8: Task Import Test
        try:
            from task import TASK_SEQUENCE
            tasks_ok = len(TASK_SEQUENCE) >= 5
            task_info = f"{len(TASK_SEQUENCE)} tasks configured"
        except Exception as e:
            tasks_ok = False
            task_info = f"Import failed: {str(e)[:30]}"
        
        self.check(
            "Task Workflow",
            tasks_ok,
            task_info,
            "Check task.py file"
        )
        
        # Check 9: Tool Import Test
        try:
            from tools import read_blood_test_report, search_tool
            tools_ok = callable(read_blood_test_report)
            tool_info = "File reader and search tools ready"
        except Exception as e:
            tools_ok = False
            tool_info = f"Import failed: {str(e)[:30]}"
        
        self.check(
            "Tool Integration",
            tools_ok,
            tool_info,
            "Check tools.py file"
        )
        
        # Print Summary
        self.print_summary()
        
        return self.checks_passed == self.checks_total
    
    def print_summary(self):
        """Print validation summary"""
        duration = time.time() - self.start_time
        success_rate = (self.checks_passed / self.checks_total) * 100
        
        print("\n" + "=" * 50)
        print("📊 QUICK VALIDATION RESULTS")
        print("=" * 50)
        print(f"✅ Passed: {self.checks_passed}")
        print(f"❌ Failed: {self.checks_total - self.checks_passed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        
        if self.checks_passed == self.checks_total:
            print("\n🎉 ALL QUICK CHECKS PASSED!")
            print("🚀 System appears ready for comprehensive testing")
            print("📋 Next steps:")
            print("   1. Run full tests: python run_all_tests.py")
            print("   2. Or test individual components:")
            print("      • python test_cli_system.py")
            print("      • python test_cli_functionality.py") 
            print("      • python test_integration.py")
            
        elif self.checks_passed >= self.checks_total * 0.8:
            print("\n⚠️  MINOR ISSUES DETECTED")
            print("🔧 Most components ready, fix issues above")
            print("💡 System likely functional with minor fixes")
            
        else:
            print("\n🚨 MAJOR ISSUES DETECTED")
            print("🔧 Significant setup required before testing")
            print("📋 Essential fixes needed:")
            
            if not Path('.env').exists():
                print("   • Create .env file: cp .env.example .env")
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or api_key == 'your_openai_api_key_here':
                print("   • Add OpenAI API key to .env file")
            
            try:
                import crewai
            except ImportError:
                print("   • Install dependencies: pip install -r requirements.txt")
            
            core_files = ['main.py', 'agents.py', 'task.py', 'tools.py']
            missing = [f for f in core_files if not Path(f).exists()]
            if missing:
                print(f"   • Add missing files: {', '.join(missing)}")

def main():
    """Main validation function"""
    try:
        validator = QuickValidator()
        success = validator.run_quick_validation()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n⏹️  Validation interrupted")
        return 1
    except Exception as e:
        print(f"\n💥 Validation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())