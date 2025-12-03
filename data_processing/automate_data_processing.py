import pandas as pd
import glob
import os

from numpy.matlib import empty

# -----------------------------
# CONFIG
# -----------------------------
DATA_FOLDER = "data"  # folder where your CSV files are
OUTPUT_FILE = "merged_cleaned_large.csv"
CHUNK_SIZE = 100000  # number of rows per chunk


# -----------------------------
# FUNCTION: Process CSV in chunks
# -----------------------------
def process_large_csv(file_path, chunksize=CHUNK_SIZE):
    cleaned_chunks = []

    categorical_counts = {}

    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        # Clean chunk
        chunk = chunk.drop_duplicates()
        chunk = chunk.fillna("0")

        str_cols = chunk.select_dtypes(include=["object"]).columns
        for col in str_cols:
            chunk[col] = chunk[col].str.strip()

        # Update numeric summary
        numeric_cols = chunk.select_dtypes(include=["number"]).columns

        # Update categorical counts
        cat_cols = chunk.select_dtypes(include=["object"]).columns
        for col in cat_cols:
            counts = chunk[col].value_counts()
            if col not in categorical_counts:
                categorical_counts[col] = counts
            else:
                categorical_counts[col] = categorical_counts[col].add(counts, fill_value=0)

        # Append cleaned chunk to list for saving
        cleaned_chunks.append(chunk)

    return cleaned_chunks, categorical_counts


# -----------------------------
# MAIN AUTOMATION
# -----------------------------
if __name__ == "__main__":
    csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    if not csv_files:
        print("No CSV files found in folder:", DATA_FOLDER)
    else:
        all_cleaned_chunks = []
        final_numeric_summary = None
        final_categorical_counts = {}

        for file in csv_files:
            print(f"Processing file: {file}")
            chunks, cat_counts = process_large_csv(file, CHUNK_SIZE)
            all_cleaned_chunks.extend(chunks)


            # Merge categorical counts
            for col, counts in cat_counts.items():
                if col not in final_categorical_counts:
                    final_categorical_counts[col] = counts
                else:
                    final_categorical_counts[col] = final_categorical_counts[col].add(counts, fill_value=0)

        # Save cleaned data incrementally to CSV to avoid memory issues
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            header_written = False
            for chunk in all_cleaned_chunks:
                chunk.to_csv(f, index=False, header=not header_written)
                header_written = True

        print(f"Cleaned merged data saved to {OUTPUT_FILE}")

        # Display analysis
        print("\n--- Numeric Summary ---")
        if final_numeric_summary is not None:
            print(final_numeric_summary)

        print("\n--- Categorical Counts ---")
        for col, counts in final_categorical_counts.items():
            print(f"\nColumn: {col}")
            print(counts)

