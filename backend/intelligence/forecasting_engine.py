

import pandas as pd

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except Exception:
    PROPHET_AVAILABLE = False


def forecast_30_days(df: pd.DataFrame):
    """
    Forecast Urban Intelligence for 30 days.

    Expected columns:
    - time
    - temperature

    Returns:
    {
        'forecast_df': dataframe,
        'confidence': float,
        'model': str
    }
    """

    if df.empty:
        return {
            'forecast_df': pd.DataFrame(),
            'confidence': 0,
            'model': 'Unavailable'
        }

    try:
        work_df = df.copy()

        work_df['time'] = pd.to_datetime(
            work_df['time'],
            errors='coerce'
        )

        work_df = work_df.dropna(
            subset=['time']
        )

        prophet_df = pd.DataFrame({
            'ds': work_df['time'],
            'y': pd.to_numeric(
                work_df['temperature'],
                errors='coerce'
            )
        }).dropna()

        if len(prophet_df) < 10:
            raise ValueError('Insufficient data')

        if PROPHET_AVAILABLE:
            model = Prophet(
                daily_seasonality=True
            )

            model.fit(prophet_df)

            future = model.make_future_dataframe(
                periods=30
            )

            forecast = model.predict(future)

            result = forecast[
                ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
            ].tail(30)

            confidence = 95

            return {
                'forecast_df': result,
                'confidence': confidence,
                'model': 'Prophet'
            }

        forecast_base = prophet_df['y'].mean()

        result = pd.DataFrame({
            'ds': pd.date_range(
                start=prophet_df['ds'].max(),
                periods=30,
                freq='D'
            ),
            'yhat': [forecast_base + i * 0.05 for i in range(30)]
        })

        result['yhat_lower'] = result['yhat'] - 1
        result['yhat_upper'] = result['yhat'] + 1

        return {
            'forecast_df': result,
            'confidence': 80,
            'model': 'Fallback Forecast'
        }

    except Exception:
        return {
            'forecast_df': pd.DataFrame(),
            'confidence': 0,
            'model': 'Error'
        }