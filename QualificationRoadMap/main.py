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
    clist = q.course # array
    rlist = []
    for c in clist : 
        courseList[c.name] = c.label
        rlist.append(c.name)
    return rlist

def callTree() :


def main() :
    ws = WebScrap(filePath='/mount/src/sem_task2/QualificationRoadMap/JsonLibrary/repo.json')

    ws.scrapAll()
    domain = ""
    edLevel = ""
    edqLevel = ""

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
                getCourseList(edLevel, ws),
            )

            domain = courseList[edqLevel]

            st.write(f":rainbow[Your course is in {domain} area]")

    qLevel = st.selectbox(
        "Choose an Academic Qualification you wish to achieve : ",
        changeQualification(edLevel),
    )

    # create a button - this button name "Get Roadmap"
    # if st.button("Get Roadmap"):
        
    # df = ""
    # st.success('The output is {}'.format(result)) 


if __name__=='__main__':
    main()