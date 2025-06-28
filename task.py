from crewai import Task
from agents import doctor, verifier
from tools import search_tool, BloodTestReportTool

# Task Definitions for Blood Test Analysis - ALL BUGS FIXED

## BUG #1 FIXED: Professional Medical Analysis
help_patients = Task(
    description="""
    Analyze the provided blood test report with medical precision and professionalism.
    
    User Query: {query}
    
    Your responsibilities:
    1. Parse the blood test report data accurately using the BloodTestReportTool
    2. Identify any values outside normal reference ranges
    3. Provide evidence-based medical interpretation based on current medical standards
    4. Reference established medical guidelines (AMA, WHO, medical journals)
    5. Highlight potential health concerns that require medical attention
    6. Recommend appropriate follow-up actions with healthcare providers
    
    CRITICAL SAFETY REQUIREMENTS:
    - Only provide medically accurate information based on established science
    - Never fabricate data, diagnoses, or medical recommendations
    - Always include appropriate medical disclaimers
    - Emphasize the importance of professional medical consultation
    """,
    expected_output="""
    A comprehensive medical analysis report including:
    
    1. BLOOD TEST SUMMARY:
       - Overview of all tested parameters
       - Identification of values outside normal ranges
       - Clinical significance of abnormal findings
    
    2. MEDICAL INTERPRETATION:
       - Evidence-based analysis of results
       - Potential health implications
       - Risk factors to consider
    
    3. RECOMMENDATIONS:
       - Specific follow-up actions needed
       - Lifestyle modifications supported by evidence
       - When to seek immediate medical attention
    
    4. MEDICAL REFERENCES:
       - Citations to peer-reviewed medical literature
       - Links to established medical guidelines
       - Professional medical organizations' recommendations
    
    5. DISCLAIMERS:
       - Clear statement that this is not medical advice
       - Recommendation to consult healthcare professionals
       - Emergency contact information guidance
    
    Format: Professional medical report with proper medical terminology and citations
    """,
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool, search_tool],
    async_execution=False,
)

## BUG #2 FIXED: Evidence-Based Nutrition Analysis
nutrition_analysis = Task(
    description="""
    Provide evidence-based nutritional guidance based on blood test results and current nutritional science.
    
    User Query: {query}
    
    Nutritional Analysis Requirements:
    1. Review blood markers directly related to nutrition status:
       - Vitamin B12, Folate, Vitamin D levels
       - Iron studies (Ferritin, TIBC, Iron)
       - Lipid panel (Cholesterol, HDL, LDL, Triglycerides)
       - Blood glucose and HbA1c
       - Protein markers (Albumin, Total Protein)
       - Electrolytes (Sodium, Potassium, Magnesium)
    
    2. Identify nutritional deficiencies or excesses based on lab values
    3. Recommend specific foods to address identified nutritional gaps
    4. Suggest evidence-based supplementation ONLY when medically indicated
    5. Consider user's specific health context and dietary preferences from query
    6. Provide practical meal planning suggestions addressing nutritional needs
    7. Base ALL recommendations on peer-reviewed nutritional research
    
    EVIDENCE REQUIREMENTS:
    - Reference established nutritional guidelines (RDA, WHO, FDA)
    - Cite peer-reviewed nutritional studies
    - Use recommendations from registered dietitians and nutrition organizations
    """,
    expected_output="""
    Professional nutritional assessment including:
    
    1. NUTRITIONAL STATUS ANALYSIS:
       - Assessment of nutrition-related blood markers
       - Identification of deficiencies or excesses
       - Clinical significance of nutritional findings
    
    2. EVIDENCE-BASED DIETARY RECOMMENDATIONS:
       - Specific foods to address identified nutritional issues
       - Portion sizes and frequency recommendations
       - Foods to limit or avoid based on blood markers
    
    3. SUPPLEMENTATION GUIDANCE:
       - Evidence-based supplement recommendations (only when necessary)
       - Dosage recommendations based on blood levels
       - Duration and monitoring requirements
       - Potential interactions with medications
    
    4. MEAL PLANNING SUGGESTIONS:
       - Sample daily meal plans addressing nutritional needs
       - Shopping lists for recommended foods
       - Cooking methods to preserve nutritional value
    
    5. MONITORING AND FOLLOW-UP:
       - Timeline for nutritional status reassessment
       - Blood markers to monitor for improvement
       - Signs of nutritional status improvement
    
    6. SCIENTIFIC REFERENCES:
       - Citations to peer-reviewed nutritional studies
       - Links to established nutritional guidelines
       - Professional nutrition organization recommendations
    
    Format: Structured nutritional plan with scientific backing and practical implementation guidance
    """,
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool, search_tool],
    async_execution=False,
)

