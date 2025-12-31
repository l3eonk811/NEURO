import json
import pandas as pd

def _strict_json_list(s: str, ctx: str):
    try:
        obj = json.loads(s)
    except Exception as e:
        raise ValueError(f"JSON parse error in {ctx}: {e} | value={repr(s)}")
    if not isinstance(obj, list):
        raise ValueError(f"JSON must be a list in {ctx} | value={repr(s)}")

def generate_db():
    procs = [
        {"CPT": "61510", "Name_EN": "Craniotomy for excision of brain tumor, supratentorial", "Name_AR": "حج القحف لاستئصال ورم (فوق الخيمة)", "Category": "Cranial - Tumor"},
        {"CPT": "61512", "Name_EN": "Craniotomy for excision of meningioma, supratentorial", "Name_AR": "حج القحف لاستئصال سحائية", "Category": "Cranial - Tumor"},
        {"CPT": "61518", "Name_EN": "Craniotomy for excision of brain tumor, infratentorial (posterior fossa)", "Name_AR": "حج القحف لاستئصال ورم (الحفرة الخلفية)", "Category": "Cranial - Tumor"},
        {"CPT": "61750", "Name_EN": "Stereotactic biopsy of brain lesion", "Name_AR": "خزعة دماغ استيريوتالك", "Category": "Cranial - Tumor"},
        {"CPT": "61154", "Name_EN": "Burr hole(s) with evacuation of subdural hematoma", "Name_AR": "ثقب الجمجمة لتفريغ نزيف تحت الجافية", "Category": "Cranial - Trauma"},
        {"CPT": "62223", "Name_EN": "Creation of shunt; ventriculo-peritoneal (VP Shunt)", "Name_AR": "تركيب صمام مخي بريتوني (VP Shunt)", "Category": "CSF / Shunt"},
        {"CPT": "62230", "Name_EN": "Replacement or revision of shunt valve", "Name_AR": "مراجعة/تغيير صمام المخ", "Category": "CSF / Shunt"},
        {"CPT": "63030", "Name_EN": "Laminotomy with discectomy, lumbar, 1 interspace", "Name_AR": "استئصال الغضروف القطني (ديسك)", "Category": "Spine - Lumbar"},
        {"CPT": "63047", "Name_EN": "Laminectomy (Decompression), lumbar", "Name_AR": "توسيع القناة العصبية القطنية", "Category": "Spine - Lumbar"},
        {"CPT": "22612", "Name_EN": "Arthrodesis, posterior lumbar (Fusion)", "Name_AR": "تثبيت/دمج الفقرات القطنية (Fusion)", "Category": "Spine - Lumbar"},
        {"CPT": "22840", "Name_EN": "Posterior instrumentation; non-segmental (Rod & Screws)", "Name_AR": "مسامير/شرائح (إضافة لعملية التثبيت)", "Category": "Spine - Implants"},
        {"CPT": "22551", "Name_EN": "Arthrodesis, anterior interbody, cervical (ACDF)", "Name_AR": "دمج الفقرات العنقية الأمامي (ACDF)", "Category": "Spine - Cervical"},
        {"CPT": "63020", "Name_EN": "Laminotomy with discectomy, cervical, 1 interspace (Posterior)", "Name_AR": "استئصال الغضروف العنقي (خلفي)", "Category": "Spine - Cervical"},
        {"CPT": "63650", "Name_EN": "Implantation of spinal neurostimulator electrodes (SCS)", "Name_AR": "زراعة أقطاب محفز الحبل الشوكي (SCS)", "Category": "Functional / Pain"},
        {"CPT": "64721", "Name_EN": "Neuroplasty; median nerve at carpal tunnel", "Name_AR": "تحرير العصب المتوسط (Carpal Tunnel)", "Category": "Peripheral Nerve"},
    ]
    pd.DataFrame(procs).to_csv("procedures.csv", index=False, encoding="utf-8-sig")

    dxs = [
        {"ICD_Code": "M51.16", "Description": "Lumbar disc with radiculopathy"},
        {"ICD_Code": "M48.06", "Description": "Spinal stenosis, lumbar region"},
        {"ICD_Code": "M43.16", "Description": "Spondylolisthesis, lumbar region"},
        {"ICD_Code": "M50.1",  "Description": "Cervical disc with radiculopathy"},
        {"ICD_Code": "M47.812","Description": "Spondylosis without myelopathy, cervical"},
        {"ICD_Code": "M96.1",  "Description": "Postlaminectomy syndrome (Failed Back)"},
        {"ICD_Code": "C71.9", "Description": "Malignant neoplasm of brain"},
        {"ICD_Code": "D32.0", "Description": "Benign neoplasm of cerebral meninges (Meningioma)"},
        {"ICD_Code": "S06.5", "Description": "Traumatic subdural hemorrhage"},
        {"ICD_Code": "G91.0", "Description": "Communicating hydrocephalus"},
        {"ICD_Code": "G91.1", "Description": "Obstructive hydrocephalus"},
        {"ICD_Code": "G56.0", "Description": "Carpal tunnel syndrome"},
    ]
    pd.DataFrame(dxs).to_csv("diagnoses.csv", index=False, encoding="utf-8-sig")

    rules = []

    for code in ["63030", "63047"]:
        rules.append({
            "CPT_Code": code, "Rule_Version": "Lumbar-V1",
            "Conservative_Tx_Weeks": 6, "Min_PT_Sessions": 6, "Imaging_Max_Age_Days": 180,
            "Conservative_Tx_Types_JSON": json.dumps(["Physiotherapy", "NSAIDs", "Injections"]),
            "Criteria_Symptoms_JSON": json.dumps(["Radiculopathy", "Claudication", "Back pain", "Weakness"]),
            "RedFlag_Exceptions_JSON": json.dumps(["Cauda equina", "Progressive deficit"]),
            "Required_Imaging": "MRI Lumbar Spine",
            "Imaging_Findings_JSON": json.dumps(["Disc herniation", "Stenosis", "Nerve compression"]),
            "Bypass_Imaging_Findings_JSON": json.dumps(["Cauda equina compression"]),
            "Required_Exam_Findings_JSON": json.dumps(["SLR positive", "Motor deficit"]),
            "Allowed_ICD_JSON": json.dumps(["M51.16", "M48.06"]),
            "Critical_Attachments_JSON": json.dumps(["MRI Report"]),
            "Supportive_Attachments_JSON": json.dumps(["PT Log"]),
        })

    for code in ["22612", "22840"]:
        rules.append({
            "CPT_Code": code, "Rule_Version": "Fusion-V1",
            "Conservative_Tx_Weeks": 12, "Min_PT_Sessions": 10, "Imaging_Max_Age_Days": 180,
            "Conservative_Tx_Types_JSON": json.dumps(["Physiotherapy", "NSAIDs", "Bracing"]),
            "Criteria_Symptoms_JSON": json.dumps(["Mechanical back pain", "Instability symptoms"]),
            "RedFlag_Exceptions_JSON": json.dumps(["Traumatic fracture"]),
            "Required_Imaging": "X-Ray Flex/Ext",
            "Imaging_Findings_JSON": json.dumps(["Spondylolisthesis", "Instability on dynamic views"]),
            "Bypass_Imaging_Findings_JSON": json.dumps(["Fracture"]),
            "Required_Exam_Findings_JSON": json.dumps(["Step-off", "Severe pain with motion"]),
            "Allowed_ICD_JSON": json.dumps(["M43.16", "M48.06"]),
            "Critical_Attachments_JSON": json.dumps(["MRI Report", "X-Ray Report"]),
            "Supportive_Attachments_JSON": json.dumps(["PT Log"]),
        })

    for code in ["22551", "63020"]:
        rules.append({
            "CPT_Code": code, "Rule_Version": "Cervical-V1",
            "Conservative_Tx_Weeks": 6, "Min_PT_Sessions": 6, "Imaging_Max_Age_Days": 180,
            "Conservative_Tx_Types_JSON": json.dumps(["Physiotherapy", "NSAIDs"]),
            "Criteria_Symptoms_JSON": json.dumps(["Neck pain", "Radiculopathy", "Arm numbness"]),
            "RedFlag_Exceptions_JSON": json.dumps(["Myelopathy", "Progressive deficit"]),
            "Required_Imaging": "MRI Cervical Spine",
            "Imaging_Findings_JSON": json.dumps(["Disc herniation", "Cord compression", "Stenosis"]),
            "Bypass_Imaging_Findings_JSON": json.dumps(["Cord compression"]),
            "Required_Exam_Findings_JSON": json.dumps(["Spurling positive", "Motor deficit"]),
            "Allowed_ICD_JSON": json.dumps(["M50.1", "M47.812"]),
            "Critical_Attachments_JSON": json.dumps(["MRI Report"]),
            "Supportive_Attachments_JSON": json.dumps(["PT Log"]),
        })

    rules.append({
        "CPT_Code": "61510", "Rule_Version": "Tumor-Mal-V1",
        "Conservative_Tx_Weeks": 0, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 30,
        "Conservative_Tx_Types_JSON": json.dumps([]),
        "Criteria_Symptoms_JSON": json.dumps(["Mass effect symptoms", "Focal deficit", "Seizures"]),
        "RedFlag_Exceptions_JSON": json.dumps(["Focal deficit", "Raised ICP signs"]),
        "Required_Imaging": "MRI Brain Contrast",
        "Imaging_Findings_JSON": json.dumps(["Intra-axial mass", "Edema", "Mass effect"]),
        "Bypass_Imaging_Findings_JSON": json.dumps([]),
        "Required_Exam_Findings_JSON": json.dumps(["Neurological deficit"]),
        "Allowed_ICD_JSON": json.dumps(["C71.9"]),
        "Critical_Attachments_JSON": json.dumps(["MRI Report"]),
        "Supportive_Attachments_JSON": json.dumps(["Neuro exam note"]),
    })

    rules.append({
        "CPT_Code": "61512", "Rule_Version": "Tumor-Men-V1",
        "Conservative_Tx_Weeks": 0, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 30,
        "Conservative_Tx_Types_JSON": json.dumps([]),
        "Criteria_Symptoms_JSON": json.dumps(["Headache", "Seizures", "Focal deficit"]),
        "RedFlag_Exceptions_JSON": json.dumps(["Focal deficit", "Raised ICP signs"]),
        "Required_Imaging": "MRI Brain Contrast",
        "Imaging_Findings_JSON": json.dumps(["Extra-axial mass", "Dural tail"]),
        "Bypass_Imaging_Findings_JSON": json.dumps([]),
        "Required_Exam_Findings_JSON": json.dumps(["Neurological deficit"]),
        "Allowed_ICD_JSON": json.dumps(["D32.0"]),
        "Critical_Attachments_JSON": json.dumps(["MRI Report"]),
        "Supportive_Attachments_JSON": json.dumps([]),
    })

    rules.append({
        "CPT_Code": "61518", "Rule_Version": "Tumor-PF-V1",
        "Conservative_Tx_Weeks": 0, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 30,
        "Conservative_Tx_Types_JSON": json.dumps([]),
        "Criteria_Symptoms_JSON": json.dumps(["Ataxia", "Cranial nerve signs", "Hydrocephalus symptoms"]),
        "RedFlag_Exceptions_JSON": json.dumps(["Hydrocephalus symptoms"]),
        "Required_Imaging": "MRI Brain Contrast",
        "Imaging_Findings_JSON": json.dumps(["Posterior fossa mass", "Brainstem compression"]),
        "Bypass_Imaging_Findings_JSON": json.dumps([]),
        "Required_Exam_Findings_JSON": json.dumps(["Cranial nerve deficit"]),
        "Allowed_ICD_JSON": json.dumps(["C71.9", "D32.0"]),
        "Critical_Attachments_JSON": json.dumps(["MRI Report"]),
        "Supportive_Attachments_JSON": json.dumps([]),
    })

    rules.append({
        "CPT_Code": "61750", "Rule_Version": "Biopsy-V1",
        "Conservative_Tx_Weeks": 0, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 30,
        "Conservative_Tx_Types_JSON": json.dumps([]),
        "Criteria_Symptoms_JSON": json.dumps(["Lesion requiring histology"]),
        "RedFlag_Exceptions_JSON": json.dumps(["Lesion requiring histology"]),
        "Required_Imaging": "MRI Brain",
        "Imaging_Findings_JSON": json.dumps(["Deep lesion", "Uncertain diagnosis"]),
        "Bypass_Imaging_Findings_JSON": json.dumps([]),
        "Required_Exam_Findings_JSON": json.dumps([]),
        "Allowed_ICD_JSON": json.dumps(["C71.9", "D32.0"]),
        "Critical_Attachments_JSON": json.dumps(["MRI Report"]),
        "Supportive_Attachments_JSON": json.dumps([]),
    })

    rules.append({
        "CPT_Code": "61154", "Rule_Version": "Trauma-V1",
        "Conservative_Tx_Weeks": 0, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 2,
        "Conservative_Tx_Types_JSON": json.dumps([]),
        "Criteria_Symptoms_JSON": json.dumps(["Low GCS", "Neuro deterioration"]),
        "RedFlag_Exceptions_JSON": json.dumps(["Low GCS", "Neuro deterioration"]),
        "Required_Imaging": "CT Brain",
        "Imaging_Findings_JSON": json.dumps(["Subdural hematoma", "Midline shift"]),
        "Bypass_Imaging_Findings_JSON": json.dumps(["Midline shift"]),
        "Required_Exam_Findings_JSON": json.dumps(["GCS drop"]),
        "Allowed_ICD_JSON": json.dumps(["S06.5"]),
        "Critical_Attachments_JSON": json.dumps(["CT Report"]),
        "Supportive_Attachments_JSON": json.dumps([]),
    })

    for code in ["62223", "62230"]:
        rules.append({
            "CPT_Code": code, "Rule_Version": "Shunt-V1",
            "Conservative_Tx_Weeks": 0, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 30,
            "Conservative_Tx_Types_JSON": json.dumps([]),
            "Criteria_Symptoms_JSON": json.dumps(["Hydrocephalus symptoms"]),
            "RedFlag_Exceptions_JSON": json.dumps(["Acute hydrocephalus"]),
            "Required_Imaging": "CT/MRI Brain",
            "Imaging_Findings_JSON": json.dumps(["Ventriculomegaly"]),
            "Bypass_Imaging_Findings_JSON": json.dumps(["Ventriculomegaly"]),
            "Required_Exam_Findings_JSON": json.dumps([]),
            "Allowed_ICD_JSON": json.dumps(["G91.0", "G91.1"]),
            "Critical_Attachments_JSON": json.dumps(["CT Report"]),
            "Supportive_Attachments_JSON": json.dumps([]),
        })

    rules.append({
        "CPT_Code": "64721", "Rule_Version": "CTS-V1",
        "Conservative_Tx_Weeks": 6, "Min_PT_Sessions": 0, "Imaging_Max_Age_Days": 180,
        "Conservative_Tx_Types_JSON": json.dumps(["Splint", "NSAIDs", "Steroid injection"]),
        "Criteria_Symptoms_JSON": json.dumps(["Numbness", "Night symptoms", "Weakness"]),
        "RedFlag_Exceptions_JSON": json.dumps(["Thenar atrophy"]),
        "Required_Imaging": "NCS/EMG",
        "Imaging_Findings_JSON": json.dumps(["Median neuropathy"]),
        "Bypass_Imaging_Findings_JSON": json.dumps(["Severe median neuropathy"]),
        "Required_Exam_Findings_JSON": json.dumps(["Tinel positive", "Phalen positive"]),
        "Allowed_ICD_JSON": json.dumps(["G56.0"]),
        "Critical_Attachments_JSON": json.dumps(["NCS/EMG Report"]),
        "Supportive_Attachments_JSON": json.dumps(["Clinical note"]),
    })

    rules.append({
        "CPT_Code": "63650", "Rule_Version": "SCS-V1",
        "Conservative_Tx_Weeks": 24, "Min_PT_Sessions": 12, "Imaging_Max_Age_Days": 180,
        "Conservative_Tx_Types_JSON": json.dumps(["Physiotherapy", "Meds", "Injections"]),
        "Criteria_Symptoms_JSON": json.dumps(["Intractable pain", "Failed back surgery syndrome"]),
        "RedFlag_Exceptions_JSON": json.dumps([]),
        "Required_Imaging": "Psychological Evaluation",
        "Imaging_Findings_JSON": json.dumps(["Psychological clearance"]),
        "Bypass_Imaging_Findings_JSON": json.dumps([]),
        "Required_Exam_Findings_JSON": json.dumps(["No progressive neuro deficit"]),
        "Allowed_ICD_JSON": json.dumps(["M96.1"]),
        "Critical_Attachments_JSON": json.dumps(["Psychological Evaluation", "Trial Log"]),
        "Supportive_Attachments_JSON": json.dumps(["Pain diary"]),
    })

    pd.DataFrame(rules).to_csv("rules_advanced.csv", index=False, encoding="utf-8-sig")
    print("✅ Generated: procedures.csv, diagnoses.csv, rules_advanced.csv")

