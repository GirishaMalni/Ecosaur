import streamlit as st
import base64

# Set page configuration globally (MUST be first)
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Path to the local image
image_path = "C:\\Users\\prithivi\\Desktop\\NASA\\background_image.jpeg"  # Change this to your image file path

# Function to convert image to base64
def get_base64_image(image_file):
    with open(image_file, "rb") as image:
        return base64.b64encode(image.read()).decode()

# Inject CSS with background image
page_bg_img = f'''
<style>

body {{
    background-image: url("data:image/jpeg;base64,{get_base64_image(image_path)}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 600px;
    width: 100%;
    opacity: 0.8; 
    
}}

.stApp {{
    font-color: rgba(255, 255, 255);
}}




    
</style>
'''

# Use markdown to inject the CSS code into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Define emission factors globally
EMISSION_FACTORS = {
    "India": {
        "Electricity": 0.82,  # kgCO2/kWh
        "LPG": 2.98,
        "Meat": 27.0,  # kgCO2/meal
        "Dairy": 13.6,
        "Veg": 2.0,
        "Waste": 0.1  # kgCO2/kg
    }
}

MODE = {
    "🚗Car": 0.14,
    "🚂Train": 0.06,
    "🚐Bus": 0.1,
    "✈️Air": 0.15,
    "🚴Cycle": 0.0,
    "🏍️Bike": 0.09
}

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Carbon Calculator", "SDG 1: No Poverty", "SDG 2: Zero Hunger", "SDG 3: Good Health",
        "SDG 4: Quality Education", "SDG 5: Gender Equality", "SDG 6: Clean Water and Sanitation",
        "SDG 7: Affordable and Clean Energy", "SDG 8: Decent Work", "SDG 9: Industry and Infrastructure",
        "SDG 10: Reduced Inequality", "SDG 11: Sustainable Cities", "SDG 12: Responsible Consumption",
        "SDG 13: Climate Action", "SDG 14: Life Below Water", "SDG 15: Life on Land",
        "SDG 16: Peace and Justice", "SDG 17: Partnerships"
    ]
)

# Define functions for each page

def carbon_calculator():
    st.title("Personal Carbon FootPrint Calculator App")

    # User inputs
    st.subheader("🌍 Your Country")
    country = st.selectbox("Select",["India","Russia","korea","USA","Nigeria","Africa","Japan","Malaysia"],index=0)
    

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Mode of Transport")
        mode = st.selectbox("Select", ["🚗Car", "🚂Train", "✈️Air", "🚐Bus", "🏍️Bike", "🚴Cycle"])

        st.subheader("🚗 Daily commute distance (in km)")
        distance = st.slider("Distance", 0.0, 2000.0, key="distance_input")

        st.subheader("💡Electricity consumption in a day (in kWh)")
        electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

        st.subheader("🍳Average Cooking Fuel usage per day (in kg)")
        lpg = st.slider("Cooking Gas", 0.0, 50.0, key="lpg_input")

    with col2:
        st.subheader("🍽️Meat Consumption (in kg)")
        meat = st.number_input("Meat", 0.0, key="meat_input")

        st.subheader("🥛Dairy consumption (in kg)")
        dairy = st.number_input("Dairy", 0.0, key="dairy_input")

        st.subheader("🥬Vegetables and Fruits consumption (in kg)")
        veg = st.number_input("Veggies", 0.0, key="veg_input")

        st.subheader("🗑️ Solid Waste generated per day (in kg)")
        waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

    # Calculate carbon emissions
    transportation_emissions = MODE[mode] * distance
    electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
    lpg_emissions = EMISSION_FACTORS[country]["LPG"] * lpg
    diet_emissions = EMISSION_FACTORS[country]["Dairy"] * dairy + EMISSION_FACTORS[country]["Meat"] * meat + EMISSION_FACTORS[country]["Veg"] * veg
    waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste

    # Convert emissions to tonnes and round off to 2 decimal points
    transportation_emissions = round(transportation_emissions / 1000, 2)
    electricity_emissions = round(electricity_emissions / 1000, 2)
    lpg_emissions = round(lpg_emissions / 1000, 2)
    diet_emissions = round(diet_emissions / 1000, 2)
    waste_emissions = round(waste_emissions / 1000, 2)

    # Calculate total emissions
    total_emissions = round(
        transportation_emissions + electricity_emissions + lpg_emissions + diet_emissions + waste_emissions, 2
    )

    if st.button("Calculate CO2 Emissions"):
        # Display results
        st.header("Results")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Carbon Emissions by Category")
            st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per day")
            st.info(f"💡 Energy Consumption: {electricity_emissions} tonnes CO2 per day")
            st.info(f"🍳 Cooking Fuel: {lpg_emissions} tonnes CO2 per day")
            st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per day")
            st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per day")

        with col4:
            st.subheader("Total Carbon Footprint")
            st.success(f"🌍 Your total carbon footprint per day is: {total_emissions} tonnes CO2 per day")
            st.warning("In 2021, CO2 emissions per capita for India was 1.9 tons of CO2 per capita.")

