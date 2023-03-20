

import traceback
import pdfplumber
import re
import os
import string
from helpers import _get_regex_finder

def _get_regex_finder(string_):
        try:
            pattern = re.compile(rf'(?i){string_}(:)?')
            return pattern
        except:
            print(traceback.print_exc())

class Page():

    def __init__(self,pdf_obj, page_number):

        self.page_number = page_number
        self.pdf_obj = pdf_obj
        self.page = self._go_to_page_in_pdf(page_number)
        self.page_width = self.page.width
        self.page_height = self.page.height
        self.page_textelements = sorted(self.page.textlinehorizontals, key = lambda x: x['y0'], reverse=True)
        self.page_text = self._get_text_only(self.page_textelements)
        # Footer 
        self.footer_texts = self._get_footer_texts()
        self.footer_text_elements = self._get_footer_text_elements()
        self.footer_bbox = self._get_footer_bbox()
        


    def _go_to_page_in_pdf(self,page_number):
        try:
            # pageObj = self.pdfReader.getPage(page_number)
            page_number = page_number-1
            page = self.pdf_obj.pages[page_number]
            return page
        except:
            print(traceback.print_exc())
            return None


    def _get_text_only(self,textelements):
        text = []
    
        for element in textelements:
            try:
                if element["text"]:
                    # text = text + " " + element["text"]
                    text.append(element["text"])
            except:
                pass
        return text


    def _remove_all(self,list_of_lists,string_):
        for list_ in list_of_lists:
            for item in list_:
                if item in string_: 
                    string_ = string_.replace(item, " ")
        return string_
    

    def _clean(self,text):

        try:

            stop_words = ['of ','on ', 'a ', 'the ','Of ', 'On ', 'A ', 'The ', 'Is ']
            full_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            short_months = [d[:4] for d in full_months]
            shorter_months = [d[:3] for d in full_months]

            rm_list = [stop_words,full_months,short_months,shorter_months]

            text = self._remove_all(rm_list,text)
            
            new_text = re.sub(r"[^a-zA-Z]", " ", text)
            new_text = new_text.strip()
            if new_text.isspace()==False and new_text!='':
                return new_text
        except:
            pass

    

    def _get_text_in_bbox(self,bbox):
        try:
            top_limit = 0
            bottom_limit = 0
            x0_limit = 0
            x1_limit = 0
            text_in_bbox = ""

            # page_chars = self.page.chars
            # for element in page_chars:

            for element in self.page_textelements:
                if element["top"]>=bbox[1]+top_limit and element["bottom"]<=bbox[3]-bottom_limit and element["x0"]>=bbox[0]+x0_limit and element["x1"]<=bbox[2]-x1_limit:
                    text_in_bbox += element["text"]
            return text_in_bbox
        except:
            pass
    def _get_text_elements_in_bbox(self,bbox):

        top_limit = 0
        bottom_limit = 0
        x0_limit = 0
        x1_limit = 0
        text_elements_in_bbox = []

        # page_chars = self.page.chars
        # for element in page_chars:
        try:
            for element in self.page_textelements:
            
                if element["top"]>=bbox[1]+top_limit and element["bottom"]<=bbox[3]-bottom_limit and element["x0"]>=bbox[0]+x0_limit and element["x1"]<=bbox[2]-x1_limit:
                    text_elements_in_bbox.append(element)
            return text_elements_in_bbox

        except:
            pass

    

    def _approx_footer_text_elements(self,page_number):
        # get last 10% of text from given page
        footer_text_elements = []

        page = self._go_to_page_in_pdf(page_number)
        page_width = page.width
        page_height = page.height
        page_textelements = sorted(page.textlinehorizontals, key = lambda x: x['y0'], reverse=True)

        footer_top = .10*self.page_height
        footer_bottom = self.page_height
        try:
            for element in page_textelements:
                if element["y1"]<=footer_top:
                    footer_text_elements.append(element)
            
            return footer_text_elements
        except:
            pass

    
        
    def _get_footer_bbox(self):
        footer_bbox = []
        x0,x1,top,bottom = None,None,None,None
        try:
            for element in self.footer_text_elements:
                if x0 == None and x1 == None and top == None and bottom == None:
                    x0 = element["x0"]
                    x1 = element["x1"]
                    top = element["top"]
                    bottom = element["bottom"]

                else:
                    if element["x0"]<x0:
                        x0 = element["x0"]
                    if element["top"]<top:
                        top = element["top"]
                    if element["x1"]>x1:
                        x1 = element["x1"]
                    if element["bottom"]>bottom:
                        bottom = element["bottom"]
            footer_bbox = [x0, top, x1, bottom]
            
            return footer_bbox
        except:
            pass



    def chkList(self,lst):
        try:
            return len(set(lst)) == 1
        except:
            pass
    

    def _clean_list(self,text_list):
        list_ = []
        try:
            for element in text_list:
                cleaned_element = self._clean(element)
                if element is not None:               
                    list_.append(cleaned_element)
            return list_
        except:
            pass

    def _get_footer_texts(self):
        footer_texts = []
        try:
            for i in range(7):
                dummy_text_elements = self._approx_footer_text_elements(i)
                dummy_texts = self._get_text_only(dummy_text_elements)
                dummy_texts = self._clean_list(dummy_texts)
                footer_texts.append(dummy_texts)
            # print("footer texts = ", footer_texts)
            footer_texts = self._get_common_elements(footer_texts)
            return footer_texts
        except:
            pass

    def _get_footer_text_elements(self):
        footer_text_elements = []
        try:
            for element in self.page_textelements:
                clean_text = self._clean(element["text"])
                for e in self.footer_texts:
                    if e is not None:
                        # for e_ in e:
                            # if e_ in element["text"]  and element not in footer_text_elements:
                            #     footer_text_elements.append(element)
                        if e==clean_text:
                            footer_text_elements.append(element)
            return footer_text_elements
        except:
            pass

        

    # function to get common elements from all lists
    # Python program to find the common elements
    def _get_common_elements(self,list_of_lists):
        try:
            res = list(set.intersection(*map(set, list_of_lists)))
            res = list(filter(lambda item: item is not None, res))


            return res
        except:
            pass
    
