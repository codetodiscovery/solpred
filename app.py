import streamlit as st
import base64
import pandas as pd
from getting_inputs import predict_smiles, predict_csv

def home():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        .navbar {
            background-color: #3d405b; 
            color: white; 
            padding: 10px;
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("# Home")
    st.markdown("This is the working WebApp for predicting the solubility (ESOL) of organic compounds. The random forest model employed in this app is trained on few descriptors the details of which can be found in the paper which can be found on the about page.")
    st.write("Also check out the GitHub repo [link](https://github.com/codetodiscovery/Predict-Solubilities) and Youtube [link](https://www.youtube.com/channel/UC6k1epfxt3gPVdQhE8gI1tQ)")
    st.markdown("<div class='navbar'>Need Support: Contact <a href='mailto:codetodiscovery@gmail.com'>codetodiscovery@gmail.com</a></div>", unsafe_allow_html=True)

def about():
    st.markdown("# About")
    st.markdown("SOlPred: An Artificial Intelligence Based WebApp for Predicting the Solubility (ESOL) of Organic Molecules")
    with open('Solubility_Report.pdf',"rb") as f:
      base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    st.markdown(pdf_display, unsafe_allow_html=True)
    st.markdown("# Thank You!")

def predict():

    st.markdown('## Predict Solubility for a Single SMILES String')
    st.markdown('#### Instructions: Generate SMILES strings for the molecule for which you want to predict the solubility using following website:')
    st.write("Cheminfo [link](https://www.cheminfo.org/flavor/malaria/Utilities/SMILES_generator___checker/index.html)")
    smiles = st.text_input('Enter SMILES:')
    if st.button('Predict'):
        try:
            prediction = predict_smiles(smiles)
            st.write(f"The Solubility (ESOL) prediction for {smiles} is {prediction.round(3)}")
        except:
            st.write("Not Valid SMILES. Check About for Instructions.")

def predict_file():
    st.markdown('## Predict Solubility for Multiple SMILES Strings')
    st.markdown('#### Instructions: Generate SMILES strings for the molecules using following website and append in a single column without any header in a csv file:')
    st.write("Cheminfo [link](https://www.cheminfo.org/flavor/malaria/Utilities/SMILES_generator___checker/index.html)")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            csv = pd.read_csv(uploaded_file, header=None)
            prediction = predict_csv(csv)
            st.write(prediction)
        except:
            st.write("Error processing file.")

def main():
    st.title('SOLPred')
    page = st.sidebar.selectbox("Choose a page", ["Home", "About", "Predict", "Predict File"])
    
    if page == "Home":
        home()
    
    elif page == "About":
        about()

    elif page == "Predict":
        predict()

    elif page == "Predict File":
        predict_file()

if __name__ == '__main__':
    main()