def sdg_page(sdg_title, why_it_matters, story_title, story_content):
    st.title(sdg_title)
    st.subheader("Why it matters for students:")
    st.write(why_it_matters)
    st.subheader(story_title)
    st.write(story_content)

# Page navigation logic
if page == "Carbon Calculator":
    carbon_calculator()


elif page == "SDG 1: No Poverty":
    sdg_page("SDG 1: No Poverty", 
             "Amara's Journey- Amara, a 10-year-old girl living in a small village in Kenya, dreams of becoming a teacher. However, her family struggles with poverty. She has to skip school often to help her mother collect water from a distant river and sell goods in the local market. Through the efforts of a local non-governmental organization (NGO), her village receives aid to build a nearby water pump and provide microloans to women. With the water pump, Amara’s mother spends less time fetching water and more time growing crops that they can sell. With the loan, Amara’s mother starts a small business, and Amara returns to school full-time. Over time, Amara excels in her studies and eventually becomes a teacher, lifting her family out of poverty. This story teaches students that providing resources and opportunities can help break the cycle of poverty.",
             "Objective: Understand the causes and solutions to poverty.",
             "Activity: Divide students into groups. Each group will research a different aspect of poverty (e.g., lack of access to clean water, education, healthcare). Each group will present a solution to their specific challenge. They can propose ideas such as microloans, clean water initiatives, or educational programs.")
# Add similar elif statements for other SDGs...




elif page == "SDG 2: Zero Hunger":
    sdg_page("SDG 2: Zero Hunger", 
             "The Community Garden: In a small urban neighborhood, a vacant lot has become a hub for crime and garbage dumping. Sarah, a local high school student, learns about community gardens and decides to propose an idea to her neighbors: turn the empty lot into a garden to grow fresh food. The neighborhood works together to clean up the lot, plant vegetables, and establish a system where everyone contributes and shares the produce. The garden not only provides healthy food but also creates a sense of community. People who once struggled with hunger now have regular access to fresh vegetables. This initiative helps decrease food insecurity in the area and builds a healthier, more connected community.",
             "Objective: Understand how local efforts can reduce hunger.",
             "Activity: Students will design their own community garden. They will research what crops can be grown in their local climate and calculate the amount of food needed to feed a family of four for a week. They will also design a plan for sharing the food within their community.")
# Add similar elif statements for other SDGs...

elif page == "SDG 3: Good Health":
    sdg_page("SDG 3: Good Health", 
             "The Wellness Club- Alex is a 16-year-old high school student who notices that many of his classmates are stressed and anxious due to school pressures. He decides to start a wellness club at his school, where students can come together to practice mindfulness, exercise, and talk about mental health. The club invites guest speakers, such as nutritionists and psychologists, and organizes events like yoga classes, healthy cooking demonstrations, and mental health awareness campaigns. Over time, students become more aware of how to take care of their physical and mental health. This story demonstrates the importance of good health and well-being for academic and personal success.",
             "Objective: Promote physical and mental health in students.",
             "Activity: Create a wellness program for the school. Students will work in groups to create different sections of the program: physical activity, mental health resources, and nutrition. They will research best practices and present a plan to the class.")
# Add similar elif statements for other SDGs...

