# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:22:50 2021

@author: dung.pham
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import xlwt
from xlwt import Workbook 
import json 
from json import JSONEncoder

#initialize chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

#create driver
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Users/dung.pham/Downloads/chromedriver.exe")



class Essay:
    def __init__(self, essay_topic, extra_topic, model_answer, original_link):
        self.essay_topic = essay_topic 
        self.extra_topic = extra_topic
        self.model_answer = model_answer
        self.original_link = original_link 
    
def replace_junk_text(model_answer):
    if model_answer:
        target_list = ["Sample Answer:", "Model Answer:", "Model Essay", "Model Essay",
                  "Sample Answer 1:", "Model Answer 1:", "Model Essay 1:", "Model Essay 1:",
                  "What is your view on this?",
                  "Give reasons and relevant examples for your answer.",
                  "You should write at least 250 words.",
                  "Give reasons for your answer and include any relevant examples from your own knowledge or experience.",
                  ]
        for tar in target_list:
            model_answer = model_answer.replace(tar, "")
        
    return model_answer

def find_model_answer(driver, target_tag_name, answer_tag_name):
    
    target = ["sample answer", "model answer", "sample essay", "model essay"]
    article_element = driver.find_element_by_tag_name(target_tag_name)
    
    p_elements = article_element.find_elements_by_tag_name(answer_tag_name)
    
    for p_index, p_ele in enumerate(p_elements):
        
        #Check if p_ele contains target
        res = [tar for tar in target if(tar in p_ele.text.lower())]
        
        #Return the model answer 
        if res: 
            if p_index < len(p_elements) - 1:
                return p_ele.text +  p_elements[p_index+1].text
            else:
                return p_ele.text
    
    #Extra Retrieve if no p element is found 
    div_elements = article_element.find_elements_by_tag_name("div")
    
    for div_index, div_ele in enumerate(div_elements):
        
        #Check if p_ele contains target
        res = [tar for tar in target if(tar in div_ele.text.lower())]
        
        #Return the model answer 
        if res:
            return div_ele.text

def extract_to_excel(essay_list, filename="exported essay data.xls"):
    wb = Workbook()
    sheet = wb.add_sheet("Essay Data")
    
    #Title
    sheet.write(0,0, "ID")
    sheet.write(0,1, "Original Link")
    sheet.write(0,2, "Topic")
    sheet.write(0,3, "Extra Topic")
    sheet.write(0,4, "Model Answer")
    
    #Write essay to each row 
    for essay_index, essay in enumerate(essay_list):
        sheet.write(essay_index + 1, 0, essay_index + 1)
        sheet.write(essay_index + 1, 1, essay.original_link)
        sheet.write(essay_index + 1, 2, essay.essay_topic)
        sheet.write(essay_index + 1, 3, essay.extra_topic)
        sheet.write(essay_index + 1, 4, essay.model_answer)
    
    wb.save(filename)

class CustomEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
        
def extract_to_json(essay_list, essay_type):
    json_object = {
            "total": len(essay_list),
            "type": essay_type, 
            "essays": essay_list
        }
    jsonString = json.dumps(json_object, cls=CustomEncoder)
    jsonFile = open("exported_essay_data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    

url = "https://www.ielts-mentor.com/writing-sample/"
url_type = "writing-task-2/"

page_url = "?start="
step = 20 

total_pages = 62 


driver.get(url + url_type)

essay_links = []
essays = []

#Retrieve all essay links
for page_index in range(total_pages):

    if page_index  > 0:
        driver.get(url + url_type + page_url + str(step*page_index))
    
    essay_elements = driver.find_element_by_class_name("category").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    
    for essay_element in essay_elements:
        essay_links.append(essay_element.find_element_by_tag_name("a").get_attribute("href"))
    


for essay_index, essay_link in enumerate(essay_links):
    
    
    driver.get(essay_link)
    h3_elements = driver.find_elements_by_tag_name("h3")
    essay_topic = h3_elements[4].text
    
    #Extra title 
    extra_topic = ""
    if len(h3_elements) > 11:
        extra_topic = h3_elements[5].text
    
    try:
        h4_element = driver.find_element_by_tag_name("h4")
        extra_topic = h4_element.text
    except:
        pass
        
    
    #Model Answer
    model_answer = find_model_answer(driver, "article", "p")
    model_answer = replace_junk_text(model_answer)
    
    #print retrieved essay 
    print("-----------------------------------------")
    print("ID: ", essay_index)
    #print("Topic:\n", essay_topic)
    #print("Model Answer:\n", model_answer)
    #print("-----------------------------------------")
    
    #Store the essay in list 
    essays.append(Essay(essay_topic, extra_topic, model_answer, essay_link))
    
    
extract_to_excel(essays)
extract_to_json(essays, "Writing Task 2")