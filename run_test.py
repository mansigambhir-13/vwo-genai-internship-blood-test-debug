#!/usr/bin/env python3
"""
VWO GenAI Internship Assignment - Master Test Runner
Orchestrates all testing scripts for comprehensive validation
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

class MasterTestRunner:
    """Orchestrates all testing scripts and provides comprehensive validation"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_suites = []
        self.overall_success = True
        
    def print_header(self):
        """Print professional test runner header"""
        print("🧪 VWO GenAI Internship Assignment - Master Test Runner")
        print("=" * 70)
        print("🔬 Comprehensive validation of blood test analysis system")
        print("📋 Running all test suites to validate VWO submission readiness")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def check_prerequisites(self):
        """Check that all required files exist before testing"""
        print("\n🔍 Checking Prerequisites...")
        
        required_files = {
            'main.py': 'CLI application entry point',
            'agents.py': 'AI agent configurations',
            'task.py': 'Task workflow definitions',
            'tools.py': 'Tool implementations',
            '.env': 'Environment configuration'
        }
        
        missing_files = []
        for file_name, description in required_files.items():
            if Path(file_name).exists():
                print(f"  ✅ {file_name}: {description}")
            else:
                print(f"  ❌ {file_name}: Missing - {description}")
                missing_files.append(file_name)
        
        if missing_files:
            print(f"\n🚨 PREREQUISITES FAILED")
            print(f"❌ Missing files: {', '.join(missing_files)}")
            print(f"📋 Ensure all required files are in the project directory")
            return False
        
        print(f"✅ All prerequisites satisfied")
        return True
    
    def run_test_suite(self, script_name: str, description: str, timeout: int = 60):
        """Run a specific test suite"""
        print(f"\n{'='*20} {description} {'='*20}")
        print(f"📄 Script: {script_name}")
        print(f"⏱️  Timeout: {timeout} seconds")
        
        if not Path(script_name).exists():
            print(f"  ⚠️  Skipping {description} - script not found")
            return True
        
        start_time = time.time()
        
        try:
            # Run the test script
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = time.time() - start_time
            success = result.returncode == 0
            
            if success:
                print(f"✅ {description} PASSED ({duration:.1f}s)")
                
                # Extract key metrics from output
                if "Success Rate:" in result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "Success Rate:" in line:
                            print(f"  📊 {line.strip()}")
                        elif "Passed:" in line and "Failed:" in line:
                            print(f"  📈 {line.strip()}")
            else:
                print(f"❌ {description} FAILED ({duration:.1f}s)")
                print(f"  Error: {result.stderr[:200] if result.stderr else 'No error details'}")
                self.overall_success = False
            
            # Store results
            self.test_suites.append({
                'name': description,
                'script': script_name,
                'success': success,
                'duration': duration,
                'stdout': result.stdout,
                'stderr': result.stderr
            })
            
            return success
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏰ {description} TIMED OUT ({duration:.1f}s)")
            self.overall_success = False
            return False
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 {description} ERROR ({duration:.1f}s): {e}")
            self.overall_success = False
            return False
    
    def print_comprehensive_summary(self):
        """Print detailed test results summary"""
        total_duration = time.time() - self.start_time
        
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 70)
        
        # Overall status
        if self.overall_success:
            print("🎉 OVERALL STATUS: ALL TESTS PASSED!")
        else:
            print("⚠️  OVERALL STATUS: SOME TESTS FAILED")
        
        print(f"⏱️  Total Execution Time: {total_duration:.1f} seconds")
        print(f"📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Individual test suite results
        print(f"\n📋 TEST SUITE BREAKDOWN:")
        for suite in self.test_suites:
            status = "✅ PASS" if suite['success'] else "❌ FAIL"
            print(f"  {status}: {suite['name']} ({suite['duration']:.1f}s)")
        
        # VWO submission readiness
        print(f"\n🎯 VWO SUBMISSION READINESS:")
        if self.overall_success:
            print(f"  ✅ System is fully validated and ready for submission")
            print(f"  ✅ All bug fixes are working correctly")
            print(f"  ✅ Professional quality assurance completed")
            print(f"  ✅ CrewAI expertise demonstrated")
            
            print(f"\n📧 READY TO SUBMIT:")
            print(f"  1. Create GitHub repository with all files")
            print(f"  2. Include test results in README.md")
            print(f"  3. Email to genai@vwo.com with confidence!")
            print(f"  4. Mention comprehensive testing in submission")
            
        else:
            print(f"  ⚠️  System needs fixes before submission")
            print(f"  🔧 Address failed tests above")
            print(f"  📋 Re-run master test after fixes")

    def run_comprehensive_tests(self):
        """Run all test suites"""
        self.print_header()
        
        if not self.check_prerequisites():
            return False
        
        # Ask about API testing
        print(f"\n⚠️  Integration tests require OpenAI API calls")
        print(f"💰 This may consume API credits (typically $0.01-0.05)")
        
        response = input(f"\n❓ Run integration tests with API calls? (yes/no): ").strip().lower()
        skip_integration = response not in ['yes', 'y']
        
        print(f"\n🚀 Starting comprehensive test suite execution...")
        
        # Run test suites in order
        test_order = [
            ('quick_validate.py', 'Quick System Validation', 30),
            ('test_cli_system.py', 'System Component Validation', 60),
            ('test_cli_functionality.py', 'CLI Functionality Testing', 90),
        ]
        
        if not skip_integration:
            test_order.append(('test_integration.py', 'End-to-End Integration', 300))
        
        for script, description, timeout in test_order:
            self.run_test_suite(script, description, timeout)
        
        # Print comprehensive summary
        self.print_comprehensive_summary()
        
        return self.overall_success

def main():
    """Main test runner function"""
    try:
        runner = MasterTestRunner()
        success = runner.run_comprehensive_tests()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Master test runner failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())