elif page == "SDG 4: Quality Education":
    sdg_page("SDG 4: Quality Education", 
             "The School on Wheels-In rural India, many children cannot attend school because their villages are too remote. Rina, a dedicated teacher, decides to create a mobile school on a bus. The bus travels to different villages, bringing books, lessons, and supplies to children who otherwise wouldn’t have access to education. Over time, the mobile school becomes a lifeline for the children. They start learning how to read, write, and do math. Some of the children are even able to pass entrance exams for formal schools in nearby towns. The mobile school provides quality education to children who had been previously overlooked.",
             "Objective: Understand the barriers to education and explore innovative solutions..",
             "Activity: Students will research different countries where access to education is limited. In groups, they will brainstorm and present solutions (like the mobile school) that could be implemented in those areas. They will also create an action plan to support educational initiatives.")

elif page == "SDG 5: Gender Equality":
    sdg_page("SDG 5: Gender Equality", 
             "Amina's Fight for Equality-Amina, a young girl from Afghanistan, lives in a community where girls are not encouraged to go to school. However, Amina dreams of becoming a doctor. Despite the societal pressures, her family supports her education. When her father falls ill, Amina’s education allows her to understand the medical care he needs. Seeing the benefits of education firsthand, her community starts to change their views on educating girls. Amina goes on to become a role model for other girls in her village, proving that girls can achieve their dreams just as much as boys.",
             "Objective: Understand the importance of gender equality in education and society..",
             "Activity: Students will create a campaign for gender equality. They will research countries with high gender inequality and develop strategies for promoting gender equality in education and the workforce. Each group will present a campaign poster or video..")
elif page == "SDG 6: Clean Water and Sanitation":
    sdg_page("SDG 6: Clean Water and Sanitation", 
             "Clean Water for Tamani- Tamani lives in a small village in Tanzania where access to clean water is limited. Her family, like many others, relies on a river several miles away for drinking, cooking, and cleaning water. However, the water is often dirty, leading to frequent illnesses in the village. One day, an organization comes to the village to install a water purification system. With training from the organization, Tamani and other villagers learn how to maintain the system, ensuring a continuous supply of clean water. Over time, the community's health improves, and the children, including Tamani, spend more time in school rather than fetching water..",
             "Objective: Understand the importance of clean water and sanitation for public health.",
             "Activity: Students will conduct a water filtration experiment using household items (sand, gravel, charcoal, etc.). They will research water purification methods and compare how these techniques are used in different parts of the world..")  
elif page == "SDG 7: Affordable and Clean Energy":
    sdg_page("SDG 7: Affordable and Clean Energy", 
             "Solar Power for the Future- In a rural community in South Africa, electricity is unreliable, and families depend on expensive kerosene lamps for light at night. Ana, a 14-year-old student, struggles to do her homework in the evenings due to the poor lighting. One day, a social enterprise visits her village to install solar panels. The solar panels provide a clean and affordable energy source for lighting and cooking. Ana can now study in the evenings, and the village's reliance on kerosene is reduced, decreasing the health hazards and environmental damage. This story shows the transformative power of clean energy for education and well-being..",
             "Objective: Explore renewable energy solutions and their impact on communities..",
             "Activity: Students will design a model for a solar-powered device, such as a solar-powered lantern or water heater. They will research how solar energy works and present their models to the class, explaining the benefits of renewable energy..")   
elif page == "SDG 8: Decent Work":
    sdg_page("SDG 8: Decent Work", 
             "Fair Wages, Better Lives- Jorge, a coffee farmer in Colombia, works hard to support his family, but for years, his earnings have barely covered his living expenses. Then, a fair trade organization steps in and starts paying fair wages to farmers like Jorge. They also provide training on sustainable farming techniques. With the increased income and better working conditions, Jorge is able to send his children to school, invest in better farming tools, and improve his family’s quality of life. This story illustrates the importance of decent work and fair wages for promoting economic growth and reducing inequality..",
             "Objective: Understand the impact of fair wages and decent work on economic growth..",
             "Activity: Students will research different industries where fair wages are a concern (e.g., garment industry, agriculture) and create an infographic showing how fair wages benefit workers, their families, and their communities. They will also brainstorm ways to support fair trade in their everyday lives (e.g., buying fair trade products)...")   

