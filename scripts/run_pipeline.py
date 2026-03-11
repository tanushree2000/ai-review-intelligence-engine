import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")
OUTPUT_PATH = Path("outputs")

OUTPUT_PATH.mkdir(exist_ok=True)

def load_reviews():
    print("Loading reviews...")
    df = pd.read_csv(DATA_PATH / "sample_reviews.csv")
    return df

def analyze_reviews(df):
    print("Analyzing reviews...")

    df["sentiment"] = df["review"].apply(
        lambda x: "positive" if "good" in x.lower() else "negative"
    )

    return df

def save_results(df):
    output_file = OUTPUT_PATH / "review_results.csv"
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

def main():
    df = load_reviews()
    df = analyze_reviews(df)
    save_results(df)

if __name__ == "__main__":
    main()