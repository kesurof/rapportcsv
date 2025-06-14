import pandas as pd

def write_to_excel(dataframe):
    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter('Analyse de Parc.xlsx', engine='xlsxwriter') as writer:
        # Write the dataframe to the specified sheet
        dataframe.to_excel(writer, sheet_name='Export', index=False)