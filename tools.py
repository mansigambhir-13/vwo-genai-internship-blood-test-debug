## Importing libraries and files
import os
import re
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PDFLoader
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


search_tool = SerperDevTool()

## Creating custom pdf reader tool

class BloodTestReportTool():
    @tool("Read Blood Test Report")
    def read_data_tool(self, path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path
        
        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.
        
        Returns:
            str: Full Blood Test report file
        """
        docs = PDFLoader(file_path=path).load()
        
        full_report = ""
        for data in docs:
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            
            full_report += content + "\n"
        
        return full_report

class NutritionTool:
    @tool("Analyze Nutrition from Blood Work")
    def analyze_nutrition_tool(self, blood_report_data: str) -> str:
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
        
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

class ExerciseTool: 
    @tool("Create Exercise Plan from Blood Work")
    def create_exercise_plan_tool(self, blood_report_data: str) -> str:
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"