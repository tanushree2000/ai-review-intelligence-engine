import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    print("Loading dataset...")
    df = pd.read_csv(DATA_DIR / "sample_reviews.csv")
    return df

def sentiment_analysis(df):
    print("Running sentiment analysis...")

    df["sentiment"] = df["review"].apply(
        lambda x: "positive" if "good" in x.lower() else "negative"
    )

    return df

def save_results(df):
    output_file = OUTPUT_DIR / "review_results.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved results to {output_file}")

def main():
    df = load_data()
    df = sentiment_analysis(df)
    save_results(df)

if __name__ == "__main__":
    main()