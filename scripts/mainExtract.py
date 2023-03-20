import json
import pdfplumber

def extract(input_file, data):
    """
    input_file: any Prospectus pdf
    data: data that needs to be extracted. Typically a json with empty fields
    """
    # print("extraction")

    pdf_obj = pdfplumber.open(input_file,laparams = {})
    final_result = {'UI':{}, 'MT_DATA':{}}

    # populate final_result



    pdf_obj.close()
    #print(final_result)
    return final_result
        
 