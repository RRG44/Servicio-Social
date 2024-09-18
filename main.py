import pandas as pd
import utilities as util
import sys
import os

#! COMMAND: python main.py "file1" "file2" "outputPath"

def run_script(siiaPath, chPath, userPath=""):
    try:
        # file reading
        siia = util.read_siia(siiaPath)
        ch = util.read_ch(chPath)
        siia = util.change_col_order(siia)
        siia.insert(0, "div", "")

        # highlighting
        dfp = util.highlight_differences(siia, ch)
        dfp.data = util.insert_na(dfp.data)

        dfp.set_properties(**{
                'border': '1px solid black',
                'text-align': 'center'
            })

        path = os.path.join(userPath, "comparison.xlsx")
        writer = pd.ExcelWriter(path, engine='xlsxwriter')

        aliases = ['GRUPO','BLOQUE','CVEM','MATERIA CH','PE','CVE PROFESOR CH','PROFESOR CH','LU CH','LU CH','SA CH', 'MA CH', 'MA CH', 'SA CH','MI CH','MI CH','SA CH','JU CH','JU CH','SA CH','VI CH','VI CH','SA CH','','MATERIA SIIA','CVE PROFESOR SIIA','PROFESOR SIIA','LU SIIA','LU SIIA','SA SIIA','MA SIIA','MA SIIA','SA SIIA','MI SIIA','MI SIIA','SA SIIA','JU SIIA','JU SIIA','SA SIIA','VI SIIA','VI SIIA','SA SIIA']
        dfp.to_excel(writer, sheet_name='Sheet1', index=False, header=aliases)

        worksheet = writer.sheets['Sheet1']

        for i, col in enumerate(dfp.data.columns):
            max_len = max(dfp.data[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, max_len + 1)

        writer.close()
        
        return {"success": True}  # Return a success flag if the script completes without errors
    except Exception as e:
        return {"success": False, "error": str(e)}  # Return error details for use in the GUI

def main():
    try:
        siiaPath = sys.argv[1]
        chPath = sys.argv[2]
        userPath = sys.argv[3] if len(sys.argv) == 4 else "" 

        result = run_script(siiaPath, chPath, userPath)
        
        if result["success"]:
            print("Script executed successfully.")
            sys.exit(0)
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()