import streamlit as st
from rdflib import Graph, Namespace, RDF, RDFS

# --- PAGE CONFIG ---
st.set_page_config(page_title="Hypertension Expert System", page_icon="🩺", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        font-size: 20px;
    }

    html, body, [class*="css"]  {
        font-size: 20px;
    }

    h1 {
        font-size: 42px !important;
    }
    h2 {
        font-size: 32px !important;
    }
    h3 {
        font-size: 26px !important;
    }

    .stCheckbox label {
        font-size: 20px !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        font-size: 20px;
        background-color: #ff4b4b;
        color: white;
    }

    section[data-testid="stSidebar"] {
        width: 420px !important;
        min-width: 420px !important;
    }

    section[data-testid="stSidebar"] * {
        font-size: 20px !important;
    }

    .report-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE KNOWLEDGE BASE ---
EX = Namespace('http://medical.org/hypertension/')
P = Namespace('http://medical.org/patient/')

@st.cache_resource
def get_graph():
    g = Graph()
    g.bind('ex', EX)
    g.bind('rdfs', RDFS)
    g.add((EX.EmergencySymptom, RDFS.subClassOf, EX.Symptom))
    g.add((EX.RiskFactor, RDFS.subClassOf, EX.PatientProfile))
    
    # Symptoms
    g.add((EX.chest_pain, RDF.type, EX.EmergencySymptom))
    g.add((EX.blurred_vision, RDF.type, EX.EmergencySymptom))
    g.add((EX.confusion, RDF.type, EX.EmergencySymptom))
    g.add((EX.shortness_of_breath, RDF.type, EX.EmergencySymptom))
    
    # Risk Factors
    g.add((EX.pregnancy, RDF.type, EX.RiskFactor))
    g.add((EX.heart_disease_history, RDF.type, EX.RiskFactor))
    g.add((EX.smoker, RDF.type, EX.RiskFactor))
    
    return g

g = get_graph()

def run_inference(patient_uri):
    inferred_triples = []
    fired_rules = []

    # 15 RULES
    if (patient_uri, EX.hasCondition, EX.high_bp) in g:
        inferred_triples.append((patient_uri, EX.status, EX.ElevatedStatus))
        fired_rules.append("Rule 1: High BP detected.")

    if (patient_uri, EX.hasCondition, EX.crisis_bp) in g:
        inferred_triples.append((patient_uri, EX.status, EX.CrisisStatus))
        fired_rules.append("Rule 2: Crisis BP detected.")

    for s, p, o in g.triples((None, RDF.type, EX.EmergencySymptom)):
        if (patient_uri, EX.hasCondition, o) in g and (patient_uri, EX.status, EX.CrisisStatus) in inferred_triples:
            inferred_triples.append((patient_uri, EX.urgency, EX.EmergencyReferral))
            fired_rules.append(f"Rule 3: Crisis BP + {o.split('/')[-1]} -> Emergency Referral.")
            break

    if (patient_uri, EX.status, EX.CrisisStatus) in inferred_triples and (patient_uri, EX.urgency, EX.EmergencyReferral) not in inferred_triples:
        inferred_triples.append((patient_uri, EX.urgency, EX.UrgentReview))
        fired_rules.append("Rule 4: Crisis BP -> Hypertensive Urgency.")

    if (patient_uri, EX.status, EX.ElevatedStatus) in inferred_triples and (patient_uri, EX.hasCondition, EX.pregnancy) in g:
        inferred_triples.append((patient_uri, EX.urgency, EX.UrgentReview))
        fired_rules.append("Rule 5: High BP + Pregnancy -> Preeclampsia Risk.")

    if (patient_uri, EX.status, EX.ElevatedStatus) in inferred_triples and (patient_uri, EX.hasCondition, EX.heart_disease_history) in g:
        inferred_triples.append((patient_uri, EX.urgency, EX.UrgentReview))
        fired_rules.append("Rule 6: High BP + Heart History -> Urgent Review.")

    if (patient_uri, EX.status, EX.ElevatedStatus) in inferred_triples and (patient_uri, EX.hasCondition, EX.headache) in g:
        inferred_triples.append((patient_uri, EX.urgency, EX.UrgentReview))
        fired_rules.append("Rule 7: High BP + Severe Headache -> Potential Urgency.")

    if (patient_uri, EX.status, EX.ElevatedStatus) not in inferred_triples and (patient_uri, EX.hasCondition, EX.headache) in g:
        inferred_triples.append((patient_uri, EX.urgency, EX.RoutineCheck))
        fired_rules.append("Rule 8: Symptoms with Normal BP -> Clinic Review.")

    if (patient_uri, EX.hasCondition, EX.smoker) in g and (patient_uri, EX.hasCondition, EX.obesity) in g:
        inferred_triples.append((patient_uri, EX.profile, EX.HighRiskLifestyle))
        fired_rules.append("Rule 9: Combined Lifestyle Risks detected.")

    if (patient_uri, EX.hasCondition, EX.age_over_65) in g and (patient_uri, EX.status, EX.ElevatedStatus) in inferred_triples:
        inferred_triples.append((patient_uri, EX.urgency, EX.UrgentReview))
        fired_rules.append("Rule 10: Elderly patient (>65) with high BP.")

    if (patient_uri, EX.urgency, EX.EmergencyReferral) in inferred_triples or (patient_uri, EX.status, EX.CrisisStatus) in inferred_triples:
        inferred_triples.append((patient_uri, EX.suspicion, EX.Probable))
        fired_rules.append("Rule 11: High severity -> Suspicion: PROBABLE.")

    if (patient_uri, EX.status, EX.ElevatedStatus) in inferred_triples and (patient_uri, EX.suspicion, EX.Probable) not in inferred_triples:
        inferred_triples.append((patient_uri, EX.suspicion, EX.Possible))
        fired_rules.append("Rule 12: Elevated BP -> Suspicion: POSSIBLE.")

    if (patient_uri, EX.status, EX.ElevatedStatus) not in inferred_triples and (patient_uri, EX.profile, EX.HighRiskLifestyle) not in inferred_triples:
        inferred_triples.append((patient_uri, EX.suspicion, EX.Unlikely))
        fired_rules.append("Rule 13: Normal status -> Suspicion: UNLIKELY.")

    if (patient_uri, EX.urgency, EX.EmergencyReferral) in inferred_triples:
        inferred_triples.append((patient_uri, RDF.type, EX.HypertensiveEmergency))
        fired_rules.append("Rule 14: Confirmed Hypertensive Emergency.")

    if (patient_uri, EX.hasCondition, EX.diabetes) in g and (patient_uri, EX.status, EX.ElevatedStatus) in inferred_triples:
        inferred_triples.append((patient_uri, EX.advice, EX.DiabetesWarning))
        fired_rules.append("Rule 15: High BP + Diabetes -> Increased Risk Warning.")

    for t in inferred_triples: g.add(t)
    return fired_rules

