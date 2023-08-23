from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests


def home(request): 
    if request.method=='POST':
        return HttpResponseRedirect('tables.html')
    return render(request, 'home.html')

def tables(request):
    # return render(request, 'tables.html')
    api_url = 'https://api.carbonintensity.org.uk/regional/postcode/HG1'
    
    # Send GET request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        api_data = response.json()
        # Extract the relevant data from the JSON structure for table 1
        dict_table_1={}
        for i in api_data['data'][0]:
            if i!='data':
                dict_table_1.update({i:api_data['data'][0][i]})

        # Extract the relevant data from the JSON structure for table 2
        dict_table_2={}
        for i in api_data['data'][0]['data'][0]['generationmix']:
            dict_table_2.update({i['fuel']:i['perc']})
        
    else:
        # Handle the case when the API request fails
        data = []

    return render(request, 'tables.html', {'table_1': dict_table_1,'table_2': dict_table_2 })