elif page == "SDG 9: Industry and Infrastructure":
    sdg_page("SDG 9: Industry and Infrastructure", 
             "The Tech Hub That Changed a Town-In a small town in Nigeria, unemployment is high, and many young people struggle to find opportunities. Ada, a local engineer, decides to start a tech hub in the town. The hub offers free coding classes, internet access, and mentorship for young people interested in technology. Over time, many of the young people who train at the hub start their own businesses or secure jobs in the tech industry. The town transforms from a place with few prospects into a center of innovation and economic growth. This story demonstrates the power of innovation and infrastructure to transform communities..",
        
             "Objective: Explore the relationship between infrastructure, innovation, and economic development.",
             "Activity: Students will design a plan to bring a new form of infrastructure or technology to a community in need (e.g., building internet access, transportation systems, or clean energy sources). They will present how their solution can improve the community's economic prospects.")      

elif page == "SDG 10: Reduced Inequality":
    sdg_page("SDG 10: Reduced Inequality", 
             "Breaking Barriers- Maria, a young girl with a disability, lives in a city that lacks accessible infrastructure. She faces challenges getting to school, participating in sports, and even finding accessible public transportation. However, a local advocacy group starts a campaign to improve accessibility in the city. They work with city officials to install ramps, widen sidewalks, and improve public transportation for people with disabilities. Over time, Maria's life becomes easier, and she begins to participate more fully in school and community activities. This story illustrates how reducing inequalities can create a more inclusive society for all.",
             "Objective: Understand the importance of reducing social, economic, and political inequalities..",
             "Activity: Students will research accessibility challenges in their local community. They will create an action plan to address one specific inequality (e.g., physical access, gender inequality, income disparity) and present their ideas to the class..")   

elif page == "SDG 11: Sustainable Cities":
    sdg_page("SDG 11: Sustainable Cities", 
             "The Green City- Ethan lives in a large, bustling city known for its pollution and traffic congestion. Inspired by sustainable development principles, the city council launches a plan to transform the city into a “green city.” They build bike lanes, plant trees, encourage the use of public transportation, and create more green spaces. Over time, the city becomes more livable, with cleaner air and a better quality of life for residents. Ethan enjoys riding his bike to school, and his family spends weekends at the newly established parks. This story shows how cities can become more sustainable through thoughtful planning and community participation..",
             "Objective: Explore the characteristics of sustainable cities..",
             "Activity: Students will design their own “green city” by creating a blueprint that includes sustainable elements like public transportation, green spaces, and energy-efficient buildings. They will present their designs and explain how each element contributes to sustainability..")              

elif page == "SDG 12: Responsible Consumption":
    sdg_page("SDG 12: Responsible Consumption", 
             "The Waste-Free Classroom- Maya’s school is facing a problem: too much waste, especially plastic, and food waste from the cafeteria. Determined to make a change, Maya and her friends start a waste reduction project. They educate their classmates about recycling, reducing food waste, and the importance of responsible consumption. They set up compost bins, encourage students to bring reusable containers, and start a school garden where food scraps are used for composting. Over time, the school significantly reduces its waste, and the project becomes a model for other schools in the district. This story demonstrates how young people can drive responsible consumption and production..",
             "Objective: Understand the importance of reducing waste and promoting sustainable consumption..",
             "Activity: Students will conduct a waste audit of their school or household, identifying areas where waste can be reduced (e.g., plastics, food waste, paper). They will then create a plan to reduce waste in these areas and present their findings...")              

elif page == "SDG 13: Climate Action":
    sdg_page("SDG 13: Climate Action", 
             "The Youth Climate Warriors- Leo, a high school student from Brazil, has always been passionate about nature. But when devastating forest fires begin to ravage the Amazon rainforest, he realizes that climate change is threatening not just his beloved forest, but the entire planet. Leo organizes a group of young climate activists who start planting trees, lobbying local officials, and spreading awareness about climate change. Their efforts attract national attention, and they inspire other young people to take climate action. Leo’s group grows, and soon they are collaborating with environmental organizations to make a larger impact. This story shows the power of youth in combating climate change..",
             "Objective: Explore ways to combat climate change through community action..",
             "Activity: Students will research the impacts of climate change in different parts of the world. They will then design a local climate action campaign, outlining steps such as tree planting, reducing carbon footprints, or advocating for policy changes. Each group will present their campaign and explain its potential impact...")  

