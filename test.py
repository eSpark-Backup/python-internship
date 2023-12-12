# import fitz  # PyMuPDF

# def extract_text_by_heading(pdf_path):
#     doc = fitz.open(pdf_path)

#     text_blocks = []

#     for page_num in range(doc.page_count):
#         page = doc[page_num]
#         blocks = page.get_text("blocks")
#         for b in blocks:
#             if 'experience' in b[4].lower():
#                 text = b[4]  # Text content
#                 fontsize = b[1]  # Font size

#             # # Assuming the heading is in a larger font size (adjust as needed)
#             # if fontsize > 12 and heading.lower() in text.lower():
#             #     text_blocks.append(text)

#     doc.close()
#     return text

# # Example usage
# pdf_path = "C:/Users/eSpark/Downloads/python_dev.pdf"
# heading = "Experience"  # Replace with your desired heading
# result = extract_text_by_heading(pdf_path)

# for text_block in result:
#     print(text_block)





# import fitz  # PyMuPDF
# import re

# def extract_dates_from_experience(pdf_path):
#     doc = fitz.open(pdf_path)
#     experience_dates = []

#     for page_num in range(doc.page_count):
#         page = doc[page_num]
#         blocks = page.get_text("blocks")

#         in_experience = False
#         for i, b in enumerate(blocks):
#             text = b[4]  # Text content

#             # Check for the presence of "EXPERIENCE" in the block text
#             if 'experience' in text.lower(): #and not in_experience:
#                 in_experience = True
#             elif in_experience:
#                 # Use a regular expression to find year patterns
#                 date_matches = re.findall(r'\b\d{4}\b', text)
#                 if date_matches!=[]:
#                     experience_dates.append(date_matches)
#                 # if date_matches!=[]:
#                     # experience_dates.append(b[4])
#     doc.close()
#     return experience_dates

# pdf_path = "C:/Users/eSpark/Downloads/cv2.pdf"
# result = extract_dates_from_experience(pdf_path)
# print(result)


# import fitz  # PyMuPDF
# import re


# def scrape(keyword, filePath):
#     results = []  # list of lists that store the information as [text, font size, font name, color, index]
#     pdf = fitz.open(filePath)  # filePath is a string that contains the path to the pdf
#     for page in pdf:
#         dict_info = page.get_text("dict")
#         blocks = dict_info["blocks"]

#         for block_num,block in enumerate(blocks):
#             if "lines" in block.keys():
#                 spans = block["lines"]                
#                 for span in spans:
#                     data = span["spans"]
#                     for line in data:
#                         if keyword in line["text"].lower():
#                             if len(line['text'])<=25:
#                                 results.append(
#                                     [line["text"], line["size"], line["font"], line["color"], (block_num)]
#                           )
            
#     new_res=[]
#     if len(results)>1:
#         for i in range(len(results)-1):
#             if results[i][1]==results[i+1][1]:
#                 new_res.append(results[i])
#             elif results[i][1]>results[i+1][1]:
#                 new_res.append(results[i])
#             else:
#                 continue
#     experience=''
#     if new_res:
#         index=new_res[0][-1]
#         size=new_res[0][1]
#         font=new_res[0][2]
#         color=new_res[0][3] 
#         out=0
#         for page in pdf:
#             dict_info = page.get_text("dict")
#             blocks = dict_info["blocks"]
            
#             for block_num in range(index,len(blocks)):
#                 block=blocks[block_num]
#                 if "lines" in block.keys():
#                     spans = block["lines"]                
#                     for span in spans:
#                         data = span["spans"]
#                         for line in data:
#                             if line['size']==size and line['font']==font and line['color']==color:
#                                 out+=1
#                                 break
#                             else:
#                                 experience+='\n'+line['text']
#                         if out>0:
#                             break

#     print(new_res)
#     print(experience)

#     # else:
#     #     print(results)
#     pdf.close()
    

# filePath="C:/Users/eSpark/Downloads/cv.pdf"
# scrape('experience', filePath)



# import datetime
# current_year = str(datetime.datetime.now().date())
# print(current_year)

# from yourapp.models import YourModel
# from datetime import datetime

# def delete_records_up_to_and_on_date(target_date):
#     # Assuming target_date is a string in the format 'YYYY-MM-DD'
#     target_date = datetime.strptime(target_date, '%Y-%m-%d')

#     # Get records to delete
#     records_to_delete = YourModel.objects.filter(your_date_field__lte=target_date)

#     # Delete the records
#     records_to_delete.delete()

# # Example usage
# delete_records_up_to_and_on_date('2023-01-01')