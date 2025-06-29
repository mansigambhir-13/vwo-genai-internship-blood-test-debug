#!/usr/bin/env python3
"""
VWO GenAI Internship Assignment - Test Data Generator
Creates various blood test report files for comprehensive testing
"""

import os
import csv
from pathlib import Path

class TestDataGenerator:
    """Generate various types of test blood test reports"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.generated_files = []
    
    def create_normal_blood_test(self):
        """Create a normal blood test report"""
        content = """
COMPREHENSIVE BLOOD TEST REPORT
Laboratory: VWO Health Diagnostics
Date: 2025-06-29
Patient ID: NORMAL-001

COMPLETE BLOOD COUNT (CBC):
White Blood Cells: 7.2 K/uL (Normal: 4.0-11.0)
Red Blood Cells: 4.5 M/uL (Normal: 4.2-5.9)
Hemoglobin: 14.2 g/dL (Normal: 12.0-16.0)
Platelets: 285 K/uL (Normal: 150-450)

BASIC METABOLIC PANEL:
Glucose: 95 mg/dL (Normal: 70-100)
Sodium: 140 mEq/L (Normal: 136-145)
Potassium: 4.2 mEq/L (Normal: 3.5-5.0)
BUN: 15 mg/dL (Normal: 7-20)
Creatinine: 0.9 mg/dL (Normal: 0.6-1.2)

LIPID PANEL:
Total Cholesterol: 185 mg/dL (Normal: <200)
HDL Cholesterol: 58 mg/dL (Normal: >40)
LDL Cholesterol: 95 mg/dL (Normal: <100)
Triglycerides: 85 mg/dL (Normal: <150)

End of Report
"""
        
        filename = self.data_dir / "normal_blood_test.txt"
        filename.write_text(content)
        self.generated_files.append(filename)
        return filename
    
    def create_csv_blood_test(self):
        """Create a CSV format blood test"""
        csv_data = [
            ['Parameter', 'Value', 'Unit', 'Reference Range', 'Status'],
            ['White Blood Cells', '7.2', 'K/uL', '4.0-11.0', 'Normal'],
            ['Red Blood Cells', '4.5', 'M/uL', '4.2-5.9', 'Normal'],
            ['Hemoglobin', '14.2', 'g/dL', '12.0-16.0', 'Normal'],
            ['Glucose', '95', 'mg/dL', '70-100', 'Normal'],
            ['Total Cholesterol', '185', 'mg/dL', '<200', 'Normal'],
            ['HDL Cholesterol', '58', 'mg/dL', '>40', 'Good'],
            ['LDL Cholesterol', '110', 'mg/dL', '<100', 'Near Optimal'],
        ]
        
        filename = self.data_dir / "blood_test_csv.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
        
        self.generated_files.append(filename)
        return filename
    
    def create_sample_file(self):
        """Create default sample.txt file"""
        content = """
SAMPLE BLOOD TEST REPORT
Laboratory: VWO Test Lab
Date: 2025-06-29

COMPLETE BLOOD COUNT:
White Blood Cells: 7.2 K/uL (Normal: 4.0-11.0)
Red Blood Cells: 4.5 M/uL (Normal: 4.2-5.9)
Hemoglobin: 14.2 g/dL (Normal: 12.0-16.0)

CHEMISTRY:
Glucose: 95 mg/dL (Normal: 70-100)
Cholesterol: 185 mg/dL (Normal: <200)

End of Report
"""
        
        filename = self.data_dir / "sample.txt"
        filename.write_text(content)
        self.generated_files.append(filename)
        return filename
    
    def generate_all_test_files(self):
        """Generate all types of test files"""
        print("🧪 VWO Assignment - Test Data Generator")
        print("=" * 50)
        print("📋 Creating test blood report files")
        print("=" * 50)
        
        generators = [
            ("Normal Blood Test", self.create_normal_blood_test),
            ("CSV Format Test", self.create_csv_blood_test),
            ("Default Sample", self.create_sample_file),
        ]
        
        for name, generator in generators:
            try:
                result = generator()
                print(f"  ✅ {name}: {result.name}")
            except Exception as e:
                print(f"  ❌ {name}: Failed - {e}")
        
        # Summary
        print(f"\n📊 TEST DATA GENERATION COMPLETE")
        print(f"✅ Generated: {len(self.generated_files)} test files")
        print(f"📁 Location: {self.data_dir.absolute()}")
        
        # List all files
        print(f"\n📋 GENERATED FILES:")
        for file in sorted(self.data_dir.glob("*")):
            size = file.stat().st_size
            print(f"   • {file.name} ({size} bytes)")
        
        print(f"\n🧪 USAGE:")
        print(f"   • Test CLI: python main.py")
        print(f"   • Run tests: python run_all_tests.py")

def main():
    """Main function"""
    try:
        generator = TestDataGenerator()
        generator.generate_all_test_files()
        return 0
    except Exception as e:
        print(f"\n💥 Generation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())