import pandas as pd
class PDF():

# comprises of all pages in a document
# toc
# refer page by page
# get section
# header, footer

    def __init__(self,pdf_obj) -> None:
        self.pdf_obj = pdf_obj
        self.numberOfPages = len(self.pdf_obj.pages)
        self.toc_page_number, self.toc_text = self.getTOC_text()
        self.toc_tuples = self._get_toc_tuples()
        self.toc_df = self.getTOC_df()

    def _go_to_page_in_pdf(self,page_number):
        try:
            # pageObj = self.pdfReader.getPage(page_number)
            page_number = page_number
            page = self.pdf_obj.pages[page_number]
            return page
        except:
            print(traceback.print_exc())
            return None
    def getTOC_df(self):
        """
        tuple = (heading, page number)
        df = all tuples
        """
        df = pd.DataFrame(self.toc_tuples, columns =['heading', 'pageNumber'])
        return df

        


    def getTOC_text(self):
        # look for "table of contents", "contents", "index"
        # font must be large, bold
        # text must be center aligned

        keywords = ["table of contents","contents"]
        for i in range(self.numberOfPages):
            page_i = Page(self.pdf_obj,i)
            page_textelements_ = page_i.page_textelements
            for element in page_textelements_:
                for keyword in keywords:
                    x = _get_regex_finder(keyword).search(element["text"])
                    if x:
                        
                        return page_i.page_textelements[0]["page_number"], page_i.page_textelements
                        # get text element that has "toc"
                        # check font
                        # check size
                        # check bbox- if in second half of the page, return next page as well
                        

    def _detect_dots(self,line):
        count=0
        for i in range(len(line)):
            if line[(i*-1)] == '.':
                count+=1
        return count

    

    def _get_toc_tuples(self):
        toc_tuples = []
        for i in range(len(self.toc_text)-1):
            element = self.toc_text[i]
            line = element["text"]
            if(line.endswith('. . .\n')) or (line.endswith('...\n')):
                # page number is in next line
                pageNumber = self.toc_text[i+1]["text"]
                heading = element["text"].replace(".","")
                heading = heading.strip()
                tuple_ =  heading,pageNumber
                toc_tuples.append(tuple_)
            
            elif line[-2].isnumeric and len(line)>10:
                line_heading = line[:-7]
                if(line_heading.endswith('. . . ')) or (line_heading.endswith('. . .')) or (line_heading.endswith('...')):
                    # page number is in next line

                    line_pn = line[-7:]
                    pageNumber = self._clean(line_pn)
                    heading = self._clean(line_pn)
                    tuple_ =  heading,pageNumber
                    toc_tuples.append(tuple_)
        return toc_tuples
    
    def _clean(self,line):
        line = line.replace(".","")
        line = line.strip()

        return line
    # the maximum value
    def extractMaximum(self,ss):
        num, res = 0, 0
        
        # start traversing the given string
        for i in range(len(ss)):
            
            if ss[i] >= "0" and ss[i] <= "9":
                num = num * 10 + int(int(ss[i]) - 0)
            else:
                res = max(res, num)
                num = 0
            
        return max(res, num)


    def _get_real_page_number(self,page_start,pageNoText):
        for i in range(page_start,self.numberOfPages):
            page_number = i
            page_ = Page(self.pdf_obj, page_number)
            text_elements = page_.page_textelements
            for element in text_elements[-4:]:
                if element["text"]==pageNoText:
                    return page_number


    def _get_heading_page(self, heading):
        for i in range(len(self.toc_df["heading"])):
            element = self.toc_df["heading"][i]
            pattern = _get_regex_finder(heading)
            x = pattern.search(element)
            if x:
                pageNoText = self.toc_df["pageNumber"][i]
                page_number = self._get_real_page_number(self.toc_page_number,pageNoText)
                return page_number
            

    def get_section(self,heading):
        """
        given heading1, and page number1 and heading1, page number2,
        get text within
        """
        heading1 = heading
        
        for i in range(len(self.toc_df["heading"])):
            element = self.toc_df["heading"][i]
            try:
                heading2 = self.toc_df["heading"][i+1]
                
            except:
                pass
            
        

            pattern = _get_regex_finder(heading1)
            x = pattern.search(element)

            if x:

                pageNoText = self.toc_df["pageNumber"][i]
                pn1 = self._get_real_page_number(self.toc_page_number,pageNoText)
                # page start is the page number of the heading
                page_start = pn1
                # page end is the page number of the next heading
                pageNoText = self.toc_df["pageNumber"][i+1]
                pn2 = self._get_real_page_number(self.toc_page_number,pageNoText)
                page_end = pn2
                

                section_text = []
                for idx in range(page_start, page_end+1):
                    text = Page(self.pdf_obj,idx).page_textelements
                    if idx == page_end:
                        heading2 = "Information on Sales Charges and Distribution Related Expenses"
                        text = self._split_list(text,heading2)

            
                    for j in range(len(text)):
                        

                        if element in text[j]["text"]:
                            section_text =  text[j:]
                            j = len(text[j:])
                            break

                        elif idx>page_start and idx<page_end+1:
                            section_text.append(text[j])

    
                            
                        else: 
                            pass
                        
                    
                    else:
                        pass

        text_only = ""
        for e in section_text:
            text_only = text_only+e["text"]

        return text_only

    def _split_list(self, list_, string_):
        # split list from where text element == string
        for i in range(len(list_)):
            if string_ in list_[i]["text"]:
                list_ = list_[:i]
                break
        return list_



