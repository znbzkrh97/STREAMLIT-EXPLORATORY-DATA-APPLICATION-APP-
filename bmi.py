import streamlit as st
import pandas as pd
import altair as alt
 
st.set_page_config(page_title="BMI Calculator",layout="centered" )

st.title(" 😋 BMI Calculator")
st.write("Let's calculate your **Body mass Index [BMI]** and understand what it means")

st.header(" 🫡 Enter your details")

height = st.number_input("Enter your height (in cm)", min_value=50,max_value=250,value=170)
weight = st.number_input("Enter your weight (in kg)", min_value=10,max_value=200,value=65)

st.write('Your Height 😶‍🌫️ :', height, "cm") 
st.write('Your weight 🤔 :', weight, "kg") 

if st.button("Calculate BMI"):
    h_m = height/100 # convert cm to m
    bmi = weight / (h_m**2) 
    st.success(f"YOUR BMI IS **{bmi:.2f}**")

    # BMI Categories
    if bmi < 18.5:
        category = "Underweight 🥵😵‍💫"
        color = "#D1290C"
    
    elif 18.5 <= bmi < 25:
        category = "Normal 😮‍💨🫦"
        color = "#00FF00"

    else:
        category = "Obesity 🙀👀"
        color = "#FF0000"
    
    st.markdown(
        f"""
        <div style='background-color:{color};padding:15px;border-radius:10px;text-align:center'>
        <h3>Your BMI Category : {category}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.header("📊 BMI Range Chart")
 
# Data
bmi_data = pd.DataFrame({
    "Category": ["Underweight", "Normal", "Overweight", "Obese"],
    "Range": [18.5, 24.9, 29.9, 40]
})
 
# Define custom colors for each category
color_scale = alt.Scale(
    domain=["Underweight", "Normal", "Overweight", "Obese"],
    range=["#B6A34D", "#81C784", "#FFD54F", "#E57373"]
)
 
# Create chart
chart = (
    alt.Chart(bmi_data)
    .mark_bar()
    .encode(
        x=alt.X("Category:N", title="BMI Category"),
        y=alt.Y("Range:Q", title="BMI Range"),
        color=alt.Color("Category:N", scale=color_scale, legend=None)
    )
    .properties(width=600, height=400)
)
 
st.altair_chart(chart, use_container_width=True)