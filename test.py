# <!DOCTYPE html>
# <html lang="en">

# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
#         integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
#     <title>eSpark Portal</title>
#     <style>
#         body {
#             background: linear-gradient(rgb(255, 255, 255), rgba(98, 184, 199, 0.466));
#             background-size: cover;
#             background-repeat: repeat;
#             background-attachment: fixed;
#         }

#         #bodies {
#             margin: 30px;
#         }

#         #main-blue {
#             background-color: #01496D;
#             height: 20px;
#         }

#         #logo {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#             margin-top: 10px;
#             margin-bottom: 10px;
#         }

#         #portal {
#             font-size: 50px;
#             font-weight: bold;
#             font-family: serif;
#             color: #009faa;
#         }

#         #no-logs a {
#             text-decoration: none;
#         }

#         #no-logs a p {
#             text-align: right;
#             font-size: 25px;
#             font-family: sans-serif;
#             color: #00B0B4;
#         }

#         #no-logs a:hover p {
#             text-align: right;
#             font-size: 25px;
#             font-family: sans-serif;
#             color: #008688;
#         }

#         #inputs {
#             background-color: #00A0A0;
#             width: 40%;
#             margin: auto;
#             margin-top: 85px;
#             padding-top: 2%;
#             padding-bottom: 2%;
#             margin-bottom: 7.4%;
#         }

#         #inputs h2 {
#             text-align: center;
#             color: #ffffff;
#             font-weight: bold;
#             font-family: serif;
#             font-size: 40px;
#         }

#         #choose-perc {
#             display: flexbox;
#             justify-items: center;
#             text-align: center;
#             margin-top: 2%;
#         }

#         #files {
#             outline: none;
#             display: inline-block;
#             width: 300px;
#             padding: 2px;
#             color: #ffffff;
#             font-size: 20px;
#             border-radius: 5px;
#             text-align: center;
#         }


#         #files::file-selector-button {
#             outline: none;
#             background-color: #00478ab7;
#             color: #ffffff;
#             padding: 5px;
#             border-radius: 5px;
#             text-align: center;
#             border: none;
#         }

#         #percent {
#             display: inline-block;
#             width: 195px;
#             margin-top: 5px;
#             margin-bottom: 5px;
#             padding: 3px;
#             outline: none;
#             border: none;
#             background-color: #ffffff7a;
#             color: #ffffff;
#             font-size: 18px;
#             font-weight: 450;
#         }

#         .keyword {
#             display: block;
#             width: 500px;
#             margin: auto;
#             margin-top: 5px;
#             margin-bottom: 5px;
#             padding: 3px;
#             outline: none;
#             border: none;
#             background-color: #ffffff7a;
#             color: #ffffff;
#             font-size: 18px;
#             font-weight: 450;
#         }

#         #submit {
#             outline: none;
#             display: block;
#             margin: auto;
#             margin-bottom: 2%;
#             padding: 3px;
#             background: #0158aa;
#             border: none;
#             color: #ffffff;
#             font-size: 20px;
#             width: 150px;
#             border-radius: 10px;
#         }

#         #footer {
#             width: 100%;
#         }

#         #greens {
#             padding: 3px;
#             background-color: #00B0B4;
#         }

#         #greys {
#             padding: 3px;
#             background-color: #B5B5B5;
#         }

#         #blues {
#             padding: 15px;
#             background-color: #01496D;
#         }

#         #error {
#             margin: auto;
#             width: 100%;
#             text-align: center;
#             margin-top: 2%;
#         }

#         .alert {
#             padding: 3px;
#             width: 40%;
#             margin: auto;
#             margin-bottom: 10px
#         }

#         #add-row {
#             padding-top: 0;
#             padding-bottom: 0;
#             outline: none;
#             margin-left: 16.5%;
#             background-color: #0158aa;
#             color: #ffffff;
#             border: #0158aa;
#             font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
#             font-size: 17px;
#             margin-top: 2px;
#         }
#     </style>

# </head>

# <body>
#     <div id="bodies">

#         <div id="heading">
#             <div id="main-blue">
#             </div>

#             <div id="logo">

#                 <span id="logo-img">
#                     <img src="/static/es_logo.png" alt="">
#                 </span>

#                 <div id="portal">
#                     eSpark Portal
#                 </div>

#                 <div id="no-logs">
#                     <a href="/logout">
#                         <p><b>Logout</b></p>
#                     </a>
#                 </div>

#             </div>