# if(line.endswith('.')):
#             print(str(_detect_dots(line)))

from time import time
if __name__ == "__main__":

    dir_path = r'/home/vaibhav/Downloads/VAFs/'

    # list to store files
    files = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):

            files.append(path)
    i = 0
    for file in files:
        if i>0:
            break
        # print(i)
        # pdf_path = "/home/vaibhav/Downloads/ProspectusSamples/BLACKROCK MANAGED VOLATILITY PORTFOLIO pro-brfunds-managedvolatilityport-svc-us.pdf"
        # pdf_path = "/home/vaibhav/Downloads/ProspectusSamples/2008936 - Candriam-bonds intermnational.pdf"
        pdf_path = "/home/vaibhav/Downloads/ProspectusSamples/BLACKROCK MANAGED VOLATILITY PORTFOLIO sai-brfunds-managedvolatilityport-us.pdf"
        pdf_obj = pdfplumber.open(pdf_path,laparams = {})
        
        for j in range(20):
            if j>0:
                break
            source = j

            p = PDF(pdf_obj)
            # p = Page(pdf_obj,2)
            start_time = time()
            # print(p.page_textelements)
            end_time = time()
            # print("time taken =", end_time-start_time)
           # get footer
            if p.toc_text:
                p
                # print("table of contents = ", p.toc_df)
                print("section text elements = ",p.get_section("Management, Advisory and Other Service Arrangements"))
                # print("footer bbox = ",p.footer_bbox)
                # print("toc text elements= ",p.footer_text_elements)
            else:
                pass
                # print("pdf_path = ",file)
                # print("toc not found!")
            
        i = i+1


