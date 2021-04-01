import json 
import numpy as np 
import pandas as pd 
import codecs



class Rest_Data:

    class Get_Data:
        def __init__(self, path):        
            self.path = path
        
        def _read_file(self):
            fileObj = codecs.open( self.path, "r", "utf_8_sig" )
            text = fileObj.read() 
            fileObj.close()
            return text

        def _format_json(self):
            return json.loads(self._read_file())['data']['items']
        
        def _start_DataFrame(self):
            """
            drop (bool) - drop unsesery columns or not, columns write in  __init__ 
            """
            data_json = self._format_json()

            if len(data_json)>1:
                data_frame = pd.DataFrame([data_json[0]])
                for i in  range(1, len(data_json)):
                    prom = pd.DataFrame([ data_json[i]])
                    data_frame = pd.concat([data_frame, prom])
            else:
                data_frame = data_frame=pd.DataFrame([data_json[0]])

            return data_frame

