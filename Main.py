import pandas as pd
import numpy as np
from AnaliseGeral import analisar_dados

# 1. CARREGAMENTO DA BASE DE DADOS
df = pd.read_csv("crypto_historical_365days.csv")

# 2. SELEÇÃO DAS VARIÁVEIS RELEVANTES
cols_relevantes = [
    "coin_id",
    "coin_name",
    "symbol",
    "market_cap_rank",
    "timestamp",
    "date",
    "month",
    "price",
    "market_cap",
    "volume",
    "daily_return",
    "price_ma7",
    "price_ma30",
    "volatility_7d",
    "cumulative_return"
]

df = df[cols_relevantes]

# 3. CONVERSÃO DE TIPOS
df["date"] = pd.to_datetime(df["date"])
df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")

num_cols = [
    "price",
    "market_cap",
    "volume",
    "daily_return",
    "price_ma7",
    "price_ma30",
    "volatility_7d",
    "cumulative_return"
]

df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

# 4. REMOÇÃO DE REGISTROS DUPLICADOS
df = df.drop_duplicates(subset=["coin_id", "date"])

# 5. TRATAMENTO DE VALORES AUSENTES
# Remove registros com dados críticos ausentes
df = df.dropna(subset=["price", "market_cap", "volume"])

# 6. VERIFICAÇÃO DE CONSISTÊNCIA TEMPORAL
df = df.sort_values(by=["coin_id", "date"])

# 7. CLASSIFICAÇÃO: BITCOIN VS ALTCOINS
df["asset_type"] = np.where(
    df["coin_name"].str.lower() == "bitcoin",
    "Bitcoin",
    "Altcoin"
)

# 8. AGREGAÇÃO TEMPORAL (MENSAL)
df_monthly = (
    df.groupby(["asset_type", "coin_name", "month"])
    .agg({
        "price": "mean",
        "daily_return": "mean",
        "volatility_7d": "mean",
        "volume": "mean",
        "cumulative_return": "last"
    })
    .reset_index()
)

# 9. NORMALIZAÇÃO (MIN-MAX)
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df_monthly["price_norm"] = min_max_normalize(df_monthly["price"])
df_monthly["volume_norm"] = min_max_normalize(df_monthly["volume"])
df_monthly["volatility_norm"] = min_max_normalize(df_monthly["volatility_7d"])

# 10. BASE FINAL PRONTA PARA ANÁLISE
print("Base diária preparada:", df.shape)
print("Base mensal preparada:", df_monthly.shape)

# df -> base diária tratada
# df_monthly -> base agregada mensalmente

analisar_dados(df)