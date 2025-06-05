import os
import csv

BASE_DIR = 'yelp_output'
MERGED_DIR = '01merged'
os.makedirs(MERGED_DIR, exist_ok=True)

for region_folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, region_folder)
    if not os.path.isdir(folder_path):
        continue

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') and not f.endswith('_combined.csv')]

    if not csv_files:
        print(f"📂 Skipping {region_folder}: no CSVs found.")
        continue

    combined_csv_path = os.path.join(MERGED_DIR, f"{region_folder.replace(' ', '_')}_combined.csv")
    print(f"🔁 Merging {len(csv_files)} files from {region_folder} into {combined_csv_path}")

    seen_aliases = set()
    header_written = False

    with open(combined_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = None

        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            with open(file_path, mode='r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader)

                if not header_written:
                    writer = csv.writer(outfile)
                    writer.writerow(header)
                    header_written = True

                for row in reader:
                    alias = row[0]  # alias is the first column
                    if alias in seen_aliases:
                        continue
                    seen_aliases.add(alias)
                    writer.writerow(row)

    print(f"✅ Merged: {combined_csv_path} ({len(seen_aliases)} unique entries)")
