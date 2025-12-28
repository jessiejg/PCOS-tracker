import streamlit as st
import statistics
from datetime import datetime, timedelta

st.set_page_config(page_title="PCOS Detection Tool", page_icon="🩺")
st.title("🩺 Integrated PCOS Detection Tool")
st.markdown("### Medical Analysis based on BMI & Menstrual Cycles")

# Section 1: Physical Measurements
st.header("1. Physical Profile")
col_a, col_b = st.columns(2)
with col_a:
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
with col_b:
    height_cm = st.number_input("Height (cm)", min_value=0.0, step=0.1)

# Section 2: Cycle History (Calendar Input)
st.header("2. Menstrual Cycle History")
st.info("Please select the starting dates of your last 3 periods.")
date1 = st.date_input("Period 1 (Oldest)", value=datetime(2025, 9, 1))
date2 = st.date_input("Period 2", value=datetime(2025, 10, 15))
date3 = st.date_input("Period 3 (Most Recent)", value=datetime(2025, 12, 5))

if st.button("Run Diagnostic Analysis"):
    if weight > 0 and height_cm > 0:
        # --- CALCULATIONS ---
        bmi = weight / ((height_cm/100)**2)
        
        # Calculate individual cycle lengths
        c1 = (date2 - date1).days
        c2 = (date3 - date2).days
        cycle_lengths = [c1, c2]
        avg_cycle = sum(cycle_lengths) / 2
        variation = abs(c1 - c2)
        
        st.divider()
        st.subheader("📋 Diagnostic Report")

        # --- DETECTION LOGIC (BMI & CYCLE) ---
        pcos_risk_points = 0
        reasons = []

        # Check BMI Factor
        if bmi >= 25.0:
            pcos_risk_points += 1
            reasons.append(f"High BMI ({bmi:.2f}) which is linked to insulin resistance.")
        
        # Check Cycle Length Factor (Oligomenorrhea)
        if avg_cycle > 35:
            pcos_risk_points += 1
            reasons.append(f"Infrequent periods (Average cycle is {avg_cycle:.1f} days).")
            
        # Check Irregularity Factor
        if variation > 7:
            pcos_risk_points += 1
            reasons.append(f"High cycle variation ({variation} days difference).")

        # --- OUTPUT DISPLAY ---
        if pcos_risk_points >= 2:
            st.error("### Result: High Probability of PCOS Symptoms")
            st.write("**Based on our analysis, you have multiple risk factors:**")
            for reason in reasons:
                st.write(f"- {reason}")
            
            st.warning("⚠️ **Medical Advice:** Your data shows a pattern often seen in PCOS. Please schedule an appointment with a gynecologist for a professional diagnosis (Ultrasound & Blood Test).")
        
        elif pcos_risk_points == 1:
            st.warning("### Result: Moderate Risk / Observation Needed")
            st.write(f"- Note: {reasons[0]}")
            st.info("While you have one risk factor, your overall pattern is borderline. Monitor your symptoms closely.")
        
        else:
            st.success("### Result: Low Probability")
            st.write("Your BMI and menstrual cycles appear to be within the healthy/regular range.")

        # Prediction Window (Always PCOS-style if risk is detected)
        st.write("---")
        next_date = date3 + timedelta(days=avg_cycle)
        if pcos_risk_points >= 1:
            st.info(f"📅 **Prediction Window:** Due to irregularities, your next period is estimated between **{next_date - timedelta(days=3)} and {next_date + timedelta(days=3)}**.")
        else:
            st.success(f"📅 **Exact Prediction:** Your next period is expected on **{next_date.strftime('%d %B %Y')}**.")

    else:
        st.error("Please ensure all physical measurements are entered correctly.")

st.divider()
st.caption("Project by: Nichaphat Theodthai, Jessie Josephine Gunawan, Sai Yasaswi Gangula, & Kopparthi Roshni")