"""
Fixed Tools Module for Blood Test Analysis System
VWO GenAI Internship - Debug Challenge Solution
All bugs resolved: #9, #10, #11, #12, #13, #14, #15, #16
"""

## Importing libraries and files
import os
import re
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tool
from crewai_tools.tools.serper_dev_tool import SerperDevTool

# PDF processing imports
try:
    import pypdf
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        from PyPDF2 import PdfReader
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False
        print("Warning: No PDF library found. Install pypdf or PyPDF2 for PDF processing.")

## Creating search tool
search_tool = SerperDevTool()

## Creating custom PDF reader tool
class BloodTestReportTool:
    """Tool for reading and processing blood test reports from PDF files"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']
    
    @tool("Read Blood Test Report")
    def read_data_tool(self, path: str = 'data/sample.pdf') -> str:
        """
        Tool to read data from a PDF or text file containing blood test results
        
        Args:
            path (str): Path to the blood test report file. Defaults to 'data/sample.pdf'.
        
        Returns:
            str: Cleaned and formatted blood test report content
        """
        try:
            # Validate file exists
            if not os.path.exists(path):
                return f"Error: File not found at path: {path}"
            
            # Get file extension
            file_ext = os.path.splitext(path)[1].lower()
            
            if file_ext == '.pdf':
                return self._read_pdf_file(path)
            elif file_ext == '.txt':
                return self._read_text_file(path)
            else:
                return f"Error: Unsupported file format: {file_ext}. Supported formats: {self.supported_formats}"
                
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _read_pdf_file(self, path: str) -> str:
        """Read PDF file and extract text content"""
        if not PDF_AVAILABLE:
            return "Error: PDF processing library not available. Please install pypdf or PyPDF2."
        
        try:
            full_report = ""
            
            with open(path, 'rb') as file:
                pdf_reader = PdfReader(file)
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            full_report += f"\n--- Page {page_num + 1} ---\n"
                            full_report += page_text + "\n"
                    except Exception as e:
                        full_report += f"\n--- Page {page_num + 1} (Error reading) ---\n"
                        full_report += f"Error extracting text from page {page_num + 1}: {str(e)}\n"
            
            # Clean and format the extracted text
            cleaned_report = self._clean_report_text(full_report)
            
            if not cleaned_report.strip():
                return "Warning: No readable text found in PDF. File may be image-based or corrupted."
            
            return cleaned_report
            
        except Exception as e:
            return f"Error processing PDF file: {str(e)}"
    
    def _read_text_file(self, path: str) -> str:
        """Read plain text file content"""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return self._clean_report_text(content)
            
        except UnicodeDecodeError:
            try:
                # Try with different encoding
                with open(path, 'r', encoding='latin-1') as file:
                    content = file.read()
                return self._clean_report_text(content)
            except Exception as e:
                return f"Error reading text file with alternative encoding: {str(e)}"
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def _clean_report_text(self, content: str) -> str:
        """Clean and format blood test report text efficiently"""
        if not content:
            return ""
        
        # Remove excessive whitespace and clean formatting using regex (Bug #13 fixed)
        # Replace multiple newlines with double newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Replace multiple spaces with single spaces
        content = re.sub(r' {2,}', ' ', content)
        
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in content.split('\n')]
        content = '\n'.join(lines)
        
        # Remove empty lines at start and end
        content = content.strip()
        
        return content

## Creating Nutrition Analysis Tool
class NutritionAnalysisTool:
    """Tool for analyzing nutritional aspects of blood test results"""
    
    @tool("Analyze Nutrition from Blood Work")
    def analyze_nutrition_from_blood(self, blood_report_data: str) -> str:
        """
        Analyze blood test data for nutritional insights
        
        Args:
            blood_report_data (str): Blood test report content
            
        Returns:
            str: Nutritional analysis based on blood markers
        """
        try:
            if not blood_report_data or blood_report_data.startswith("Error:"):
                return "Error: No valid blood test data provided for nutrition analysis"
            
            # Extract key nutritional markers
            markers = self._extract_nutrition_markers(blood_report_data)
            
            # Generate nutrition recommendations
            recommendations = self._generate_nutrition_recommendations(markers)
            
            return recommendations
            
        except Exception as e:
            return f"Error in nutrition analysis: {str(e)}"
    
    def _extract_nutrition_markers(self, blood_data: str) -> dict:
        """Extract nutrition-related blood markers"""
        markers = {}
        
        # Common patterns for blood values
        patterns = {
            'glucose': r'glucose[:\s]*(\d+\.?\d*)',
            'cholesterol': r'cholesterol[:\s]*(\d+\.?\d*)',
            'hdl': r'hdl[:\s]*(\d+\.?\d*)',
            'ldl': r'ldl[:\s]*(\d+\.?\d*)',
            'triglycerides': r'triglycerides?[:\s]*(\d+\.?\d*)',
            'vitamin_d': r'vitamin\s*d[:\s]*(\d+\.?\d*)',
            'b12': r'b12|vitamin\s*b12[:\s]*(\d+\.?\d*)',
            'iron': r'iron[:\s]*(\d+\.?\d*)',
            'hemoglobin': r'hemoglobin[:\s]*(\d+\.?\d*)'
        }
        
        blood_data_lower = blood_data.lower()
        
        for marker, pattern in patterns.items():
            matches = re.search(pattern, blood_data_lower)
            if matches:
                try:
                    markers[marker] = float(matches.group(1))
                except ValueError:
                    continue
        
        return markers
    
    def _generate_nutrition_recommendations(self, markers: dict) -> str:
        """Generate nutrition recommendations based on markers"""
        if not markers:
            return "NUTRITION ANALYSIS: Insufficient blood marker data for detailed analysis"
        
        recommendations = "NUTRITION ANALYSIS BASED ON BLOOD MARKERS\n"
        recommendations += "=" * 45 + "\n\n"
        
        recommendations += "DETECTED MARKERS:\n"
        for marker, value in markers.items():
            recommendations += f"• {marker.replace('_', ' ').title()}: {value}\n"
        
        recommendations += "\nGENERAL NUTRITION RECOMMENDATIONS:\n"
        
        if 'glucose' in markers:
            recommendations += "• Monitor carbohydrate intake and focus on complex carbs\n"
            recommendations += "• Consider smaller, frequent meals to stabilize blood sugar\n"
        
        if 'cholesterol' in markers or 'hdl' in markers or 'ldl' in markers:
            recommendations += "• Emphasize heart-healthy fats (omega-3, olive oil)\n"
            recommendations += "• Increase fiber intake with fruits, vegetables, and whole grains\n"
        
        if 'hemoglobin' in markers or 'iron' in markers:
            recommendations += "• Ensure adequate iron-rich foods (lean meats, spinach, legumes)\n"
            recommendations += "• Pair iron sources with vitamin C for better absorption\n"
        
        if 'vitamin_d' in markers:
            recommendations += "• Consider vitamin D-rich foods (fatty fish, fortified dairy)\n"
        
        if 'b12' in markers:
            recommendations += "• Include B12 sources (meat, fish, dairy, fortified foods)\n"
        
        recommendations += "\nIMPORTANT: This analysis is for informational purposes only.\n"
        recommendations += "Consult with a registered dietitian for personalized nutrition planning.\n"
        
        return recommendations

## Creating Exercise Planning Tool  
class ExercisePlanningTool:
    """Tool for creating exercise recommendations based on blood test results"""
    
    @tool("Create Exercise Plan from Blood Work")
    def create_exercise_plan_from_blood(self, blood_report_data: str) -> str:
        """
        Create exercise recommendations based on blood test results
        
        Args:
            blood_report_data (str): Blood test report content
            
        Returns:
            str: Exercise recommendations based on health markers
        """
        try:
            if not blood_report_data or blood_report_data.startswith("Error:"):
                return "Error: No valid blood test data provided for exercise planning"
            
            # Analyze cardiovascular and metabolic markers
            health_markers = self._assess_exercise_readiness(blood_report_data)
            
            # Generate exercise recommendations
            exercise_plan = self._generate_exercise_recommendations(health_markers)
            
            return exercise_plan
            
        except Exception as e:
            return f"Error in exercise planning: {str(e)}"
    
    def _assess_exercise_readiness(self, blood_data: str) -> dict:
        """Assess exercise readiness from blood markers"""
        assessment = {
            'cardiovascular_risk': 'unknown',
            'metabolic_health': 'unknown',
            'energy_levels': 'unknown',
            'recommendations': []
        }
        
        blood_data_lower = blood_data.lower()
        
        # Basic assessment based on common markers
        if 'glucose' in blood_data_lower:
            assessment['metabolic_health'] = 'needs_monitoring'
            assessment['recommendations'].append('Monitor blood sugar before/after exercise')
        
        if 'cholesterol' in blood_data_lower:
            assessment['cardiovascular_risk'] = 'present'
            assessment['recommendations'].append('Focus on cardiovascular exercises')
        
        if 'hemoglobin' in blood_data_lower:
            assessment['energy_levels'] = 'assess_based_on_levels'
            assessment['recommendations'].append('Monitor energy during exercise')
        
        if 'blood pressure' in blood_data_lower:
            assessment['cardiovascular_risk'] = 'monitor'
            assessment['recommendations'].append('Avoid high-intensity exercises initially')
        
        return assessment
    
    def _generate_exercise_recommendations(self, health_markers: dict) -> str:
        """Generate exercise plan based on health assessment"""
        plan = "EXERCISE RECOMMENDATIONS BASED ON BLOOD WORK\n"
        plan += "=" * 42 + "\n\n"
        
        plan += "GENERAL EXERCISE GUIDELINES:\n"
        plan += "• Start slowly and progress gradually\n"
        plan += "• Monitor how you feel during exercise\n"
        plan += "• Stay hydrated and maintain proper nutrition\n"
        plan += "• Warm up before and cool down after exercise\n"
        plan += "• Stop if you experience chest pain, dizziness, or shortness of breath\n\n"
        
        plan += "RECOMMENDED ACTIVITIES:\n"
        plan += "• Walking: Start with 10-15 minutes daily, increase gradually\n"
        plan += "• Swimming: Low-impact, full-body exercise\n"
        plan += "• Cycling: Good cardiovascular workout\n"
        plan += "• Strength training: 2-3 times per week with light weights\n"
        plan += "• Yoga/Stretching: Improve flexibility and reduce stress\n\n"
        
        if health_markers.get('recommendations'):
            plan += "SPECIFIC CONSIDERATIONS BASED ON YOUR BLOOD WORK:\n"
            for rec in health_markers['recommendations']:
                plan += f"• {rec}\n"
            plan += "\n"
        
        plan += "MONITORING GUIDELINES:\n"
        plan += "• Track your heart rate during exercise\n"
        plan += "• Keep a log of how you feel before/after workouts\n"
        plan += "• Progress gradually - increase intensity/duration by 10% weekly\n"
        plan += "• Schedule rest days for recovery\n\n"
        
        plan += "IMPORTANT DISCLAIMER:\n"
        plan += "This is general guidance based on available data.\n"
        plan += "Consult with a certified exercise physiologist or your healthcare provider\n"
        plan += "before starting any new exercise program, especially if you have health conditions.\n"
        
        return plan

# Export tools for use in agents
__all__ = ['BloodTestReportTool', 'NutritionAnalysisTool', 'ExercisePlanningTool', 'search_tool']