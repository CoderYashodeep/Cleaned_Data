
import pandas as pd
from pathlib import Path

file_path = Path(
    r"C:\Users\Yash\OneDrive\Desktop\Data Analyatics project\archive\netflix_titles.csv"
)

output_dir = Path(__file__).resolve().parent / "cleaned_data"
output_dir.mkdir(exist_ok=True)

if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")

df = pd.read_csv(file_path)

initial_rows = len(df)
initial_columns = len(df.columns)

missing_before = df.isnull().sum().copy()
total_missing_before = int(missing_before.sum())

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

print("\n========== ORIGINAL DATASET SHAPE ==========")
print(df.shape)

print("\n========== ORIGINAL COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== ORIGINAL DATASET INFORMATION ==========")
df.info()

print("\n========== MISSING VALUES BEFORE CLEANING ==========")
print(missing_before)

print("\n========== ORIGINAL DUPLICATE ROWS ==========")
print(df.duplicated().sum())

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all"))

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
)

text_columns = df.select_dtypes(include=["object"]).columns

for column in text_columns:
    df[column] = df[column].apply(
        lambda value: " ".join(value.split())
        if isinstance(value, str) else value
    )

if "show_id" in df.columns:
    df["show_id"] = df["show_id"].str.upper()

exact_duplicates = int(df.duplicated().sum())
df = df.drop_duplicates()

duplicate_ids = 0

if "show_id" in df.columns:
    duplicate_ids = int(df["show_id"].duplicated().sum())
    df = df.drop_duplicates(subset=["show_id"], keep="first")

if "type" in df.columns:
    df["type"] = df["type"].str.title()

if "rating" in df.columns:
    df["rating"] = df["rating"].apply(
        lambda value: value.upper()
        if isinstance(value, str) else value
    )

if "listed_in" in df.columns:
    df["listed_in"] = df["listed_in"].apply(
        lambda value: ", ".join(
            item.strip() for item in value.split(",")
        ) if isinstance(value, str) else value
    )

missing_categories = ["director", "cast", "country", "rating"]

for column in missing_categories:
    if column in df.columns:
        df[column] = df[column].fillna("Unknown")

if "date_added" in df.columns:
    df["date_added"] = pd.to_datetime(
        df["date_added"].astype("string").str.strip(),
        format="%B %d, %Y",
        errors="coerce"
    )

if "release_year" in df.columns:
    df["release_year"] = pd.to_numeric(
        df["release_year"], errors="coerce"
    ).astype("Int64")

if "duration" in df.columns:
    df["duration"] = df["duration"].astype("string").str.strip()

missing_key_rows_removed = 0

if "show_id" in df.columns and "title" in df.columns:
    missing_key_rows_removed = int(
        df[["show_id", "title"]].isnull().any(axis=1).sum()
    )
    df = df.dropna(subset=["show_id", "title"])

missing_after = df.isnull().sum().copy()
total_missing_after = int(missing_after.sum())

final_rows = len(df)
final_columns = len(df.columns)

output_file = output_dir / "netflix_cleaned.csv"

df.to_csv(
    output_file,
    index=False,
    date_format="%Y-%m-%d"
)

summary_file = output_dir / "cleaning_summary.txt"

with open(summary_file, "w", encoding="utf-8") as file:
    file.write("NETFLIX DATA CLEANING SUMMARY\n")
    file.write("=" * 40 + "\n\n")

    file.write(f"Initial rows: {initial_rows}\n")
    file.write(f"Initial columns: {initial_columns}\n")
    file.write(f"Exact duplicate rows removed: {exact_duplicates}\n")
    file.write(f"Duplicate show_id records found: {duplicate_ids}\n")
    file.write(f"Rows removed due to missing show_id/title: {missing_key_rows_removed}\n")
    file.write(f"Final rows: {final_rows}\n")
    file.write(f"Final columns: {final_columns}\n\n")

    file.write(f"Total missing values before cleaning: {total_missing_before}\n")
    file.write(f"Total missing values after cleaning: {total_missing_after}\n\n")

    file.write("MISSING VALUES BEFORE CLEANING:\n")
    file.write(missing_before.to_string())
    file.write("\n\nMISSING VALUES AFTER CLEANING:\n")
    file.write(missing_after.to_string())

    file.write("\n\nFINAL DATA TYPES:\n")
    file.write(df.dtypes.astype(str).to_string())

print("\n========== CLEANING COMPLETED ==========")
print("Initial dataset shape:", (initial_rows, initial_columns))
print("Final dataset shape:", (final_rows, final_columns))
print("Exact duplicate rows removed:", exact_duplicates)
print("Duplicate show_id records found:", duplicate_ids)
print("Rows removed due to missing show_id/title:", missing_key_rows_removed)
print("Missing values before cleaning:", total_missing_before)
print("Missing values after cleaning:", total_missing_after)

print("\n========== REMAINING MISSING VALUES ==========")
print(missing_after)

print("\n========== FINAL DATA TYPES ==========")
print(df.dtypes)

print("\nCleaned dataset saved at:", output_file)
print("Cleaning summary saved at:", summary_file)


