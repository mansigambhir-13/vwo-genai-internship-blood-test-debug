#!/usr/bin/env python3
"""
VWO GenAI Internship Assignment - CLI Functionality Testing Script
Tests the actual CLI application functionality and user workflows
"""

import subprocess
import tempfile
import time
from pathlib import Path
import sys

class CLIFunctionalTester:
    """Test CLI application functionality and user workflows"""
    
    def __init__(self):
        self.test_results = []
        self.temp_files = []
        self.test_timeout = 30  # seconds
    
    def cleanup(self):
        """Clean up temporary test files"""
        for temp_file in self.temp_files:
            try:
                if Path(temp_file).exists():
                    Path(temp_file).unlink()
            except:
                pass
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if details:
            print(f"    💬 {details}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details
        })
    
    def create_test_blood_file(self, filename: str = None) -> str:
        """Create a test blood test file"""
        if filename is None:
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
            filename = temp_file.name
            self.temp_files.append(filename)
        else:
            temp_file = open(filename, 'w')
        
        test_content = """
COMPREHENSIVE BLOOD TEST REPORT
Laboratory: VWO Test Lab
Date: 2025-06-29

COMPLETE BLOOD COUNT (CBC):
White Blood Cells: 7.2 K/uL (Normal: 4.0-11.0)
Red Blood Cells: 4.5 M/uL (Normal: 4.2-5.9)
Hemoglobin: 14.2 g/dL (Normal: 12.0-16.0)

BASIC METABOLIC PANEL:
Glucose: 95 mg/dL (Normal: 70-100)
Cholesterol: 185 mg/dL (Normal: <200)
"""
        temp_file.write(test_content)
        temp_file.close()
        
        return filename
    
    def test_cli_help_commands(self):
        """Test CLI help and version commands"""
        print("\n🔍 Testing CLI Help Commands...")
        
        # Test --help
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '--help'],
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if result.returncode == 0 and 'VWO Blood Test Analysis' in result.stdout:
                self.log_test("Help command", True, "Help text displays correctly")
            else:
                self.log_test("Help command", False, f"Return code: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            self.log_test("Help command", False, "Command timed out")
        except Exception as e:
            self.log_test("Help command", False, f"Error: {e}")
        
        # Test --version
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '--version'],
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if result.returncode == 0 and '2.0.0' in result.stdout:
                self.log_test("Version command", True, "Version displays correctly")
            else:
                self.log_test("Version command", False, f"Return code: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            self.log_test("Version command", False, "Command timed out")
        except Exception as e:
            self.log_test("Version command", False, f"Error: {e}")
    
    def test_file_validation(self):
        """Test file validation functionality"""
        print("\n🔍 Testing File Validation...")
        
        # Test 1: Non-existent file
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', 'nonexistent_file.pdf', '-q', 'Test query'],
                input='yes\n',  # Accept disclaimer
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if 'File not found' in result.stdout or 'not found' in result.stderr:
                self.log_test("Non-existent file handling", True, "Correctly rejects missing files")
            else:
                self.log_test("Non-existent file handling", False, "Should reject missing files")
                
        except subprocess.TimeoutExpired:
            self.log_test("Non-existent file handling", False, "Command timed out")
        except Exception as e:
            self.log_test("Non-existent file handling", False, f"Error: {e}")
        
        # Test 2: Invalid file type
        try:
            # Create fake image file
            fake_image = tempfile.NamedTemporaryFile(mode='w', suffix='.jpg', delete=False)
            fake_image.write("fake image content")
            fake_image.close()
            self.temp_files.append(fake_image.name)
            
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', fake_image.name, '-q', 'Test query'],
                input='yes\n',
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if 'Unsupported file format' in result.stdout or 'not supported' in result.stderr:
                self.log_test("Invalid file type handling", True, "Correctly rejects unsupported formats")
            else:
                self.log_test("Invalid file type handling", False, "Should reject unsupported formats")
                
        except subprocess.TimeoutExpired:
            self.log_test("Invalid file type handling", False, "Command timed out")
        except Exception as e:
            self.log_test("Invalid file type handling", False, f"Error: {e}")
    
    def test_query_validation(self):
        """Test query validation functionality"""
        print("\n🔍 Testing Query Validation...")
        
        # Create valid test file
        test_file = self.create_test_blood_file()
        
        # Test 1: Too short query
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', test_file, '-q', 'x'],
                input='yes\n',
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if 'must be at least' in result.stdout or 'too short' in result.stderr:
                self.log_test("Short query validation", True, "Correctly rejects short queries")
            else:
                self.log_test("Short query validation", False, "Should reject short queries")
                
        except subprocess.TimeoutExpired:
            self.log_test("Short query validation", False, "Command timed out")
        except Exception as e:
            self.log_test("Short query validation", False, f"Error: {e}")
        
        # Test 2: Valid query
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', test_file, '-q', 'Analyze my cholesterol levels'],
                input='yes\n',
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if 'Query validated' in result.stdout:
                self.log_test("Valid query acceptance", True, "Accepts properly formatted queries")
            else:
                self.log_test("Valid query acceptance", False, "Should accept valid queries")
                
        except subprocess.TimeoutExpired:
            self.log_test("Valid query acceptance", False, "Command timed out")
        except Exception as e:
            self.log_test("Valid query acceptance", False, f"Error: {e}")
    
    def test_system_validation(self):
        """Test system validation on startup"""
        print("\n🔍 Testing System Validation...")
        
        # Create valid test file
        test_file = self.create_test_blood_file()
        
        try:
            # Run with valid inputs to check system validation
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', test_file, '-q', 'Test system validation'],
                input='yes\n',
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            validation_checks = [
                'Task workflow dependencies validated',
                'Multi-agent system (doctor + verifier) ready',
                'Tool integration (file reader + search) confirmed',
                'Required directories initialized',
                'All system validations passed'
            ]
            
            passed_validations = sum(1 for check in validation_checks if check in result.stdout)
            
            if passed_validations >= 4:
                self.log_test("System validation", True, f"Passed {passed_validations}/5 validation checks")
            else:
                self.log_test("System validation", False, f"Only {passed_validations}/5 validations passed")
                
        except subprocess.TimeoutExpired:
            self.log_test("System validation", False, "Command timed out")
        except Exception as e:
            self.log_test("System validation", False, f"Error: {e}")
    
    def test_medical_disclaimer_flow(self):
        """Test medical disclaimer acceptance flow"""
        print("\n🔍 Testing Medical Disclaimer Flow...")
        
        test_file = self.create_test_blood_file()
        
        # Test 1: Disclaimer acceptance
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', test_file, '-q', 'Test disclaimer'],
                input='yes\n',
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if 'IMPORTANT MEDICAL DISCLAIMER' in result.stdout and 'Medical disclaimer acknowledged' in result.stdout:
                self.log_test("Medical disclaimer display", True, "Displays and processes disclaimer correctly")
            else:
                self.log_test("Medical disclaimer display", False, "Disclaimer not properly displayed")
                
        except subprocess.TimeoutExpired:
            self.log_test("Medical disclaimer display", False, "Command timed out")
        except Exception as e:
            self.log_test("Medical disclaimer display", False, f"Error: {e}")
        
        # Test 2: Disclaimer rejection
        try:
            result = subprocess.run(
                [sys.executable, 'main.py', '-f', test_file, '-q', 'Test disclaimer rejection'],
                input='no\n',
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )
            
            if 'Analysis cancelled for safety compliance' in result.stdout:
                self.log_test("Medical disclaimer rejection", True, "Properly handles disclaimer rejection")
            else:
                self.log_test("Medical disclaimer rejection", False, "Should cancel on disclaimer rejection")
                
        except subprocess.TimeoutExpired:
            self.log_test("Medical disclaimer rejection", False, "Command timed out")
        except Exception as e:
            self.log_test("Medical disclaimer rejection", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Run all CLI functionality tests"""
        print("🧪 VWO GenAI Internship Assignment - CLI Functionality Testing")
        print("=" * 70)
        print("🔬 Testing CLI application functionality and user workflows")
        print("📋 Validating bug fixes and user experience")
        print("=" * 70)
        
        # Ensure data directory exists
        Path("data").mkdir(exist_ok=True)
        
        test_functions = [
            ("CLI Help Commands", self.test_cli_help_commands),
            ("File Validation", self.test_file_validation),
            ("Query Validation", self.test_query_validation),
            ("System Validation", self.test_system_validation),
            ("Medical Disclaimer Flow", self.test_medical_disclaimer_flow),
        ]
        
        for test_name, test_function in test_functions:
            try:
                test_function()
            except Exception as e:
                print(f"\n❌ {test_name} test failed: {e}")
                self.log_test(f"{test_name} (category)", False, f"Test category failed: {e}")
        
        # Print summary
        self.print_summary()
        
        # Cleanup
        self.cleanup()
        
        return all(result['success'] for result in self.test_results)
    
    def print_summary(self):
        """Print test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 70)
        print("📊 CLI FUNCTIONALITY TESTING RESULTS")
        print("=" * 70)
        
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL CLI FUNCTIONALITY TESTS PASSED!")
            print(f"🚀 Your CLI application is fully functional!")
            print(f"✅ Ready for VWO submission with confidence!")
        elif failed_tests <= 2:
            print(f"\n⚠️  MINOR ISSUES DETECTED")
            print(f"🔧 Most functionality working correctly")
        else:
            print(f"\n🚨 SIGNIFICANT ISSUES DETECTED")
            print(f"🔧 Please address failing tests before submission")

def main():
    """Main testing function"""
    try:
        tester = CLIFunctionalTester()
        success = tester.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())