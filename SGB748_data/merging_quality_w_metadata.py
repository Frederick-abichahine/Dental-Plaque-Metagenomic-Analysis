# Importing Dependencies
import pandas as pd

# Storing file paths
metadata_file = "./SGB748_data/SGB748_metadata.tsv"
high_quality_file = "./SGB748_data/checkm_output_genus_level_analysis_analysis/high_quality_genomes.csv"
medium_quality_file = "./SGB748_data/checkm_output_genus_level_analysis_analysis/medium_quality_genomes.csv"
output_file = "./SGB748_data/SGB748_metadata_w_quality.tsv"

# Loading the SGB metadata TSV file
metadata_df = pd.read_csv(metadata_file, sep="\t")

# Loading the high and medium quality genome files, and extracting the MAG IDs into separate lists
high_quality_df = pd.read_csv(high_quality_file)
high_quality_mag_ids = high_quality_df.iloc[:, 0].tolist()
medium_quality_df = pd.read_csv(medium_quality_file)
medium_quality_mag_ids = medium_quality_df.iloc[:, 0].tolist()

# Creating a copy of the metadata df and adding a new column in that to store quality information
metadata_df_copy = metadata_df.copy()
metadata_df_copy["Quality"] = "Unknown"

# Looping through the high quality MAG IDs and updating the Quality column in the copy of the metadata df
for mag_id in high_quality_mag_ids:
    metadata_df_copy.loc[metadata_df_copy["magID"] == mag_id, "Quality"] = "High"

# Looping through the medium quality MAG IDs and updating the Quality column in the copy of the metadata df
for mag_id in medium_quality_mag_ids:
    metadata_df_copy.loc[metadata_df_copy["magID"] == mag_id, "Quality"] = "Medium"
    
# Saving the updated dataframe as a new TSV file
metadata_df_copy.to_csv(output_file, sep="\t", index=False)
print(f"Updated metadata file saved as {output_file}.")