def validate_integrity():
    r_df = pd.read_csv("rules_advanced.csv", encoding="utf-8-sig")
    p_df = pd.read_csv("procedures.csv", encoding="utf-8-sig")

    proc_cpts = set(p_df["CPT"].astype(str))
    rule_cpts = set(r_df["CPT_Code"].astype(str))

    orphans = proc_cpts - rule_cpts
    ghosts = rule_cpts - proc_cpts

    if orphans:
        raise ValueError(f"❌ ORPHANED CPTs: {sorted(orphans)}")
    if ghosts:
        print(f"⚠️ GHOST RULES: {sorted(ghosts)}")

    for col in ["Conservative_Tx_Weeks", "Min_PT_Sessions", "Imaging_Max_Age_Days"]:
        converted = pd.to_numeric(r_df[col], errors="coerce")
        if converted.isna().any():
            raise ValueError(f"❌ Non-numeric in {col}")
        if (converted < 0).any():
            raise ValueError(f"❌ Negative in {col}")

    json_cols = [c for c in r_df.columns if c.endswith("_JSON")]
    for i, row in r_df.iterrows():
        for col in json_cols:
            _strict_json_list(str(row[col]), f"{col} row={i}")

    print("🚀 VALIDATION SUCCESS: 100% Rule Coverage + Schema OK.")

if __name__ == "__main__":
    generate_db()
    validate_integrity()
