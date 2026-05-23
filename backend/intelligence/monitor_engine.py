try:
    import psutil
except:
    psutil = None


def get_system_metrics(records):

    cpu = (

        psutil.cpu_percent()

        if psutil

        else 0

    )

    ram = (

        psutil.virtual_memory().percent

        if psutil

        else 0

    )

    confidence = min(

        98,

        max(
            70,
            65 + records // 100
        )

    )

    health = max(

        0,

        100 -

        (

            cpu * .3

            +

            ram * .2

        )

    )

    return {

        "cpu": round(cpu),

        "ram": round(ram),

        "confidence": round(confidence),

        "health": round(health)

    }