## BUG #3 FIXED: Safe Exercise Planning
exercise_planning = Task(
    description="""
    Develop a safe, medically-informed exercise plan based on blood test results, health status, and fitness level.
    
    User Query: {query}
    
    Exercise Planning Requirements:
    1. Review blood markers affecting exercise capacity and safety:
       - Hemoglobin and Hematocrit (oxygen carrying capacity)
       - Blood glucose levels (energy metabolism and diabetes management)
       - Cardiovascular markers (cholesterol, triglycerides)
       - Inflammatory markers (CRP, ESR if available)
       - Kidney function (Creatinine, BUN)
       - Liver function (ALT, AST)
       - Electrolyte balance (Sodium, Potassium)
    
    2. Assess current fitness level and health limitations from user query
    3. Design progressive, safe exercise recommendations appropriate for health status
    4. Include appropriate intensity guidelines based on medical findings
    5. Provide comprehensive safety considerations and contraindications
    6. Consider age, gender, and any medical conditions mentioned in query
    7. Base recommendations on exercise physiology and sports medicine research
    
    SAFETY REQUIREMENTS:
    - Prioritize safety and gradual progression over intensity
    - Include warning signs to stop exercise immediately
    - Provide modifications for health limitations identified in blood work
    - Recommend medical clearance when cardiovascular or metabolic concerns exist
    """,
    expected_output="""
    Comprehensive, medically-informed exercise plan including:
    
    1. EXERCISE READINESS ASSESSMENT:
       - Analysis of blood markers affecting exercise capacity
       - Identification of any exercise contraindications or limitations
       - Cardiovascular and metabolic readiness evaluation
       - Risk stratification for exercise participation
    
    2. PROGRESSIVE EXERCISE PROGRAM:
       - Phase 1: Foundation building (weeks 1-4) - Low intensity, form focus
       - Phase 2: Gradual progression (weeks 5-8) - Moderate intensity increase
       - Phase 3: Maintenance and advancement (weeks 9-12) - Sustained progress
       - Clear progression criteria and assessment points for each phase
    
    3. SPECIFIC ACTIVITY RECOMMENDATIONS:
       - Cardiovascular exercise (type, duration, intensity, frequency)
       - Strength training (exercises, sets, reps, progression guidelines)
       - Flexibility and mobility work (stretching, yoga, range of motion)
       - Recovery and rest day guidelines with active recovery options
    
    4. SAFETY PROTOCOLS:
       - Pre-exercise health screening checklist
       - Warning signs requiring immediate exercise cessation
       - Emergency contact procedures and action plans
       - When to seek medical attention during exercise program
    
    5. MODIFICATIONS FOR HEALTH CONDITIONS:
       - Exercise adaptations based on blood test findings
       - Alternative exercises for identified limitations
       - Intensity modifications for safety (heart rate zones, RPE scales)
       - Special considerations for metabolic or cardiovascular concerns
    
    6. MONITORING AND PROGRESSION:
       - Timeline for fitness and health reassessment
       - Blood markers to monitor during exercise program
       - Signs of positive adaptation vs. overtraining
       - Criteria for when to modify or advance the program
    
    7. PROFESSIONAL REFERENCES:
       - Citations to exercise physiology research
       - Sports medicine and cardiology guidelines
       - Professional fitness organization recommendations
       - Evidence-based exercise prescription principles
    
    Format: Progressive exercise prescription with comprehensive safety protocols and medical considerations
    """,
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool, search_tool],
    async_execution=False,
)

