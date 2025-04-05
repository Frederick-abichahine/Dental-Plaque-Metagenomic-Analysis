#!/usr/bin/env python3

'''
In this script we exclude hypothetical proteins from the analysis.
'''

# Importing Dependencies
import os
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Function to parse the product column from Prokka .tsv files
def parse_product_column(filepath):
    products = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    if not lines:
        return products

    header = lines[0].strip().split('\t')
    if 'product' not in header:
        print(f">> 'product' column not found in {filepath}")
        return products

    product_index = header.index('product')

    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) > product_index:
            value = parts[product_index].strip()
            if value and value != 'hypothetical protein': # in order to avoid empty or 'hypothetical protein' values
                products.append(value)
    return products

# Function to iterate through all .tsv files and build a MAG-to-product list dictionary
def get_all_mag_products(prokka_output_path):
    mag_dict = {}
    for root, _, files in os.walk(prokka_output_path):
        for file in files:
            if file.endswith(".tsv"):
                filepath = os.path.join(root, file)
                mag_name = os.path.splitext(file)[0]
                product_list = parse_product_column(filepath)
                mag_dict[mag_name] = product_list
                print(f"✅ Parsed {file} — {len(product_list)} valid product entries")
    return mag_dict

# Function to map each product to the set of MAGs it appears in
def get_element_mags(mag_products):
    element_to_mags = defaultdict(set)
    for mag, products in mag_products.items():
        for product in set(products):
            element_to_mags[product].add(mag)
    return element_to_mags

# Function to find products that are common across a certain percentage of MAGs
def find_common_products(element_to_mags, total_mags, percent):
    threshold = math.ceil((percent / 100.0) * total_mags)
    return {
        product for product, mags in element_to_mags.items()
        if len(mags) >= threshold
    }

if __name__ == "__main__":
    prokka_output_path = "./SGB748_data/prokka_output/"
    mag_products = get_all_mag_products(prokka_output_path)
    total_mags = len(mag_products)
    
    print(f"\n** Total MAGs parsed: {total_mags} **")

    element_to_mags = get_element_mags(mag_products)
    
    common_100 = find_common_products(element_to_mags, total_mags, 100)
    common_90 = find_common_products(element_to_mags, total_mags, 90)
    common_80 = find_common_products(element_to_mags, total_mags, 80)
    common_70 = find_common_products(element_to_mags, total_mags, 70)
    common_0 = find_common_products(element_to_mags, total_mags, 0)

    print(f"\n>> Products in 100% of MAGs ({len(common_100)})")
    # print(sorted(common_100))

    print(f"\n>> Products in ≥90% of MAGs ({len(common_90)})")
    # print(sorted(common_90))

    print(f"\n>> Products in ≥80% of MAGs ({len(common_80)})")
    # print(sorted(common_80))

    print(f"\n>> Products in ≥70% of MAGs ({len(common_70)})")
    # print(sorted(common_70))
    
    print(f"\n>> Products in ≥0% of MAGs ({len(common_0)})")
    # print(sorted(common_0))
    

    # Plotting the number of products shared across MAGs
    thresholds = ['≥0%', '≥70%', '≥80%', '≥90%', '100%']
    counts = [len(common_0), len(common_70), len(common_80), len(common_90), len(common_100)]
    colors = sns.color_palette("Set2", len(thresholds))  # You can use "pastel", "husl", etc.

    plt.figure(figsize=(8, 5))
    bars = plt.bar(thresholds, counts, color=colors, edgecolor='black', linewidth=1.2)
    plt.title("Number of Non-Hypothetical Gene Products Shared Across MAGs", fontsize=14, weight='bold')
    plt.xlabel("Presence Threshold", fontsize=12)
    plt.ylabel("Number of Products", fontsize=12)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 5, str(height), ha='center', va='bottom', fontsize=10)
        
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("./SGB748_data/prokka_output_analysis/products_shared_across_mags.png", dpi=300)
    plt.show()

    # Table for products found in 100% of MAGs
    df_common_100 = pd.DataFrame(sorted(common_100), columns=["Product"])
    fig, ax = plt.subplots(figsize=(10, 0.5 * len(df_common_100) + 1))
    ax.axis('off')
    table = ax.table(
        cellText=df_common_100.values,
        colLabels=["Non-Hypothetical Products Found in 100% of MAGs"],
        cellLoc='left',
        colLoc='left',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.auto_set_column_width([0])
    table.scale(1.5, 1.5)

    for key, cell in table.get_celld().items():
        row, col = key
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4C72B0')
        elif row % 2 == 0:
            cell.set_facecolor('#f2f2f2')
        else:
            cell.set_facecolor('white')
        cell.set_edgecolor('grey')
        cell.set_linewidth(0.5)

    plt.tight_layout()
    plt.savefig("./SGB748_data/prokka_output_analysis/products_in_100_percent_MAGs.png", dpi=300)
    plt.show()