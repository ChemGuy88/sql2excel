
def getTableDescription(tableName, connection):
    """
    Gets table description using Oracle syntax
    """
    query = "SELECT table_name, column_name, data_type, data_length\n" +\
            "FROM all_tab_columns\n" +\
            f"WHERE table_name = '{tableName}'"
    output = pd.read_sql_query(sql=query, con=connection)
    return output


def getTableIntersection(tables, connection):
    """
    Creates a table listing the SQL columns and in what tables they are found.
    """
    descriptions = {}
    for tableName in tables:
        descriptions[tableName] = getTableDescription(tableName, connection)

    columns = set()
    for tableName, df in descriptions.items():
        columns.update(df["column_name"])

    results = pd.DataFrame(None, index=columns, columns=sorted(descriptions.keys())).sort_index()
    for columnName in columns:
        for tableName, df in descriptions.items():
            if columnName in df["column_name"].values:
                results[tableName][columnName] = True
            elif columnName not in df["column_name"].values:
                results[tableName][columnName] = ""
    
    return results


def predictColumnWidth(numCharacters, extrapolate=False):
    """
    Returns the predicted column width for Excel spreadsheets given a length in terms of number of characters.
    The prediction is based on a linear regression on empirical data with a range from 9 to 23.
    See `determineColumnWidth.py`
    """
    if not extrapolate:
        assert numCharacters >= 9
        assert numCharacters <= 23
    coef =  1.302135796233495
    intercept = -2.6305462154556647
    maximumCorrection = 1.4478302907857667  # Maximum deviation from the regression line based on training data
    width = numCharacters *  coef + intercept + maximumCorrection
    return width


def tableDescriptions2Excel(tables, fpath, connection):
    """
    Gets and saves tables descriptions to an Excel spreadsheet.
    """
    with pd.ExcelWriter(fpath) as writer:
        for tableName in tables:
            df = getTableDescription(tableName, connection)
            df.to_excel(writer, sheet_name=tableName, index=False)
            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                predicted_column_length = predictColumnWidth(column_length)
                writer.sheets[tableName].set_column(col_idx, col_idx, predicted_column_length)