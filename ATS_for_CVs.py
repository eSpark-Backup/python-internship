from pdfminer.high_level import extract_text  #extract information from PDF documents to string
import os   # interact with the operating system, like creating files and directories, management of files and directories
import shutil   #automate process of copying and removal of files and directories.

def pdf_to_txt(cv):
        with open(cv, 'rb') as cv:
           text=extract_text(cv)
        return text

save_to='C:/Users/eSpark/Documents/GitHub/py_intern/python-internship/successfull_candidates'

if not os.path.exists(save_to):
    os.mkdir(save_to)

while True:
    try:
        cv_folder=input('Enter the path of CV folder: ')
        keywords=input('Enter 5 keywords separated by comma(,): ')
        keywords_list=keywords.split(',')
        for file in os.listdir(cv_folder):
            if file.endswith(".pdf") :
                file_path=os.path.join(cv_folder,file)
                text=pdf_to_txt(file_path)
            total_keywords=len(keywords_list)
            matched=0
            for keyword in keywords_list:
                if keyword.upper() in text.upper():
                    matched+=1
            success_percent=(matched/total_keywords)*100
            if success_percent>=50:
                output_file_path = os.path.join(save_to, file)
                shutil.copy(file_path, output_file_path)
                print(f"Saved {file} to the successful_candidates.")
            else:
                print(f"{file} Discarded!!")
        break
    except Exception as e:
        print("You have entered wrong folder path!!!")
        continue
    