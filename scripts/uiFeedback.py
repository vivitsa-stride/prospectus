import json
import pdfplumber


def extract(input_file, data):
    
    
    pdf_obj = pdfplumber.open(input_file,laparams = {})
   
    final_result = {'UI':{}, 'MT_DATA':{}}

    # populate final result
         
  
    pdf_obj.close()
    return final_result