## BUG #4 FIXED: Proper Document Verification
verification = Task(
    description="""
    Thoroughly verify and validate the authenticity, completeness, and quality of the provided medical document.
    
    Document Verification Protocol:
    1. Document Format and Structure Analysis:
       - Confirm file format (PDF, CSV, JSON, Excel, etc.)
       - Validate document structure and layout consistency
       - Check for proper medical document formatting standards
       - Assess file integrity and readability
    
    2. Blood Test Report Validation:
       - Verify presence of required laboratory identification and accreditation
       - Confirm patient information fields (properly anonymized for privacy)
       - Validate test collection date and processing information
       - Check for proper reference ranges and units of measurement
       - Verify laboratory contact information and certification
    
    3. Required Blood Test Parameters Check:
       - Complete Blood Count (CBC) components if present
       - Basic Metabolic Panel (BMP) or Comprehensive Metabolic Panel (CMP)
       - Lipid panel components and cardiovascular markers
       - Additional specialized tests (thyroid, vitamins, hormones, etc.)
       - Liver and kidney function markers
    
    4. Data Quality Assessment:
       - Check for missing or incomplete test values
       - Validate numerical ranges are within biological possibility
       - Assess data consistency and formatting standards
       - Identify any corrupted, unreadable, or suspicious sections
       - Verify units of measurement are standard and consistent
    
    5. Laboratory Standards Compliance:
       - Verify reference ranges are from accredited laboratories
       - Check for proper unit measurements (mg/dL, mmol/L, etc.)
       - Validate test methodology information if available
       - Confirm quality control and calibration indicators
    
    VERIFICATION REQUIREMENTS:
    - Document must be a legitimate blood test report from accredited lab
    - All critical blood markers must be present and readable
    - Reference ranges must be provided for accurate interpretation
    - Document quality must be sufficient for reliable medical analysis
    - Any concerns about authenticity must be clearly flagged
    """,
    expected_output="""
    Comprehensive document verification report including:
    
    1. DOCUMENT AUTHENTICATION:
       - Document type confirmation: [BLOOD TEST REPORT: YES/NO]
       - File format and structure assessment: [Valid/Invalid]
       - Laboratory identification verified: [Present/Missing]
       - Overall document quality rating: [Excellent/Good/Fair/Poor/Invalid]
    
    2. REQUIRED PARAMETERS CHECKLIST:
       ✓ Complete Blood Count (CBC): [Present/Missing/Partial]
       ✓ Basic/Comprehensive Metabolic Panel: [Present/Missing/Partial]
       ✓ Lipid Panel: [Present/Missing/Partial]
       ✓ Liver Function Tests: [Present/Missing/Partial]
       ✓ Kidney Function Tests: [Present/Missing/Partial]
       ✓ Additional Specialized Tests: [List all additional parameters found]
    
    3. DATA QUALITY ASSESSMENT:
       - Missing values count and impact: [Specify which parameters and clinical significance]
       - Reference ranges provided: [Yes/No for each critical parameter]
       - Unit measurements consistent: [Yes/No with details]
       - Numerical values within biological range: [Yes/No with flagged outliers]
       - Data formatting and consistency: [Professional/Acceptable/Poor]
    
    4. LABORATORY INFORMATION VERIFICATION:
       - Laboratory name and accreditation: [Present/Missing/Verified]
       - Test collection date: [Present/Missing/Valid date range]
       - Test processing date: [Present/Missing/Reasonable timeframe]
       - Physician or ordering provider: [Present/Missing]
       - Laboratory contact and certification info: [Present/Missing]
    
    5. VERIFICATION DECISION:
       - Document suitable for medical analysis: [YES/NO/WITH LIMITATIONS]
       - Required actions before analysis: [List any corrections or clarifications needed]
       - Confidence level in document authenticity: [High/Medium/Low]
       - Analysis limitations due to document issues: [List specific limitations]
    
    6. RECOMMENDATIONS:
       - If document is incomplete: [Specific missing information needed for complete analysis]
       - If document is invalid: [Clear reasons for rejection and alternative requirements]
       - If document is valid: [Proceed to medical analysis with noted limitations]
       - Quality improvement suggestions: [How to obtain better documentation]
    
    Format: Structured verification checklist with clear pass/fail status and actionable recommendations
    """,
    agent=verifier,  # CRITICAL: Using verifier agent, not doctor!
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
)

