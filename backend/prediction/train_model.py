import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression


data = pd.DataFrame(
{
"humidity":[
30,35,40,45,50,
55,60,65,70,75,80
],

"temperature":[
39,38,37,36,35,
34,33,32,31,30,29
]
}
)

X = data[["humidity"]]

y = data["temperature"]

model = LinearRegression()

model.fit(X,y)

joblib.dump(
model,
"models/weather/weather_model.pkl"
)

print(
"UrbanMind model retrained"
)