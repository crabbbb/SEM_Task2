import streamlit as st
import pandas as pd
from web_scraping import WebScrap

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

courseList = {}

def changeQualification(edLevel) :
    index = 0
    if edLevel != "SPM" and edLevel != "STPM" :
        index = qualificationProvide.index(edLevel) + 1
    return qualificationProvide[index:]

def getCourseList(edLevel, ws : WebScrap) : 
    q = ws.qualificationList[edLevel]
    clist = q.course
    rlist = []
    for key in clist : 
        courseList[key] = clist[key]
        rlist.append(clist[key])
    return rlist

def main() :
    ws = WebScrap(filePath='JsonLibrary/repo.json')

    ws.scrapAll()

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

    if edLevel != "SPM" and edLevel != "STPM" :
        studyAttarumt = st.checkbox(f"Do you study {edLevel} at TAR UMT? (If Yes please click the box)")

        if studyAttarumt :
            edqLevel = st.selectbox(
                "Choose your Course : ",
                getCourseList(edLevel),
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