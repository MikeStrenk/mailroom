def output_excel(df, wkng_folder, filename):
    """Renders and saves an excel file from a dataframe, returns full filepath"""
    full_filepath = wkng_folder + filename

    writer = pd.ExcelWriter(full_filepath, engine="xlsxwriter")

    df.to_excel(writer, sheet_name="team_data", index=False)
    master_df.to_excel(writer, sheet_name="raw_data", index=False)

    df_col_names = [{"header": col_name} for col_name in df.columns.values.tolist()]

    format_excel(writer, df.shape, df_col_names)
    writer.save()
    print(f"\n Saved the Excel File as {filename}")

    return full_filepath
