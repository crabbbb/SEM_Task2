import streamlit as st
import pandas as pd
from web_scraping import WebScrap
from buildTree import Tree

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

def extractLeafPaths(root):
    paths = []
    # traverse all nodes under the root
    for node in root.descendants:  
        if node.is_leaf:  # check leaf node
            # get full path 
            path = [ancestor.name for ancestor in node.path] 
            paths.append(path)
    return paths

def getDataFrame(root) :
    leaf_paths = extractLeafPaths(root)

    # find the maximum depth of the paths to leaf nodes
    max_depth = max(len(path) for path in leaf_paths)

    # columnsName = ["Current", "Diploma / Foundation"]
    df = pd.DataFrame(leaf_paths, columns=[f"Level {i+1}" for i in range(max_depth)])

    return df 

def getTree(edLevel, qLevel, ws, edqLevel, domain) : 
    tree = Tree(edLevel, qLevel, ws, edqLevel, domain)
    tree.setChild(edLevel, tree.root)

    return tree.root


def main() :
    ws = WebScrap(filePath='/mount/src/sem_task2/QualificationRoadMap/JsonLibrary/repo.json')

    ws.scrapAll()
    domain = None
    edLevel = None
    edqLevel = None

    # Title 
    st.title("Qualification Roadmap For :rainbow[TAR UMT] :cherry_blossom:")

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

    df = ""

    # create a button - this button name "Get Roadmap"
    if st.button("Get Roadmap"):
        df = getDataFrame(getTree(edLevel, qLevel, ws, edqLevel, domain))

        uniqueStart = df['Level 2'].unique()
        for uni in uniqueStart :
            st.header(f"Next Level Start From {uni}", divider="rainbow")
            newdf = df[df['Level 2']==uni]
            st.table(newdf)
        # st.table(df)


if __name__=='__main__':
    main()