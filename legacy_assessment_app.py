
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Legacy Assessment from CMDB", layout="wide")

st.title("🧠 Automated Legacy System Assessment")
st.markdown("Upload your **CMDB Export CSV**, and get auto-scored legacy risk results per application.")

uploaded_file = st.file_uploader("Upload CMDB CSV", type=["csv"])

def derive_legacy_assessment(row):
    questions = []

    # Q1
    questions.append("Yes" if row["Programming Language"] in ["COBOL", "FORTRAN", "VB6"] else "No")
    # Q2
    questions.append("Yes" if row["Hosting Platform"] in ["AS/400", "Mainframe", "Solaris"] else "No")
    # Q3
    questions.append("Yes" if row["Integration Count"] > 5 else "No")
    # Q4
    questions.append("Yes" if row["Performance Incidents"] > 3 else "No")
    # Q5
    questions.append("Yes" if row["API Coverage (%)"] < 50 else "No")
    # Q6
    questions.append("Yes" if row["Months Since Last Change"] > 18 else "No")
    # Q7
    questions.append("No" if row["Engineer Assigned"] else "Yes")
    # Q8
    questions.append("Yes" if row["Documentation Status"] in ["Missing", "Outdated"] else "No")
    # Q9
    questions.append("Yes" if row["Known Workarounds"] else "No")
    # Q10
    questions.append("Yes" if row["Months Since Last Change"] > 24 and not row["Engineer Assigned"] else "No")
    # Q11
    questions.append("Yes" if row["Strategic Relevance"] in ["Low", "None"] else "No")
    # Q12
    questions.append("Yes" if row["Innovation Blockers"] else "No")
    # Q13
    questions.append("Yes" if row["Annual Maintenance Cost"] > 70000 else "No")
    # Q14
    questions.append("Yes" if row["Compliance Findings"] else "No")
    # Q15
    questions.append("Yes" if row["Support Status"] in ["End-of-life", "Obsolete"] else "No")

    return questions

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    output = []

    for _, row in df.iterrows():
        answers = derive_legacy_assessment(row)
        score = sum(1 for ans in answers if ans == "Yes")
        risk = "High Risk" if score >= 10 else "Moderate Risk" if score >= 5 else "Low Risk"
        output.append([row["Application Name"], row["Application Version"]] + answers + [score, risk])

    headers = ["Application Name", "Application Version"] + [f"Q{i+1}" for i in range(15)] + ["Total Score", "Risk Category"]
    result_df = pd.DataFrame(output, columns=headers)

    st.success("✅ Assessment complete.")
    st.dataframe(result_df, use_container_width=True)

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="Legacy_Assessment_Result.csv", mime="text/csv")
