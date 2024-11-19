# cd "C:\Users\paul\OneDrive - Oldendorff Carriers\Documents\Python Scripts\BOSS Raw dat"
# streamlit run boss_cleanup.py

import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import io

st.set_page_config(page_icon="📋",)

# Streamlit app title
st.title("BOSS Raw Data Processor")

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload BOSS raw data files", accept_multiple_files=True, type="xlsx")

# Minimum steaming hours input
min_steaming_hrs = st.number_input("Minimum Steaming Hrs", min_value=0, value=22)

# Processing each uploaded file
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Load the Excel file and skip the first 4 rows
        df = pd.read_excel(uploaded_file, skiprows=4)

        # Step 1: Paste values and rename columns as specified
        rename_columns = {
            25: "DMG",
            54: "Total Cons/day",
            55: "ME Cons/day",
            56: "AE Cons/day",
            57: "Blr Cons/day",
            58: "ME - MT/NM"
        }
        for col, new_name in rename_columns.items():
            df.iloc[:, col] = df.iloc[:, col].values  # Paste values
            df.rename(columns={df.columns[col]: new_name}, inplace=True)

        # Rename additional specified columns
        rename_cols = {
            0: "S.No", 1: "Vessel Name", 2: "Voyage No", 3: "From", 4: "To", 
            5: "Date/Time", 8: "Condition", 9: "Lat", 10: "Long", 12: "Report Type", 
            23: "Steaming Hrs", 24: "SOG", 26: "BF (Rep)", 27: "Wind Dir (R) (Rep)", 
            28: "Sea State (R)", 183: "Disp", 185: "Cargo wt", 186: "Ballast",
            188: "Draft F", 189: "Draft A", 191: "ME Load", 192: "RPM", 193: "Slip%", 
            194: "DTW", 196: "STW (HC)", 204: "STW (Rep)", 205: "CSS", 206: "BF (HC)",
            207: "Wind Dir (R) (HC)", 208: "Sig wave ht (HC)", 209: "Sig wave Dir (HC)",
            210: "CF (HC)", 211: "AE 1 hrs", 212: "AE 2 Hrs", 213: "AE 3 hrs", 
            215: "Sig wave ht (Rep)", 216: "Scav Air Press"
        }
        df.rename(columns={df.columns[k]: v for k, v in rename_cols.items()}, inplace=True)

        # Step 2: Create calculated columns
        df["Avg Draft"] = (df.iloc[:, 188] + df.iloc[:, 189]) / 2  # Average Draft (Col 190)
        df["DMG"] = df["Steaming Hrs"] * df["SOG"]  # DMG as Steaming Hrs * SOG
        df["Total Cons/day"] = df["ME Cons/day"] + df["AE Cons/day"] + df["Blr Cons/day"]  # Total Cons/day as sum

        # Step 3: Drop specified columns
        delete_cols = [6, 7, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 29, 30, 31, 
                       32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 
                       48, 49, 50, 51, 52, 53, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 
                       69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 
                       85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 
                       101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 
                       114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 
                       127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 
                       140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 
                       153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 
                       166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 
                       179, 180, 181, 182, 184, 187, 195, 197, 198, 199, 200, 201, 202, 203]
        df.drop(df.columns[delete_cols], axis=1, inplace=True)

        # Step 4: Filter based on Steaming Hrs
        df = df[df['Steaming Hrs'] >= min_steaming_hrs]

        # Step 5: Reorder columns as specified
        new_column_order = [
            "S.No", "Vessel Name", "Voyage No", "From", "To", "Date/Time", "Condition", "Lat", "Long", 
            "Report Type", "Steaming Hrs", "DMG", "DTW", "SOG", "STW (HC)", "STW (Rep)", "CSS", "CF (HC)", 
            "Total Cons/day", "ME Cons/day", "AE Cons/day", "Blr Cons/day", "ME - MT/NM", "Disp", 
            "Cargo wt", "Ballast", "Draft F", "Draft A", "Avg Draft", "BF (Rep)", "BF (HC)", 
            "Wind Dir (R) (Rep)", "Wind Dir (R) (HC)", "Sea State (R)", "Sig wave ht (Rep)", "Sig wave ht (HC)", 
            "Sig wave Dir (HC)", "ME Load", "RPM", "Slip%", "AE 1 hrs", "AE 2 Hrs", "AE 3 hrs", "Scav Air Press"
        ]
        df_reordered = df[new_column_order]

        # Step 6: Limit decimal places to 2 for all numeric columns
        df_reordered = df_reordered.round(2)

        # Step 7: Export to Excel with auto-fit column widths
        wb = Workbook()
        ws = wb.active

        # Add headers and data to the worksheet
        for r_idx, row in enumerate(dataframe_to_rows(df_reordered, index=False, header=True)):
            ws.append(row)

        # Auto-fit column widths
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter  # Get the column name
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2  # Add a little extra space
            ws.column_dimensions[col_letter].width = adjusted_width

        # Save the file to a BytesIO stream to enable download
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        # Generate a unique filename
        vessel_name = df_reordered["Vessel Name"].iloc[0] if "Vessel Name" in df_reordered else "Unknown_Vessel"
        filename = f"BOSS_raw_data_{vessel_name}_{datetime.now().strftime('%d%m%y%H%M')}.xlsx"

        # Provide download link
        st.download_button(label=f"Download Processed File: {filename}", data=output, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