# --- UI LAYOUT ---
st.title("🩺 Medical Expert System: Hypertension")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Clinical Questionnaire")
    st.info("Please fill out the patient's symptoms and history below.")
    
    questions = {
        "1": "🩸 Is your Blood Pressure high (>140/90)?", 
        "2": "⚠️ Is your BP reading in a crisis range (>180/120)?",
        "3": "🤕 Do you have a severe headache?", 
        "4": "😵 Are you feeling dizzy?", 
        "5": "👁️ Are you experiencing blurred vision?", 
        "6": "💔 Do you have chest pain?", 
        "7": "🫁 Do you have shortness of breath?", 
        "8": "🧠 Are you feeling confused?",
        "9": "🩸 Do you have a nosebleed?", 
        "10": "🤰 Are you pregnant?", 
        "11": "🏥 History of heart disease?", 
        "12": "🚬 Do you smoke?", 
        "13": "⚖️ Obesity (BMI > 30)?", 
        "14": "👴 Age over 65?",
        "15": "🧂 High salt intake?", 
        "16": "🍬 Do you have Diabetes?", 
        "17": "🛋️ Sedentary lifestyle?", 
        "18": "🍺 Regular alcohol use?"
    }
    
    responses = {}
    q_items = list(questions.items())
    
    # Split questions into two sub-columns
    sq1, sq2 = st.columns(2)
    for i, (k, q) in enumerate(q_items):
        with sq1 if i < 9 else sq2:
            responses[k] = st.checkbox(q, key=k)

    if st.button("🚀 Analyze Condition"):
        patient_uri = P.Streamlit_Patient
        g.remove((patient_uri, None, None))
        
        fact_mapping = {
            "1": EX.high_bp,
            "2": EX.crisis_bp,
            "3": EX.headache,
            "4": EX.dizziness,
            "5": EX.blurred_vision,
            "6": EX.chest_pain,
            "7": EX.shortness_of_breath,
            "8": EX.confusion,
            "9": EX.nosebleed,
            "10": EX.pregnancy,
            "11": EX.heart_disease_history,
            "12": EX.smoker,
            "13": EX.obesity,
            "14": EX.age_over_65,
            "15": EX.high_salt_intake,
            "16": EX.diabetes,
            "17": EX.sedentary_lifestyle,
            "18": EX.alcohol_consumption
       }
        
        for k, v in responses.items():
            if v: g.add((patient_uri, EX.hasCondition, fact_mapping[k]))
        
        rules_fired = run_inference(patient_uri)
        
        # Get results
        susp = "UNLIKELY ⚪"
        if (patient_uri, EX.suspicion, EX.Probable) in g: susp = "PROBABLE 🔴"
        elif (patient_uri, EX.suspicion, EX.Possible) in g: susp = "POSSIBLE 🟡"
        
        urg = "ROUTINE ✅"
        color = "green"
        if (patient_uri, EX.urgency, EX.EmergencyReferral) in g: 
            urg = "EMERGENCY REFERRAL 🚨"
            color = "red"
        elif (patient_uri, EX.urgency, EX.UrgentReview) in g: 
            urg = "URGENT REVIEW ⚠️"
            color = "orange"
        elif (patient_uri, EX.urgency, EX.RoutineCheck) in g: 
            urg = "CLINIC REVIEW 🩺"
            color = "blue"

        with col2:
            st.header("📊 Diagnostic Results")
            st.subheader(f"Suspicion: {susp}")
            st.subheader(f"Urgency: :{color}[{urg}]")
            
            st.markdown("### 💡 Recommendation")
            if "EMERGENCY" in urg:
                st.error("SEEK EMERGENCY MEDICAL CARE IMMEDIATELY! 🚑")
            elif "URGENT" in urg:
                st.warning("Contact your doctor within 24 hours. 📞")
            else:
                st.success("Maintain a healthy lifestyle and monitor BP. ✅")

            st.markdown("---")
            st.markdown("### 🔍 Explanation Facility")
            for i, r in enumerate(rules_fired):
                st.write(f"{i+1}. {r}")

with st.sidebar:
    st.image(r"C:\Users\moham\Desktop\knowledge base\Project\image.png")
    st.title("About")
    st.info("This is a Knowledge-Based Expert System for Hypertension assessment.")
    st.markdown("""
    **Project Specs:**
    - 18 Named Facts ✅
    - 15 Inference Rules ✅
    - Explanation Facility ✅
    """)

# +++++++++++++++++++