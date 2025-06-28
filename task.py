from crewai import Task
from agents import doctor, verifier
from tools import search_tool, BloodTestReportTool

# Task Definitions for Blood Test Analysis - ALL BUGS FIXED INCLUDING DEPENDENCIES

## BUG #5 FIX: Proper Task Dependencies and Workflow
# BEFORE: All tasks ran independently without context
# AFTER: Logical workflow where each task builds on previous analyses

## STEP 1: Document Verification (First - No dependencies)
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
    agent=verifier,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False,
    # NO CONTEXT - This is the first task in the workflow
)

## STEP 2: Medical Analysis (Depends on verification)
help_patients = Task(
    description="""
    Analyze the provided blood test report with medical precision and professionalism.
    
    User Query: {query}
    
    WORKFLOW CONTEXT: This analysis depends on successful document verification.
    Use the verification results to understand data quality and limitations.
    
    Your responsibilities:
    1. Parse the blood test report data accurately using the BloodTestReportTool
    2. Identify any values outside normal reference ranges
    3. Provide evidence-based medical interpretation based on current medical standards
    4. Reference established medical guidelines (AMA, WHO, medical journals)
    5. Highlight potential health concerns that require medical attention
    6. Recommend appropriate follow-up actions with healthcare providers
    7. Consider verification findings when assessing data reliability
    
    CRITICAL SAFETY REQUIREMENTS:
    - Only provide medically accurate information based on established science
    - Never fabricate data, diagnoses, or medical recommendations
    - Always include appropriate medical disclaimers
    - Emphasize the importance of professional medical consultation
    - Note any analysis limitations identified during verification
    """,
    expected_output="""
    A comprehensive medical analysis report including:
    
    1. BLOOD TEST SUMMARY:
       - Overview of all tested parameters
       - Identification of values outside normal ranges
       - Clinical significance of abnormal findings
       - Data quality assessment from verification results
    
    2. MEDICAL INTERPRETATION:
       - Evidence-based analysis of results
       - Potential health implications
       - Risk factors to consider
       - Confidence level based on data quality
    
    3. RECOMMENDATIONS:
       - Specific follow-up actions needed
       - Lifestyle modifications supported by evidence
       - When to seek immediate medical attention
       - Additional testing recommendations if data gaps exist
    
    4. MEDICAL REFERENCES:
       - Citations to peer-reviewed medical literature
       - Links to established medical guidelines
       - Professional medical organizations' recommendations
    
    5. DISCLAIMERS:
       - Clear statement that this is not medical advice
       - Recommendation to consult healthcare professionals
       - Emergency contact information guidance
       - Analysis limitations based on verification findings
    
    Format: Professional medical report with proper medical terminology and citations
    """,
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool, search_tool],
    async_execution=False,
    context=[verification],  # BUG #5 FIX: Depends on verification results
)

## STEP 3: Nutrition Analysis (Depends on verification and medical analysis)
nutrition_analysis = Task(
    description="""
    Provide evidence-based nutritional guidance based on blood test results and current nutritional science.
    
    User Query: {query}
    
    WORKFLOW CONTEXT: Build upon the medical analysis findings to provide targeted nutritional recommendations.
    Use medical interpretation results to prioritize nutritional interventions.
    
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
    8. Coordinate with medical findings to ensure nutritional safety
    
    EVIDENCE REQUIREMENTS:
    - Reference established nutritional guidelines (RDA, WHO, FDA)
    - Cite peer-reviewed nutritional studies
    - Use recommendations from registered dietitians and nutrition organizations
    - Ensure recommendations align with medical analysis findings
    """,
    expected_output="""
    Professional nutritional assessment including:
    
    1. NUTRITIONAL STATUS ANALYSIS:
       - Assessment of nutrition-related blood markers
       - Identification of deficiencies or excesses
       - Clinical significance of nutritional findings
       - Integration with medical analysis results
    
    2. EVIDENCE-BASED DIETARY RECOMMENDATIONS:
       - Specific foods to address identified nutritional issues
       - Portion sizes and frequency recommendations
       - Foods to limit or avoid based on blood markers
       - Coordination with medical recommendations
    
    3. SUPPLEMENTATION GUIDANCE:
       - Evidence-based supplement recommendations (only when necessary)
       - Dosage recommendations based on blood levels
       - Duration and monitoring requirements
       - Potential interactions with medications or health conditions
    
    4. MEAL PLANNING SUGGESTIONS:
       - Sample daily meal plans addressing nutritional needs
       - Shopping lists for recommended foods
       - Cooking methods to preserve nutritional value
       - Special considerations based on medical findings
    
    5. MONITORING AND FOLLOW-UP:
       - Timeline for nutritional status reassessment
       - Blood markers to monitor for improvement
       - Signs of nutritional status improvement
       - Coordination with medical follow-up schedule
    
    6. SCIENTIFIC REFERENCES:
       - Citations to peer-reviewed nutritional studies
       - Links to established nutritional guidelines
       - Professional nutrition organization recommendations
    
    Format: Structured nutritional plan with scientific backing and practical implementation guidance
    """,
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool, search_tool],
    async_execution=False,
    context=[verification, help_patients],  # BUG #5 FIX: Depends on verification AND medical analysis
)

