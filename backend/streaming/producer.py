import json
import time


while True:

    print(
        json.dumps(
            {
                "temp": 30
            }
        )
    )

    time.sleep(5)