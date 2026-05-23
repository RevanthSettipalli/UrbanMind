def future_weather(model):

    result=[]

    for h in range(40,91,5):

        temp=model.predict([[h]])[0]

        result.append({

            "humidity":h,

            "temperature":round(
                temp,
                1
            )

        })

    return result