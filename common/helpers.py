import traceback
import re

def _get_regex_finder(string_):
        try:
            pattern = re.compile(rf'(?i){string_}(:)?')
            return pattern
        except:
            print(traceback.print_exc())
            return None
        
def _get_strict_regex_finder(string_):
        try:
            pattern = re.compile(rf'{string_}(:)?')
            return pattern
        except:
            print(traceback.print_exc())
            return None