#             <div id="main-blue">
#             </div>
#         </div>


#         <div id="inputs">

#             <h2>
#                 ATS System
#             </h2>
#             <form id="folderForm" enctype="multipart/form-data" method="post">
#                 {% csrf_token %}
#                 <div id="choose-perc">
#                     <input type="file" name="files" webkitdirectory directory multiple id="files" required>
#                     <input type="number" name="percent" id="percent" placeholder="Matching criteria %" min="50"
#                         max="100" step="10" required value="{{inpu_values.percent}}">
#                 </div>
#                 <input type="text" name="keywords[]" class="keyword" placeholder="Enter keyword" required
#                     autocomplete="off">
#                 <input type="text" name="keywords[]" class="keyword" placeholder="Enter keyword" required
#                     autocomplete="off">
#                 <input type="text" name="keywords[]" class="keyword" placeholder="Enter keyword" required
#                     autocomplete="off">
#                 <input type="text" name="keywords[]" class="keyword" placeholder="Enter keyword" required
#                     autocomplete="off">
#                 <input type="text" name="keywords[]" class="keyword" placeholder="Enter keyword" required
#                     autocomplete="off" id="dynamic-sample">
#                 <button type="button" id="add-row"> + </button>
#                 <div id="error">
#                     {% if error_message %}
#                     <div class="alert alert-danger" role="alert">{{ error_message }}</div>
#                     {% endif %}
#                 </div>
#                 <input type="submit" value="Submit" id="submit">
#             </form>
#         </div>

#         <div id="footer">
#             <div id="greens"></div>
#             <div id="greys"></div>
#             <div id="blues"></div>
#         </div>
#     </div>

#     <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
#         integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
#         crossorigin="anonymous"></script>

#     <script>

#         // Function to add a new row
#         function addRow() {
#             const template = $('#dynamic-sample').clone();
#             template.removeAttr('id').show();
#             template.val('');

#             $('#folderForm input[type="text"]:last').after(template);
#             attachEventListenersToDynamicRows();
#         }

#         $(document).ready(function () {
            # $('#folderForm').on('submit', function (event) {
            #     event.preventDefault(); // Prevent the default form submission

            #     // Get the CSRF token from the form
            #     var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

            #     // Perform an AJAX request to submit the form data
            #     $.ajax({
            #         url: '/ats_system/',
            #         type: 'POST',
            #         data: new FormData(this),
            #         processData: false,
            #         contentType: false,
            #         headers: {
            #             'X-CSRFToken': csrf_token
            #         },
            #         dataType: 'json',
            #         success: function (data) {
            #             // Handle the JSON response
            #             $('#error').html('<div class="alert alert-danger" role="alert">' + data.error_message + '</div>');
            #         }
            #     });
            # });


#             $('#add-row').click(function () {
#                 addRow();
#             });
#         });

#     </script>


# </body>

# </html>




# @login_adminorhr_successfull
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def ats_system(request):
#     if request.method == 'POST':
#         files = request.FILES.getlist('files')
#         keywords_list = request.POST.getlist('keywords[]')
#         percentage=int(request.POST['percent'])
#         pdfs=0
#         matching_files = []
        
#         for file in files:
#             try:
#                 file_data = file.read()

#                 # Convert byte data to a file-like object
#                 file_like_object = BytesIO(file_data)

#                 # Extract text from the file-like object
#                 text = extract_text(file_like_object)
                
#                 # calculating the percentage of matched words
#                 total_keywords = len(keywords_list)
#                 matched = 0
#                 for keyword in keywords_list:
#                     if keyword.upper() in text.upper():
#                         matched += 1
#                 success_percent = (matched / total_keywords) * 100

#                 if success_percent >= percentage:
#                     matching_files.append((file.name, file_data))
#                 pdfs+=1
#             except:
#                 continue
#         if matching_files:
#             print('in matching files')
#             # Create a ZIP file containing all matching files
#             zip_buffer = BytesIO()
#             with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
#                 for filename, file_data in matching_files:
#                     zip_file.writestr(filename, file_data)
            
#             print('generating respoinse')
#             # Set response headers for the ZIP file
#             response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
#             response['Content-Disposition'] = 'attachment; filename=shortlisted_candidates.zip'
#             return response
#         elif pdfs>0:
#            return JsonResponse({'error_message': f'No file matches {percentage}% of the keywords.'})
#         else:
#             return JsonResponse({'error_message': 'Folder does not contain pdf files.'})
            
#     return render(request, 'ats_sys.html')