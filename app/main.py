from fastapi import FastAPI, HTTPException
import pandas as pd

from app.data_loader import load_rates


app = FastAPI(title="ECB FX API")

DATA_FILE = "data/ecb_rates.csv"


def get_data():
    return load_rates(DATA_FILE)

def get_currency_rate(row, currency):
    if currency == "EUR":
        return 1.0

    return row[currency]

@app.get("/rate")
def get_exchange_rate(
    date: str,
    from_currency: str,
    to_currency: str
):
    df = get_data()

    try:
        row = df[df["Date"] == pd.to_datetime(date)]

        if row.empty:
            raise HTTPException(
                status_code=404,
                detail="Exchange rate not found for the given date"
            )

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency != "EUR" and from_currency not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Invalid source currency"
            )

        if to_currency != "EUR" and to_currency not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Invalid target currency"
            )

        from_rate = get_currency_rate(row.iloc[0], from_currency)
        to_rate = get_currency_rate(row.iloc[0], to_currency)

        rate = float(to_rate) / float(from_rate)

        return {
            "date": date,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": rate
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/rates")
def get_exchange_rates(
    from_date: str,
    to_date: str,
    from_currency: str,
    to_currency: str
):
    df = get_data()

    try:
        from_date = pd.to_datetime(from_date)
        to_date = pd.to_datetime(to_date)

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency != "EUR" and from_currency not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Invalid source currency"
            )

        if to_currency != "EUR" and to_currency not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Invalid target currency"
            )

        if from_date > to_date:
            raise HTTPException(
                status_code=400,
                detail="from_date cannot be after to_date"
            )

        rows = df[
            (df["Date"] >= from_date) &
            (df["Date"] <= to_date)
        ]

        if rows.empty:
            raise HTTPException(
                status_code=404,
                detail="No exchange rates found for the given date range"
            )

        result = []

        for _, row in rows.iterrows():

            from_rate = get_currency_rate(row, from_currency)
            to_rate = get_currency_rate(row, to_currency)
            rate = float(to_rate) / float(from_rate)

            result.append({
                "date": row["Date"].strftime("%Y-%m-%d"),
                "from_currency": from_currency,
                "to_currency": to_currency,
                "rate": rate
            })

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )