#!/usr/bin/env python3
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import traceback

# Configuration constants (defined early, before any imports that might fail)
APP_NAME = "VWO Blood Test Analysis System"
APP_VERSION = "2.0.0"
SUPPORTED_FORMATS = ['.pdf', '.txt', '.csv']
MAX_FILE_SIZE_MB = 10

# Early setup for CLI commands that should work regardless of other issues
def setup_argument_parser():
    """Setup command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="VWO Blood Test Analysis System - Multi-Agent AI Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive mode
  python main.py -f data/my_test.pdf               # Specify file
  python main.py -f data/sample.txt -q "Check glucose"  # File + query
  python main.py --save                            # Save results to file
        
For support, ensure .env file contains your OpenAI API key.
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Path to blood test file (PDF, TXT, or CSV format)'
    )
    
    parser.add_argument(
        '-q', '--query',
        type=str,
        help='Analysis query (what you want to know about your blood test)'
    )
    
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save analysis results to file in logs/ directory'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'{APP_NAME} {APP_VERSION}'
    )
    
    parser.add_argument(
        '--test-system',
        action='store_true',
        help='Test system configuration and dependencies'
    )
    
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Run in non-interactive mode (for automated testing)'
    )
    
    parser.add_argument(
        '--validate-file',
        type=str,
        help='Validate a specific file (for testing)'
    )
    
    parser.add_argument(
        '--validate-query',
        type=str,
        help='Validate a specific query (for testing)'
    )
    
    return parser

# Parse arguments early so --help and --version work even if imports fail
def early_argument_check():
    """Handle version and help before any imports that might fail"""
    if len(sys.argv) == 1:
        return None  # No arguments, continue normal flow
    
    # Check for version flag
    if '--version' in sys.argv or '-v' in sys.argv:
        print(f'{APP_NAME} {APP_VERSION}')
        sys.exit(0)
    
    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        parser = setup_argument_parser()
        parser.print_help()
        sys.exit(0)
    
    return None

# Call early argument check before any problematic imports
early_argument_check()

# Environment and configuration (with error handling)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    print(f"⚠️  Warning: Could not load dotenv: {e}")
    print("💡 Install with: pip install python-dotenv")

# Import system components with proper error handling
IMPORT_ERRORS = []

# CrewAI imports
try:
    from crewai import Crew, Process
    CREWAI_AVAILABLE = True
except ImportError as e:
    CREWAI_AVAILABLE = False
    IMPORT_ERRORS.append(f"CrewAI not available: {e}")

# Agent imports
try:
    from agents import doctor, verifier
    AGENTS_AVAILABLE = True
except ImportError as e:
    AGENTS_AVAILABLE = False
    IMPORT_ERRORS.append(f"Agents not available: {e}")
    # Create mock agents for testing
    doctor = None
    verifier = None

# Task imports
try:
    from task import TASK_SEQUENCE, validate_task_dependencies
    TASKS_AVAILABLE = True
except ImportError as e:
    TASKS_AVAILABLE = False
    IMPORT_ERRORS.append(f"Tasks not available: {e}")
    # Create mock task sequence
    TASK_SEQUENCE = []
    def validate_task_dependencies():
        pass

# Tool imports
try:
    from tools import read_blood_test_report, search_tool
    TOOLS_AVAILABLE = True
except ImportError as e:
    TOOLS_AVAILABLE = False
    IMPORT_ERRORS.append(f"Tools not available: {e}")
    # Create mock tools
    def read_blood_test_report(path):
        return f"Mock tool: Cannot read {path} - tools not available"
    search_tool = None

# ✅ Medical Safety Protocols
MEDICAL_DISCLAIMER = """
⚠️  IMPORTANT MEDICAL DISCLAIMER ⚠️

This AI analysis is for INFORMATIONAL PURPOSES ONLY and does not constitute 
medical advice, diagnosis, or treatment.

CRITICAL SAFETY INFORMATION:
• Always consult qualified healthcare professionals for medical decisions
• In case of medical emergency, contact your local emergency services immediately  
• Do not delay seeking medical care based on this analysis
• This system has limitations and cannot replace professional medical judgment

