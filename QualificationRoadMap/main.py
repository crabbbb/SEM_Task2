import streamlit as st
import pandas as pd

currentEducationLevel = [
    'SPM',
    'STPM',
    'FOUNDATION',
    'DIPLOMA',
    'BACHELOR DEGREE',
    'MASTER'
]

qualificationProvide = [
    'FOUNDATION',
    'DIPLOMA',
    'BACHELOR DEGREE',
    'MASTER',
    'PHD'
]

def changeQualification(edLevel) :
    index = qualificationProvide.index(edLevel)
    return qualificationProvide[index:]

def main() :
    # Title 
    st.title("Credit Approval Prediction")

    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Credict Approval App </h2>
    </div>
    """

    edLevel = st.selectbox(
        "Choose your current Highest Academic Qualification Level : ",
        currentEducationLevel,
    )

    qLevel = st.selectbox(
        "Choose an Academic Qualification you wish to achieve : ",
        changeQualification(edLevel),
    )

    # # create a button - this button name "Predict"
    # if st.button("Predict"):
    #     result = predict(response=response) # when click will run this function 
    result = ""
    st.success('The output is {}'.format(result)) 


if __name__=='__main__':
    main()