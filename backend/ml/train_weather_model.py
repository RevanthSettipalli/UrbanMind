import pandas as pd
import joblib
import json

from pathlib import Path

from sklearn.model_selection import (
    train_test_split
)

from sklearn.ensemble import (
    RandomForestRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)


# =====================================
# PATH
# =====================================

ROOT = Path(
    __file__
).resolve().parents[2]

DATA = (

ROOT
/
"data"
/
"weather_history.csv"

)

MODEL = (

ROOT
/
"models"
/
"weather"

)

MODEL.mkdir(
parents=True,
exist_ok=True
)


# =====================================
# LOAD
# =====================================

print(
"\nLoading dataset..."
)

df = pd.read_csv(
DATA,
on_bad_lines="skip"
)

print(
f"Records: {len(df)}"
)


# =====================================
# CLEAN
# =====================================

required = [

"time",
"temperature",
"humidity"

]

for c in required:

    if c not in df:

        raise Exception(
            f"Missing {c}"
        )


df["time"] = pd.to_datetime(
df["time"],
errors="coerce"
)

df["temperature"] = pd.to_numeric(
df["temperature"],
errors="coerce"
)

df["humidity"] = pd.to_numeric(
df["humidity"],
errors="coerce"
)

df = df.dropna()


# =====================================
# FEATURES
# =====================================

df["hour"] = (
df["time"]
.dt.hour
)

df["day"] = (
df["time"]
.dt.day
)

df["month"] = (
df["time"]
.dt.month
)

df["temp_ma"] = (

df[
"temperature"
]

.rolling(
5
)

.mean()

)

df=df.dropna()


# =====================================
# TRAIN
# =====================================

X = df[[

"humidity",

"hour",

"day",

"month",

"temp_ma"

]]

y = df[
"temperature"
]


X_train,X_test,y_train,y_test = (

train_test_split(

X,

y,

test_size=.2,

random_state=42

)

)


# =====================================
# MODEL
# =====================================

print(
"\nTraining..."
)

model = (

RandomForestRegressor(

n_estimators=300,

max_depth=15,

random_state=42

)

)

model.fit(
X_train,
y_train
)


# =====================================
# SCORE
# =====================================

pred = model.predict(
X_test
)

mae = round(

mean_absolute_error(

y_test,

pred

),

3

)

r2 = round(

r2_score(

y_test,

pred

),

3

)

print(
f"MAE: {mae}"
)

print(
f"R2 : {r2}"
)


# =====================================
# SAVE
# =====================================

joblib.dump(

model,

MODEL
/
"weather_model.pkl"

)

with open(

MODEL
/
"model_metrics.json",

"w"

) as f:

    json.dump({

        "mae":mae,

        "r2":r2,

        "records":len(df)

    },

    f,

    indent=4

    )


print(
"\nModel Saved"
)

print(
MODEL
/
"weather_model.pkl"
)