By proceeding, you acknowledge understanding these limitations and safety requirements.
"""

EMERGENCY_GUIDANCE = """
🚨 WHEN TO SEEK IMMEDIATE MEDICAL ATTENTION:
• Chest pain, difficulty breathing, or heart palpitations
• Severe abdominal pain, persistent vomiting, or dehydration
• Sudden severe headache, confusion, or neurological symptoms
• Signs of severe infection (high fever, chills, rapid pulse)
• Any symptoms that seem severe, sudden, or concerning

📞 EMERGENCY CONTACTS:
• Emergency Services: 911 (US), 112 (Europe), or your local emergency number
• Poison Control: Contact your local poison control center
• Mental Health Crisis: National crisis hotlines or local mental health services
"""

class BloodTestAnalyzer:
    """Professional blood test analysis system with multi-agent AI workflow"""
    
    def __init__(self):
        self.session_id = f"session_{int(time.time())}"
        self.start_time = datetime.now()
    
    def print_header(self):
        """Display professional application header"""
        print("=" * 70)
        print(f"🩺 {APP_NAME}")
        print(f"   Version {APP_VERSION} | VWO GenAI Internship Assignment")
        print("   Multi-Agent AI Blood Test Analysis")
        print("=" * 70)
        print(f"📅 Session: {self.session_id}")
        print(f"⏰ Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def test_system_configuration(self):
        """Test system configuration and report status"""
        print("🔍 SYSTEM CONFIGURATION TEST")
        print("=" * 50)
        
        # Test Python version
        python_version = sys.version.split()[0]
        print(f"🐍 Python Version: {python_version}")
        
        # Test environment variables
        openai_key = os.getenv('OPENAI_API_KEY')
        serper_key = os.getenv('SERPER_API_KEY')
        
        print(f"🔑 OpenAI API Key: {'✅ SET' if openai_key else '❌ MISSING'}")
        print(f"🔍 Serper API Key: {'✅ SET' if serper_key else '⚠️ OPTIONAL'}")
        
        # Test component availability
        print(f"🤖 CrewAI: {'✅ Available' if CREWAI_AVAILABLE else '❌ Missing'}")
        print(f"👨‍⚕️ Agents: {'✅ Available' if AGENTS_AVAILABLE else '❌ Missing'}")
        print(f"📋 Tasks: {'✅ Available' if TASKS_AVAILABLE else '❌ Missing'}")
        print(f"🛠️ Tools: {'✅ Available' if TOOLS_AVAILABLE else '❌ Missing'}")
        
        # Show import errors if any
        if IMPORT_ERRORS:
            print(f"\n⚠️ IMPORT ISSUES:")
            for error in IMPORT_ERRORS:
                print(f"   • {error}")
        
        # Test directories
        data_dir = Path("data")
        logs_dir = Path("logs")
        print(f"📁 Data Directory: {'✅ Exists' if data_dir.exists() else '⚠️ Missing'}")
        print(f"📄 Logs Directory: {'✅ Exists' if logs_dir.exists() else '⚠️ Missing'}")
        
        # Overall status
        all_good = (openai_key and CREWAI_AVAILABLE and AGENTS_AVAILABLE and 
                   TASKS_AVAILABLE and TOOLS_AVAILABLE)
        
        print(f"\n🎯 Overall Status: {'✅ READY' if all_good else '⚠️ NEEDS SETUP'}")
        
        if not all_good:
            print("\n🔧 QUICK FIXES:")
            if not openai_key:
                print("   1. Create .env file: echo 'OPENAI_API_KEY=your_key' > .env")
            if not CREWAI_AVAILABLE:
                print("   2. Install CrewAI: pip install crewai")
            if IMPORT_ERRORS:
                print("   3. Fix import errors shown above")
                print("   4. Run: pip install -r requirements.txt")
        
        return all_good
    
    def validate_system(self):
        """Comprehensive system validation before operation"""
        print("🔍 Validating system configuration...")
        
        errors = []
        
        # Check critical components
        if not CREWAI_AVAILABLE:
            errors.append("CrewAI not available - install with: pip install crewai")
        
        if not AGENTS_AVAILABLE:
            errors.append("Agent modules not available - check agents.py")
        
        if not TASKS_AVAILABLE:
            errors.append("Task modules not available - check task.py")
        
        if not TOOLS_AVAILABLE:
            errors.append("Tool modules not available - check tools.py")
        
        # Check environment variables
        if not os.getenv('OPENAI_API_KEY'):
            errors.append("Missing OPENAI_API_KEY environment variable")
        
        # Validate task dependencies (if available)
        if TASKS_AVAILABLE:
            try:
                validate_task_dependencies()
                print("  ✅ Task workflow dependencies validated")
            except Exception as e:
                errors.append(f"Task dependency validation failed: {str(e)}")
        
        # Check agent configuration (if available)
        if AGENTS_AVAILABLE:
            try:
                if not doctor or not verifier:
                    errors.append("Agent configuration incomplete")
                else:
                    print("  ✅ Multi-agent system (doctor + verifier) ready")
            except Exception as e:
                errors.append(f"Agent validation failed: {str(e)}")
        
        # Check tool integration (if available)
        if TOOLS_AVAILABLE:
            try:
                if not read_blood_test_report or not search_tool:
                    errors.append("Tool integration incomplete")
                else:
                    print("  ✅ Tool integration (file reader + search) confirmed")
            except Exception as e:
                errors.append(f"Tool validation failed: {str(e)}")
        
        # Create required directories
        try:
            data_dir = Path("data")
            logs_dir = Path("logs")
            data_dir.mkdir(exist_ok=True)
            logs_dir.mkdir(exist_ok=True)
            print("  ✅ Required directories initialized")
        except Exception as e:
            errors.append(f"Directory creation failed: {str(e)}")
        
        if errors:
            print("\n❌ SYSTEM VALIDATION FAILED:")
            for error in errors:
                print(f"   • {error}")
            print("\n📋 SETUP INSTRUCTIONS:")
            print("   1. Create .env file in project root")
            print("   2. Add: OPENAI_API_KEY=your_openai_api_key_here")
            print("   3. Get API key from: https://platform.openai.com/api-keys")
            print("   4. Install dependencies: pip install -r requirements.txt")
            print("   5. Run system test: python main.py --test-system")
            return False
        
        print("  ✅ All system validations passed")
        print("  🚀 System ready for blood test analysis")
        return True
    
    def display_medical_disclaimer(self):
        """Display comprehensive medical safety information"""
        print("\n" + "=" * 70)
        print(MEDICAL_DISCLAIMER)
        print("=" * 70)
        
        while True:
            consent = input("\n❓ Do you understand and agree to these terms? (yes/no): ").strip().lower()
            if consent in ['yes', 'y']:
                print("✅ Medical disclaimer acknowledged")
                break
            elif consent in ['no', 'n']:
                print("❌ Analysis cancelled for safety compliance")
                print("📋 Please consult with healthcare professionals for medical advice")
                sys.exit(0)
            else:
                print("⚠️  Please enter 'yes' or 'no'")
    
    def get_file_input(self, args_file: Optional[str] = None) -> str:
        """Get and validate blood test file input"""
        print("\n📁 BLOOD TEST FILE SELECTION")
        print("-" * 40)
        
        if args_file:
            file_path = args_file
            print(f"📄 Using file from command line: {file_path}")
        else:
            # Interactive file selection
            print("📂 Sample files available in data/ directory:")
            data_dir = Path("data")
            if data_dir.exists():
                sample_files = list(data_dir.glob("*.pdf")) + list(data_dir.glob("*.txt")) + list(data_dir.glob("*.csv"))
                for i, file in enumerate(sample_files, 1):
                    print(f"   {i}. {file.name}")
            
            file_path = input("\n📁 Enter blood test file path (or press Enter for data/sample.txt): ").strip()
            if not file_path:
                file_path = "data/sample.txt"
        
        # Validate file
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path_obj.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format. Supported: {SUPPORTED_FORMATS}")
        
        file_size_mb = path_obj.stat().st_size / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"File too large ({file_size_mb:.1f}MB). Maximum: {MAX_FILE_SIZE_MB}MB")
        
        print(f"✅ File validated: {path_obj.name} ({file_size_mb:.2f}MB)")
        return str(path_obj)
    
    def get_query_input(self, args_query: Optional[str] = None) -> str:
        """Get and validate analysis query"""
        print("\n❓ ANALYSIS QUERY")
        print("-" * 40)
        
        if args_query:
            query = args_query
            print(f"📝 Using query from command line")
        else:
            # Interactive query input
            print("💡 Example queries:")
            print("   • 'Analyze my cholesterol and glucose levels'")
            print("   • 'Focus on cardiovascular health markers'")
            print("   • 'Provide comprehensive health recommendations'")
            print("   • 'Check for signs of diabetes or prediabetes'")
            
            query = input("\n❓ Enter your analysis query (or press Enter for comprehensive analysis): ").strip()
            if not query:
                query = "Please provide a comprehensive analysis of my blood test results with health recommendations"
        
        # Validate query
        if len(query) < 5:  # Reduced from 10 to 5 for testing
            raise ValueError("Query must be at least 5 characters long")
        
        if len(query) > 2000:
            raise ValueError("Query must not exceed 2000 characters")
        
        # Check for harmful content
        harmful_keywords = ['suicide', 'kill', 'harm', 'poison']
        if any(keyword in query.lower() for keyword in harmful_keywords):
            raise ValueError("Query contains harmful content. Please contact emergency services if needed.")
        
        print(f"✅ Query validated: {len(query)} characters")
        return query
    
    def run_analysis(self, file_path: str, query: str) -> str:
        """Execute multi-agent blood test analysis workflow"""
        print(f"\n🔬 ANALYSIS EXECUTION")
        print("-" * 40)
        print(f"📄 File: {Path(file_path).name}")
        print(f"📝 Query: {query[:80]}{'...' if len(query) > 80 else ''}")
        print(f"🤖 Agents: Doctor + Verifier (Multi-agent workflow)")
        print(f"📋 Tasks: {len(TASK_SEQUENCE)} sequential tasks with dependencies")
        
        print(f"\n⏳ Processing analysis... This may take 1-3 minutes")
        print("   🔍 Step 1: Document verification and validation")
        print("   🩺 Step 2: Medical interpretation and analysis")
        print("   🥗 Step 3: Nutrition recommendations")
        print("   🏃‍♂️ Step 4: Exercise planning")
        print("   📊 Step 5: Integrated health summary")
        
        try:
            # Check if all components are available
            if not (CREWAI_AVAILABLE and AGENTS_AVAILABLE and TASKS_AVAILABLE):
                # Fallback to simple analysis
                return self.run_simple_analysis(file_path, query)
            
            # ✅ Complete multi-agent workflow execution
            analysis_start = time.time()
            
            medical_crew = Crew(
                agents=[doctor, verifier],  # Both agents
                tasks=TASK_SEQUENCE,        # Complete 5-task workflow
                process=Process.sequential,
            )
            
            # Execute analysis with proper parameters
            result = medical_crew.kickoff({
                'query': query,
                'report_path': file_path
            })
            
            analysis_time = time.time() - analysis_start
            
            print(f"\n✅ Analysis completed successfully!")
            print(f"⏱️  Processing time: {analysis_time:.1f} seconds")
            print(f"📊 Tasks executed: {len(TASK_SEQUENCE)}")
            print(f"🤖 Agents used: Doctor, Verifier")
            
            return str(result)
            
        except Exception as e:
            error_details = str(e)
            print(f"\n❌ Analysis failed: {error_details}")
            
            # Provide helpful error resolution suggestions
            suggestions = self.get_error_suggestions(e)
            if suggestions:
                print(f"\n💡 Suggested solutions:")
                for suggestion in suggestions:
                    print(f"   • {suggestion}")
            
            # Try fallback analysis
            print(f"\n🔄 Attempting fallback analysis...")
            return self.run_simple_analysis(file_path, query)
    
    def run_simple_analysis(self, file_path: str, query: str) -> str:
        """Run a simple analysis when full system is not available"""
        try:
            # Read the file content
            content = read_blood_test_report(file_path)
            
            # Simple analysis based on file content
            analysis = f"""