## STEP 4: Exercise Planning (Depends on verification, medical analysis, and nutrition analysis)
exercise_planning = Task(
    description="""
    Develop a safe, medically-informed exercise plan based on blood test results, health status, and fitness level.
    
    User Query: {query}
    
    WORKFLOW CONTEXT: Integrate findings from medical and nutritional analyses to create a comprehensive,
    safe exercise plan that complements medical and nutritional recommendations.
    
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
    8. Coordinate with nutritional recommendations for optimal performance and recovery
    
    SAFETY REQUIREMENTS:
    - Prioritize safety and gradual progression over intensity
    - Include warning signs to stop exercise immediately
    - Provide modifications for health limitations identified in blood work
    - Recommend medical clearance when cardiovascular or metabolic concerns exist
    - Ensure exercise plan complements nutritional interventions
    """,
    expected_output="""
    Comprehensive, medically-informed exercise plan including:
    
    1. EXERCISE READINESS ASSESSMENT:
       - Analysis of blood markers affecting exercise capacity
       - Identification of any exercise contraindications or limitations
       - Cardiovascular and metabolic readiness evaluation
       - Risk stratification for exercise participation
       - Integration with medical and nutritional findings
    
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
       - Coordination with medical and nutritional monitoring
    
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
    context=[verification, help_patients, nutrition_analysis],  # BUG #5 FIX: Depends on ALL previous analyses
)

## BUG #5 FIX: Add Integrated Health Summary Task
integrated_health_summary = Task(
    description="""
    Create a comprehensive health summary integrating all analysis results into a cohesive, actionable plan.
    
    WORKFLOW CONTEXT: This is the final integration task that synthesizes findings from document verification,
    medical analysis, nutritional assessment, and exercise planning into a unified health strategy.
    
    Integration Requirements:
    1. Synthesize findings from medical, nutritional, and exercise analyses
    2. Identify interconnected health patterns and correlations across analyses
    3. Prioritize recommendations by medical importance and urgency
    4. Create actionable next steps for the patient with clear timelines
    5. Ensure all recommendations are mutually compatible and safe
    6. Provide clear timeline for implementation and follow-up
    7. Include monitoring parameters and success metrics
    8. Address any conflicts or contradictions between different analyses
    
    QUALITY ASSURANCE:
    - Verify all recommendations align with verification findings
    - Ensure medical safety takes priority over other considerations
    - Provide clear escalation paths for concerning findings
    - Include comprehensive disclaimers and safety information
    """,
    expected_output="""
    Integrated health summary including:
    
    1. EXECUTIVE SUMMARY:
       - Key findings across all analyses (medical, nutrition, exercise)
       - Priority health concerns requiring immediate attention
       - Overall health status assessment based on blood work
       - Data quality and analysis confidence levels
    
    2. PRIORITIZED ACTION PLAN:
       - Immediate actions (0-2 weeks) with specific steps
       - Short-term goals (2-8 weeks) with measurable outcomes
       - Long-term health objectives (2-6 months) with milestones
       - Emergency warning signs and immediate contact procedures
    
    3. COORDINATED RECOMMENDATIONS:
       - Medical follow-up requirements with timeline
       - Nutritional interventions with implementation schedule
       - Exercise program with progression markers
       - Monitoring schedule for blood work and health metrics
    
    4. INTEGRATION INSIGHTS:
       - How nutritional and exercise recommendations support medical goals
       - Potential synergies between different intervention strategies
       - Risk factors that appear across multiple analysis domains
       - Success metrics that span medical, nutritional, and fitness outcomes
    
    5. IMPLEMENTATION ROADMAP:
       - Week-by-week implementation guide for first month
       - Checkpoint dates for progress assessment
       - Modification triggers and adaptation strategies
       - Professional consultation schedule (doctors, nutritionists, trainers)
    
    6. SAFETY NET PROTOCOLS:
       - Warning signs requiring immediate medical attention
       - Emergency contact information and procedures
       - When to pause exercise or nutritional interventions
       - Escalation procedures for concerning developments
    
    Format: Executive-level health summary suitable for patient and healthcare provider coordination
    """,
    agent=doctor,
    tools=[search_tool],
    async_execution=False,
    context=[verification, help_patients, nutrition_analysis, exercise_planning],  # BUG #5 FIX: Depends on ALL analyses
)

## BUG #5 FIX: Define proper task execution sequence
TASK_SEQUENCE = [
    verification,              # Step 1: Verify document authenticity and quality
    help_patients,            # Step 2: Medical analysis (depends on verification)
    nutrition_analysis,       # Step 3: Nutrition recommendations (depends on medical analysis)
    exercise_planning,        # Step 4: Exercise planning (depends on medical and nutrition)
    integrated_health_summary # Step 5: Integrated summary (depends on all previous analyses)
]

## BUG #5 FIX: Task dependency validation function
def validate_task_dependencies():
    """
    Validate that task dependencies are properly configured for logical workflow
    """
    print("🔍 Validating task dependency structure...")
    
    # Verify task sequence order
    expected_sequence = [verification, help_patients, nutrition_analysis, exercise_planning, integrated_health_summary]
    
    for i, task in enumerate(TASK_SEQUENCE):
        print(f"  ✓ Task {i+1}: {task.description.split('.')[0][:50]}...")
        
        if i == 0:  # First task should have no dependencies
            if hasattr(task, 'context') and task.context:
                raise ValueError(f"First task {task} should not have dependencies")
        else:  # Subsequent tasks should have proper context
            if not hasattr(task, 'context') or not task.context:
                raise ValueError(f"Task {task} should have context dependencies")
            
            # Verify dependencies come before current task
            for dep_task in task.context:
                if dep_task not in TASK_SEQUENCE[:i]:
                    raise ValueError(f"Task {task} depends on {dep_task} which comes later in sequence")
    
    print("✅ Task dependency validation passed")
    print(f"✅ Workflow: verification → medical → nutrition → exercise → summary")
    return True

# Automatically validate dependencies when module is imported
try:
    validate_task_dependencies()
    print("🎯 Task workflow is properly configured!")
except Exception as e:
    print(f"❌ Task dependency error: {e}")
    raise