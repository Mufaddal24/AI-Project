import json, re, os, glob
from tkinter import filedialog
from tkinter import *
root = Tk()
root.withdraw()
# filename = filedialog.askopenfilename

class QA_data(): 
    def __init__(self, filepath):
        self.path = filepath  
        # self.files = glob.glob(path + "*.txt")
        self.final_json = {}      
        self.final_json['version'] = "v2.0"
        self.final_json['data'] = []
    
    def get_loc(self, answer, content):
        loc = re.search(answer.lower(), content.lower())
        if loc is None:
             return -1
        else:
             return loc.span()[0]
     
    def into_json(self):
        with open(self.path, 'r', encoding="utf8") as f:
            topics = f.read()
            for k, items in enumerate(topics.split("\n\n\n\n")):                
                d0 = {}
                d0['title'] = items.split("\n\n", 1)[0].replace("Title:", "").strip()
                d0['paragraphs'] = []

                for j, item in enumerate(items.split("\n\n", 1)[1].strip().split("\n\n\n",)):

                    # print(f'\n\n{self.path}\n{k}-{j} : {item}')
            
                    d1 = {}
                    d1['context'] = item.split("\n\n")[0].replace("Content:", "").strip()
                
                    d1['qas'] = []
                    for i, section in enumerate(item.split("\n\n")):
                        # print(f"i -> {i}\n")
                        #print(section)
                        if  i != 0:
                            d2 = {}
                            d2['question'] = section.split("\n")[0].strip().replace("Question:", "").strip()
                            ans = section.split("\n")[1].strip().replace("Answer:", "").strip()
                            print((100*k)+i)
                            d2['id'] = f"id_{k}_{j}_{i}"
                            loc = self.get_loc(ans, d1['context'])

                            d2['is_impossible'] = True if loc == -1 else False
                            if loc == -1:
                                d2['answers']= []
                            else:
                                d2['answers']= [{'answer_start': loc,"text":ans}]
                        
                            d1['qas'].append(d2)

                    d0['paragraphs'].append(d1)
                self.final_json['data'].append(d0) 
                
        return self.final_json       
        
                
    

if __name__ == "__main__":
    # path = filedialog.askopenfilename(title = "Select Text File")
    path = filedialog.askdirectory(title = "Select Directory")

    for file in sorted(files for files in os.listdir(path)):
        if file.endswith('.txt'):
            print(f"\nProcessing file : {file}")
            filepath =f"{path}/{file}"
            obj = QA_data(filepath)
            output_dict = obj.into_json()
            print(f"Processed file {file}")

            #with open(f"1/JSON_RESULTS/{file}.json", "w") as write_file:
            #Creating folder if not present
            outfolder = '../script2genSquad2'
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)
            with open(f"{outfolder}/{file}.json", "w") as write_file:
                print('Hi')
                json.dump(output_dict, write_file, indent=4)
        
    