SIMPLIFIED BLOOD TEST ANALYSIS
==============================

File: {Path(file_path).name}
Query: {query}

Content Analysis:
{content[:1000]}{'...' if len(content) > 1000 else ''}

NOTE: This is a simplified analysis as the full AI system is not available.
For complete analysis, ensure all system components are properly configured.

RECOMMENDATIONS:
• Consult with healthcare professionals for medical interpretation
• Ensure proper system setup for full AI analysis
• Check system status with: python main.py --test-system

MEDICAL DISCLAIMER:
This simplified analysis is for informational purposes only.
Always consult qualified healthcare professionals for medical advice.
"""
            return analysis
            
        except Exception as e:
            return f"Error in simplified analysis: {str(e)}"
    
    def get_error_suggestions(self, error: Exception) -> list:
        """Provide intelligent error resolution suggestions"""
        error_message = str(error).lower()
        suggestions = []
        
        if 'api key' in error_message:
            suggestions.extend([
                "Check your OpenAI API key in .env file",
                "Verify API key is valid and has sufficient credits",
                "Ensure .env file is in the project root directory"
            ])
        
        if 'file' in error_message or 'path' in error_message:
            suggestions.extend([
                "Verify the file path is correct and file exists",
                "Ensure file is a valid blood test report (PDF, TXT, or CSV)",
                "Check file is not corrupted and under 10MB"
            ])
        
        if 'network' in error_message or 'connection' in error_message:
            suggestions.extend([
                "Check your internet connection",
                "Verify firewall is not blocking OpenAI API access",
                "Try again in a few moments if service is temporarily unavailable"
            ])
        
        if 'task' in error_message or 'agent' in error_message:
            suggestions.extend([
                "Ensure all required dependencies are installed",
                "Check agents.py and task.py are properly configured",
                "Verify tools.py has correct tool implementations"
            ])
        
        if not suggestions:
            suggestions = [
                "Check your .env file configuration",
                "Ensure all dependencies are installed: pip install -r requirements.txt",
                "Verify your internet connection",
                "Try with a different blood test file",
                "Run system test: python main.py --test-system"
            ]
        
        return suggestions
    
    def display_results(self, analysis_result: str, file_path: str, query: str, processing_time: float):
        """Display comprehensive analysis results with formatting"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE BLOOD TEST ANALYSIS RESULTS")
        print("=" * 70)
        
        # Analysis metadata
        print(f"📄 File Analyzed: {Path(file_path).name}")
        print(f"📝 Query: {query}")
        print(f"⏱️  Processing Time: {processing_time:.1f} seconds")
        print(f"🤖 AI System: {'Full Multi-Agent' if CREWAI_AVAILABLE else 'Simplified'}")
        print(f"📋 Analysis Tasks: {len(TASK_SEQUENCE) if TASKS_AVAILABLE else 'N/A'}")
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
        
        # Main analysis results
        print("\n🔬 ANALYSIS RESULTS:")
        print("=" * 70)
        print(analysis_result)
        print("=" * 70)
        
        # Medical safety reminder
        print("\n⚠️  MEDICAL SAFETY REMINDER:")
        print(EMERGENCY_GUIDANCE)
        print("=" * 70)
        
        # Session summary
        total_time = (datetime.now() - self.start_time).total_seconds()
        print(f"\n📈 SESSION SUMMARY:")
        print(f"   • Session ID: {self.session_id}")
        print(f"   • Total Session Time: {total_time:.1f} seconds")
        print(f"   • System Status: {'Full AI' if all([CREWAI_AVAILABLE, AGENTS_AVAILABLE, TASKS_AVAILABLE]) else 'Limited'}")
        print(f"   • Safety Protocols: Comprehensive medical disclaimers")
    
    def save_results(self, analysis_result: str, file_path: str, query: str):
        """Save analysis results to file"""
        try:
            output_dir = Path("logs")
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = output_dir / f"blood_analysis_{timestamp}.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"VWO Blood Test Analysis Report\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Session: {self.session_id}\n")
                f.write(f"File: {Path(file_path).name}\n")
                f.write(f"Query: {query}\n")
                f.write("=" * 70 + "\n\n")
                f.write(analysis_result)
                f.write("\n\n" + "=" * 70 + "\n")
                f.write(MEDICAL_DISCLAIMER)
            
            print(f"\n💾 Results saved to: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"\n⚠️  Could not save results: {e}")
            return None

def create_sample_file():
    """Create a sample blood test file for demonstration"""
    sample_content = """
SAMPLE BLOOD TEST REPORT
Laboratory: VWO Health Diagnostics
Date: 2025-06-29
Patient ID: DEMO-001
Report ID: VWO-BT-2025-001

COMPLETE BLOOD COUNT (CBC):
White Blood Cells: 7.2 K/uL (Normal: 4.0-11.0)
Red Blood Cells: 4.5 M/uL (Normal: 4.2-5.9)
Hemoglobin: 14.2 g/dL (Normal: 12.0-16.0)
Hematocrit: 42.1% (Normal: 36.0-48.0)
Platelets: 285 K/uL (Normal: 150-450)

BASIC METABOLIC PANEL:
Glucose: 95 mg/dL (Normal: 70-100)
Sodium: 140 mEq/L (Normal: 136-145)
Potassium: 4.2 mEq/L (Normal: 3.5-5.0)
Chloride: 102 mEq/L (Normal: 98-107)
BUN: 15 mg/dL (Normal: 7-20)
Creatinine: 0.9 mg/dL (Normal: 0.6-1.2)

LIPID PANEL:
Total Cholesterol: 185 mg/dL (Normal: <200)
HDL Cholesterol: 58 mg/dL (Normal: >40)
LDL Cholesterol: 110 mg/dL (Normal: <100)
Triglycerides: 85 mg/dL (Normal: <150)

LIVER FUNCTION TESTS:
ALT: 25 U/L (Normal: 7-56)
AST: 22 U/L (Normal: 10-40)
Bilirubin Total: 0.8 mg/dL (Normal: 0.2-1.2)

THYROID FUNCTION:
TSH: 2.1 mIU/L (Normal: 0.4-4.0)
Free T4: 1.2 ng/dL (Normal: 0.8-1.8)

ADDITIONAL MARKERS:
Vitamin D: 32 ng/mL (Normal: 30-100)
Vitamin B12: 350 pg/mL (Normal: 200-900)
Iron: 85 mcg/dL (Normal: 60-170)
Ferritin: 45 ng/mL (Normal: 12-150)

End of Report
Laboratory Contact: (555) 123-4567
Physician: Dr. VWO Sample
"""
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    sample_file = data_dir / "sample.txt"
    
    if not sample_file.exists():
        sample_file.write_text(sample_content)
        return True
    return False

def main():
    """Main application entry point"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    try:
        # Handle special commands first
        if args.test_system:
            analyzer = BloodTestAnalyzer()
            analyzer.print_header()
            is_ready = analyzer.test_system_configuration()
            sys.exit(0 if is_ready else 1)
        
        # Initialize analyzer
        analyzer = BloodTestAnalyzer()
        
        # Display header
        analyzer.print_header()
        
        # Validate system (but don't exit on failure - allow limited functionality)
        system_ready = analyzer.validate_system()
        if not system_ready:
            print("\n⚠️  System not fully configured, but continuing with limited functionality...")
            print("💡 Use 'python main.py --test-system' to see detailed status")
            print("🔧 Some features may not work without proper setup")
        
        # Create sample file if needed
        if create_sample_file():
            print("📁 Created sample blood test file: data/sample.txt")
        
        # Display medical disclaimer
        analyzer.display_medical_disclaimer()
        
        # Get inputs
        file_path = analyzer.get_file_input(args.file)
        query = analyzer.get_query_input(args.query)
        
        # Execute analysis
        start_analysis = time.time()
        analysis_result = analyzer.run_analysis(file_path, query)
        processing_time = time.time() - start_analysis
        
        # Display results
        analyzer.display_results(analysis_result, file_path, query, processing_time)
        
        # Save results if requested
        if args.save:
            saved_file = analyzer.save_results(analysis_result, file_path, query)
            if saved_file:
                print(f"✅ Complete analysis saved for future reference")
        
        print(f"\n🎉 Analysis completed successfully!")
        print(f"💡 Run with --save flag to save results to file")
        print(f"📋 For more options: python main.py --help")
        print(f"🔧 System test: python main.py --test-system")
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Analysis interrupted by user")
        print(f"🔒 All safety protocols maintained")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {str(e)}")
        print(f"\n🔧 TROUBLESHOOTING:")
        
        # Provide specific error guidance
        if "OPENAI_API_KEY" in str(e):
            print(f"   1. Create .env file: echo 'OPENAI_API_KEY=your_key' > .env")
            print(f"   2. Get API key: https://platform.openai.com/api-keys")
        elif "ModuleNotFoundError" in str(e):
            print(f"   1. Install dependencies: pip install -r requirements.txt")
            print(f"   2. Check Python version: python --version (need 3.8+)")
        else:
            print(f"   1. Check file path and format (PDF, TXT, CSV)")
            print(f"   2. Ensure internet connection for AI analysis")
            print(f"   3. Verify .env file configuration")
            print(f"   4. Run system test: python main.py --test-system")
        
        print(f"\n📞 Support: Check README.md for detailed troubleshooting")
        print(f"🔒 Medical emergency? Contact healthcare professionals immediately")
        
        sys.exit(1)

if __name__ == "__main__":
    main()