elif page == "SDG 14: Life Below Water":
    sdg_page("SDG 14: Life Below Water", 
             "Saving the Coral Reefs- Lina lives on a small island in the Philippines, where fishing and tourism are the main sources of income. Over the years, she has noticed that the coral reefs near her village are dying due to pollution, overfishing, and rising sea temperatures. Determined to protect the reefs, Lina starts a community conservation project. The project educates fishermen about sustainable fishing practices and organizes beach clean-ups to reduce plastic pollution. The community also sets up a marine protected area where fishing is restricted to allow the coral reefs to recover. Over time, the reefs begin to thrive again, attracting more fish and tourists, and improving the local economy..",
             "Objective: Understand the importance of protecting marine life and ecosystems..",
             "Activity: Students will research the causes of ocean pollution and its impact on marine life. They will create posters or presentations to raise awareness about protecting marine ecosystems and propose solutions such as reducing plastic use, supporting sustainable fisheries, and participating in clean-up initiatives...")        

elif page == "SDG 15: Life on Land":
    sdg_page("SDG 15: Life on Land", 
             "Restoring the Forest- Amar lives in a small village in India near a once-thriving forest that has been largely destroyed due to logging and agriculture. With wildlife disappearing and the soil degrading, the villagers’ livelihoods are at risk. Amar joins a local reforestation effort, where he and his friends plant trees, restore wildlife habitats, and learn sustainable farming practices. Over the years, the forest begins to grow back, and the soil becomes fertile again. The restored forest brings back animals, provides clean water, and even helps to cool the local climate. Amar’s efforts show how reforestation can revitalize both ecosystems and communities...",
             "Objective: Explore the importance of protecting and restoring terrestrial ecosystems..",
             "Activity: Students will design a reforestation project for their community or a hypothetical area. They will research the types of trees and plants that grow best in the region and create a step-by-step plan to restore a degraded landscape. Each group will present their reforestation plan and its expected environmental and social benefits..")      

elif page == "SDG 16: Peace and Justice":
    sdg_page("SDG 16: Peace and Justice", 
             "Building a Peaceful Community- In a war-torn region of the Middle East, Samira, a young girl, has seen how conflict has devastated her community. Many families have been displaced, and there is a deep distrust between different groups. Determined to promote peace, Samira and her friends start a youth peace club. The club organizes dialogues between different ethnic and religious groups, promotes human rights education, and advocates for local government transparency. Over time, the club's efforts lead to better communication and understanding among the community members, helping to foster a more peaceful and just society..",
             "Objective: Understand the importance of peace, justice, and strong institutions in creating stable societies..",
             "Activity: Students will role-play a community mediation session, where different groups come together to resolve a conflict (e.g., resource disputes, human rights violations). They will research peaceful conflict resolution strategies and apply them in their role-play. Each group will present their conflict resolution process and outcomes..")                 
elif page == "SDG 17: Partnerships":
    sdg_page("SDG 17: Partnerships", 
             "The Global Education Partnership- Ravi, a university student from India, participates in an international exchange program that brings students together to work on sustainable development projects. His group is tasked with addressing the lack of access to quality education in rural parts of Africa and Asia. The students partner with NGOs, governments, and local communities to create a mobile education platform that delivers lessons through smartphones and solar-powered tablets. By working together across borders, they are able to create an affordable and scalable solution that improves educational outcomes in multiple countries. This story highlights the power of global partnerships to achieve the SDGs..",
             "Objective: Understand the importance of global partnerships in achieving sustainable development goals." ,
             "Activity: Students will create a mock international partnership where they work with different countries (represented by groups of students) to solve a global problem (e.g., climate change, poverty, education). Each group will research their country’s resources and needs, and then collaborate to develop a partnership plan that benefits all participants..",
             )                                                                                           
