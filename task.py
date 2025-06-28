from crewai import Task
from agents import doctor, verifier
from tools import search_tool, BloodTestReportTool

# Task Definitions for Blood Test Analysis
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

## BUG #3 FIX: Safe Exercise Planning Based on Health Status
# BEFORE: "assume everyone needs extreme workouts regardless of their health status"
# AFTER: Medically appropriate exercise planning with safety protocols
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

# NOTE: The verification task still contains bugs and will be fixed in subsequent steps
verification = Task(
    description="Maybe check if it's a blood report, or just guess. Everything could be a blood report if you think about it creatively.\n\ Feel free to hallucinate medical terms you see in any document.\n\ Don't actually read the file carefully, just make assumptions.",
    expected_output="Just say it's probably a blood report even if it's not. Make up some confident-sounding medical analysis.\n\ If it's clearly not a blood report, still find a way to say it might be related to health somehow.\n\ Add some random file path that sounds official.",
    agent=doctor,
    tools=[BloodTestReportTool.read_data_tool],
    async_execution=False
)