import streamlit as st
import json

with open('/mount/src/sem_task2_recommendationsystem/RecommendationSystem/CareerProspects.json') as file:
    data = json.load(file)


count = {
    'Diploma in Computer Science': 0,
    'Diploma in Information Technology': 0,
    'Diploma in Software Engineering': 0,
    'Bachelor of Science (Honours) in Management Mathematics with Computing': 0,
    'Bachelor of Information Systems (Honours) in Enterprise Information Systems': 0,
    'Bachelor of Computer Science (Honours) in Interactive Software Technology': 0,
    'Bachelor of Information Technology (Honours) in Information Security': 0,
    'Bachelor of Computer Science (Honours) in Data Science': 0,
    'Bachelor of Information Technology (Honours) in Software Systems Development': 0,
    'Bachelor of Software Engineering (Honours)': 0,
    'Master of Computer Science': 0,
    'Master of Information Technology': 0,
    'Master of Science in Mathematical Sciences': 0,
    'Doctor of Philosophy in Computer Science': 0,
    'Doctor of Philosophy in Information Technology': 0,
    'Doctor of Philosophy in Mathematical Sciences': 0
}


def recommend_course(level=None, career=[]):
    recommendations = []

    for course in data[level]:
        for careerOption in course['career']:
            for chosenCareer in career:
                if(careerOption == chosenCareer):
                    if(course not in recommendations):
                        recommendations.append(course)
                        count[course['course']] = 1
                    else:
                        count[course['course']] = count[course['course']] + 1
    
    return recommendations


def main():
    nl = '\n'
    recommendations = []
    top_recommendations = []

    st.title("Course Recommendation")

    level = st.selectbox(
        "Choose your desired education level",
        ["Diploma", "Bachelor Degree", "Master Degree", "PhD"],
        index = None,
    )

    # st.write("You selected: ", level)


    if(level == 'Diploma'):
        career = st.multiselect(
            "What are your career prospects (max choose 3)",
            [
                "Database Administrator",
                "IT Executive",
                "IT Support Executive",
                "Mobile Application Developer",
                "Network Support Officer",
                "Programmer",
                "Software Developer",
                "Software Engineer",
                "Software Tester",
                "System Analyst",
                "Web Developer"
            ],
            max_selections = 3
        )
    elif(level == 'Bachelor Degree'):
        career = st.multiselect(
            "What are your career prospects (max choose 3)",
            [
                "Asset/Liability Manager",
                "Business Analyst",
                "Business Intelligence Specialist",
                "Business Process Consultant",
                "Computer Science Researcher",
                "Credit Risk Manager",
                "Data Analyst",
                "Data Engineer",
                "Data Modelling Engineer",
                "Data Scientist",
                "Data Warehouse Developer",
                "Database Administrator",
                "ERP Consultant",
                "Financial Analyst",
                "Financial Planners and Advisor",
                "Forensics Analyst",
                "Forensics Investigator",
                "Games Designer",
                "Games Producer",
                "Games Programmer",
                "Games Software Engineer",
                "Games Tester",
                "Information Security Administrator",
                "Information Security Analyst",
                "Information Security Auditor",
                "Information Security Consultant",
                "Information Security Engineer",
                "Information Security Manager",
                "Investment Analyst",
                "IoT Developer",
                "IT Consultant",
                "IT Manager",
                "Machine Learning Engineer",
                "Management Consultant",
                "Market Risk Manager",
                "Mobile Application Developer",
                "Multimedia Developer",
                "Network Engineer",
                "Network Security Engineer",
                "Officers in Financial Institutions",
                "Pricing Analyst",
                "Programmer",
                "Project Manager",
                "Quality Manager",
                "Quantitative Analyst",
                "Reserach Officer",
                "Security Software Developer",
                "Software Architect",
                "Software Developer",
                "Software Engineer",
                "Software Quality Assurance Engineer",
                "Software Tester",
                "System Analyst",
                "Technical Lead",
                "Web Designer",
                "Web Developer"
            ],
            max_selections = 3
        )
    elif(level == 'Master Degree'):
        career = st.multiselect(
            "What are your career prospects (max choose 3)",
            [
                "Academician",
                "Business Analysis Consultant",
                "Business Analyst",
                "Business Development Executive",
                "Consultant",
                "Data Analyst",
                "Data Scientist",
                "Data Security Consultant",
                "Insurance underwriter",
                "IT Consultant",
                "IT Strategist",
                "Machine Learning Engineer",
                "Market Analyst",
                "Mobile Application Developer",
                "Network Security Consultant",
                "Operations Research Analyst",
                "Product Development Executive",
                "Product Planner",
                "Programmer",
                "Project Consultant",
                "Project Leader",
                "Quality Data Analyst",
                "Quantitative Analyst",
                "R&D Analyst",
                "Researcher",
                "Software Analyst",
                "Software Designer",
                "Software Developer",
                "Software Engineer",
                "Software Research Engineer",
                "Solution Architect",
                "Technical Lead"
            ],
            max_selections = 3
        )
    else:
        career = st.multiselect(
            "What are your career prospects (max choose 3)",
            [
                "Business Consultant",
                "Lead Researcher",
                "Project Manager",
                "Research Scientist (Maths)",
                "Senior Academician",
                "Senior Big Data Analyst",
                "Senior Business Analyst",
                "Senior Business Development Executive",
                "Senior Data Engineer",
                "Senior Data Scientist",
                "Senior Data Security Consultant",
                "Senior IT Consultant",
                "Senior IT Strategist",
                "Senior Machine Learning Engineer",
                "Senior Market Analyst",
                "Senior Mobile Application Developer",
                "Senior Network Security Consultant",
                "Senior Product Development Executive",
                "Senior Product Planner",
                "Senior Programmer",
                "Senior Software Developer",
                "Talent Director"
            ],
            max_selections = 3
        )

    # st.write("You selected: ", career)


    if st.button("View Recommendation"):
        recommendations = recommend_course(level=level, career=career)
        top_recommendations = dict(sorted(count.items(), key = lambda item:item[1], reverse = True)[:3])
        st.success("Recommended Course:")
    

    for top in top_recommendations:
        for r in recommendations:
            if(r['course'] == top):
                st.success(f"{r['course']}{nl}{nl}For more information, visit {r['link']}{nl}{nl}{count[r['course']]} career(s) matched")


if __name__ == '__main__':
    main()
