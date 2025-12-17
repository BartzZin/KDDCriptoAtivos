import matplotlib.pyplot as plt

def analisar_dados(df):
    # Q1 – As altcoins acompanham o comportamento do Bitcoin
    q1_data = (
        df.groupby(["date", "asset_type"])["daily_return"]
        .mean()
        .reset_index()
    )

    q1_pivot = q1_data.pivot(
        index="date",
        columns="asset_type",
        values="daily_return"
    )

    q1_monthly = (
        df.groupby(["month", "asset_type"])["daily_return"]
        .mean()
        .reset_index()
    )

    q1_bar = q1_monthly.pivot(
        index="month",
        columns="asset_type",
        values="daily_return"
    )

    q1_bar.plot(
        kind="bar",
        figsize=(12, 5)
    )

    plt.title("Q1 – Retorno médio mensal: Bitcoin vs Altcoins")
    plt.xlabel("Mês")
    plt.ylabel("Retorno médio")
    plt.legend(title="Ativo")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

    # Q2 – As altcoins apresentam maior volatilidade?
    q2_data = (
        df.groupby("asset_type")["volatility_7d"]
        .mean()
        .reset_index()
    )

    plt.figure()
    plt.bar(q2_data["asset_type"], q2_data["volatility_7d"])
    plt.title("Q2 – Volatilidade média (7 dias)")
    plt.xlabel("Tipo de ativo")
    plt.ylabel("Volatilidade média")
    plt.show()

    # Q3 – Existem períodos de descolamento?
    q3_data = (
        df.groupby(["date", "asset_type"])["cumulative_return"]
        .mean()
        .reset_index()
    )

    q3_pivot = q3_data.pivot(
        index="date",
        columns="asset_type",
        values="cumulative_return"
    )

    plt.figure()
    plt.plot(q3_pivot.index, q3_pivot["Bitcoin"], label="Bitcoin")
    plt.plot(q3_pivot.index, q3_pivot["Altcoin"], label="Altcoins")
    plt.title("Q3 – Retorno acumulado: Bitcoin vs Altcoins")
    plt.xlabel("Data")
    plt.ylabel("Retorno acumulado médio")
    plt.legend()
    plt.show()

    # Q4 – Volume negociado
    q4_data = (
        df.groupby(["date", "asset_type"])["volume"]
        .mean()
        .reset_index()
    )

    q4_pivot = q4_data.pivot(
        index="date",
        columns="asset_type",
        values="volume"
    )

    plt.figure()
    plt.plot(q4_pivot.index, q4_pivot["Bitcoin"], label="Bitcoin")
    plt.plot(q4_pivot.index, q4_pivot["Altcoin"], label="Altcoins")
    plt.title("Q4 – Volume médio negociado")
    plt.xlabel("Data")
    plt.ylabel("Volume médio")
    plt.legend()
    plt.show()

    # Q5 – Tendência via médias móveis
    q5_data = (
        df.groupby(["date", "asset_type"])
        .agg({
            "price_ma7": "mean",
            "price_ma30": "mean"
        })
        .reset_index()
    )

    q5_bitcoin = q5_data[q5_data["asset_type"] == "Bitcoin"]
    q5_altcoin = q5_data[q5_data["asset_type"] == "Altcoin"]

    plt.figure()
    plt.plot(q5_bitcoin["date"], q5_bitcoin["price_ma7"], label="BTC MA7")
    plt.plot(q5_bitcoin["date"], q5_bitcoin["price_ma30"], label="BTC MA30")
    plt.title("Q5 – Bitcoin: Médias móveis")
    plt.xlabel("Data")
    plt.ylabel("Preço médio")
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(q5_altcoin["date"], q5_altcoin["price_ma7"], label="Altcoins MA7")
    plt.plot(q5_altcoin["date"], q5_altcoin["price_ma30"], label="Altcoins MA30")
    plt.title("Q5 – Altcoins: Médias móveis")
    plt.xlabel("Data")
    plt.ylabel("Preço médio")
    plt.legend()
    plt.show()