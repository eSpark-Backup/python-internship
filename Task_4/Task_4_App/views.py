from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd


# Create your views here.
def home(request):
    if request.method == 'POST':
        if 'item_name' in request.POST:
            item_name = request.POST.get('item_name', '')
            return HttpResponseRedirect(reverse('result_item') + f'?item_name={item_name}')
        elif 'part_number' in request.POST:
            part_number = request.POST.get('part_number', '')
            return HttpResponseRedirect(reverse('result_part') + f'?part_number={part_number}')
    return render(request, 'index.html')


def result_item(request):
    query_item = request.POST.get('item_name','')

    excel_file="C:/Users/eSpark/Documents/Python_Tasks/Task_4/StockData 20-07-23.xlsx"
    df=pd.read_excel(excel_file)
    items=df['ItemName'].unique()
    result=[]
    item_list=[]
    for item in items:
        if query_item!='' and query_item in item:
            item_list.append(item)

    if len(item_list)==0:
        result=[0]
        item_list=['Not Available']

    else:
        for item in item_list:
            stock_item=df[df['ItemName']==item]
            result.append(stock_item['Stock'].sum())

    item_result_pairs = zip(item_list, result)

            
    return render(request,'result_item.html',{'item_view':item_result_pairs})


def result_part(request):
    query_part=request.POST.get('part_number','')

    excel_file="C:/Users/eSpark/Documents/Python_Tasks/Task_4/StockData 20-07-23.xlsx"
    df=pd.read_excel(excel_file)
    items=df['ManufacturerPartNo'].unique()

    if query_part in items:
        result_df=df[df['ManufacturerPartNo']==query_part]
        item_name=result_df['ItemName'].to_list()
        result_item=item_name[0]
        print()
        result_quantity=result_df['Stock'].sum()

    else:
        query_part='Not Available'
        result_item='Not Available'
        result_quantity=0

    return render(request,'result_part.html',{'query_part': query_part,'result_item':result_item, 'result_quantity': result_quantity})
    