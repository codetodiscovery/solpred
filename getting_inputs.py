#files importing
import pickle
import pandas as pd
import numpy as np
import warnings


import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem

import mordred
from mordred import Calculator, descriptors
warnings.filterwarnings("ignore")

##### Loading important files

model = pickle.load(open('resources/model_rf', 'rb'))
scaler = pickle.load(open('resources/scaler.pkl', 'rb'))

# function to predict from a single smiles string
def predict_smiles(smiles):

    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    df_mol = pd.DataFrame(data = [mol], columns=(['mol']), dtype='object')
    calc = Calculator(descriptors, ignore_3D=True)
    desc = calc.pandas(df_mol['mol'])
    desc_8 = desc[['FilterItLogS', 'Lipinski', 'SIC0', 'RNCG', 'RPCG', 'ATS0Z',
            'PEOE_VSA6', 'AATS0i']]
    X_test = scaler.transform(desc_8)
    result = model.predict(X_test)
    return result[0]

# function to predict from a csv file
def predict_csv(csv):
    df = pd.DataFrame(csv)
    result = []
    for j in range(len(df)):
        smiles = df.iloc[j, 0]
        prediction = predict_smiles(smiles)
        result.append(prediction.round(3))
    df[1]=result
    return df
