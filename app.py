from fastapi import FastAPI, File, Query, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, PlainTextResponse
import uvicorn
import joblib
from pydantic import BaseModel
import pandas as pd
from sklearn import preprocessing, linear_model
import numpy as np
from typing import Dict

app = FastAPI(
    title="Détection de faux billets API",
    description="""API utilisant une régression logistique afin de prédire si un
    billet est vrai ou faux grâce à ses dimensions.""",
    version="1.0.0", debug=True)
    
model = joblib.load('modele.pkl')
scaler = joblib.load('scaler.pkl')

@app.get("/", response_class=PlainTextResponse)
async def running():
  note = """
API de Détection de faux billets.
Note: ajouter "/docs" à l'URL pour obtenir les documents de l'interface utilisateur Swagger.
  """
  return note
   
class monoDetection(BaseModel):
    diagonal:float
    height_left:float
    height_right:float	
    margin_low:float	
    margin_up:float	
    length:float

@app.post('/predict')
def predict(data : monoDetection):
                                                                                                                                                                                                                                
    features = np.array([[data.diagonal, data.height_left, data.height_right, data.margin_low, data.margin_up, data.length]])
    features = scaler.transform(features)
    predictions = model.predict_proba(features)[:,1]>=0.62
    if predictions == 1:
        return "Vrai billet"
    elif predictions == 0:
        return "Faux billet"


class multiDetection(BaseModel):
    diagonal:Dict[str, float]
    height_left:Dict[str, float]
    height_right:Dict[str, float]	
    margin_low:Dict[str, float]	
    margin_up:Dict[str, float]	
    length:Dict[str, float]
    ide:Dict[str, str]

@app.post('/multipredict')
def multipredict(data : multiDetection):
    features = pd.DataFrame({"diagonal":data.diagonal,
              "height_left":data.height_left,
              "height_right":data.height_right,
              "margin_low":data.margin_low,
              "margin_up":data.margin_up,
              "length":data.length}).to_numpy()
    features = scaler.transform(features)
    predictions = model.predict_proba(features)[:,1]
    return pd.DataFrame(predictions, index=data.ide.values()).to_dict()
    
