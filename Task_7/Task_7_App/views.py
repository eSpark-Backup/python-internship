from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .decorators import login_user_successfull,login_admin_successfull
from django.views.decorators.cache import cache_control
import pandas as pd


excel_file="C:/Users/eSpark/Documents/Python_Tasks/Tasks/Task_7/StockData 20-07-23.xlsx"



# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'eSparkAdmin' and password == 'admin@espark':
            request.session['role'] = 'admin'
            return redirect("home_admin")

        elif username == 'eSparkUser' and password == 'user@espark':
            request.session['role'] = 'user'
            return redirect("home")

        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    response = render(request, 'login.html')
    # Add Cache-Control header to prevent caching
    response['Cache-Control'] = 'no-store, must-revalidate'

    return response





@login_user_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

    df=pd.read_excel(excel_file)

    result=[]
    item_list=[]
    part_no = []

    query_elements=query_item.split()

    if len(query_elements)==1 or len(query_elements)==0:
        for index, row in df.iterrows():
            new_row=row['ItemName'].split()
            for item in new_row:
                if query_item!='' and query_item.lower() == item.lower() :
                    item_list.append(row['ItemName'])
                    result.append(row['Stock'])
                    part_no.append(row['ManufacturerPartNo'])
    else:
        for index, row in df.iterrows():
            it_check=0
            new_row=row['ItemName'].split()
            if len(query_elements)<len(new_row):
                for i in range(len(query_elements)):
                    if query_elements[i].lower()==new_row[i].lower():
                        it_check+=1

            else:
                for i in range(len(new_row)):
                    if query_elements[i].lower()==new_row[i].lower():
                        it_check+=1
            if len(query_elements)==it_check:
                    item_list.append(row['ItemName'])
                    result.append(row['Stock'])
                    part_no.append(row['ManufacturerPartNo'])


    if len(item_list)==0:
        result=[0]
        item_list=['Not Available']
        part_no=['Not Available']

    item_result_pairs = zip(part_no,item_list, result)

            
    return render(request,'result_item.html',{'item_view':item_result_pairs})





def result_part(request):
    query_part=request.POST.get('part_number','')


    df=pd.read_excel(excel_file)
    items=df['ManufacturerPartNo'].unique()

    if query_part in items:
        result_df=df[df['ManufacturerPartNo']==query_part]
        item_name=result_df['ItemName'].to_list()
        result_item=item_name[0]
        result_quantity=result_df['Stock'].sum()

    else:
        query_part='Not Available'
        result_item='Not Available'
        result_quantity=0

    return render(request,'result_part.html',{'query_part': query_part,'result_item':result_item, 'result_quantity': result_quantity})





@login_admin_successfull
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_admin(request):
    if request.method == 'POST':
        if 'item_name' in request.POST:
            item_name = request.POST.get('item_name', '')
            return HttpResponseRedirect(reverse('admin_result_item') + f'?item_name={item_name}')
        elif 'part_number' in request.POST:
            part_number = request.POST.get('part_number', '')
            return HttpResponseRedirect(reverse('admin_result_part') + f'?part_number={part_number}')
    return render(request, 'index_admin.html')


    

@login_admin_successfull
def admin_result_item(request):

    query_item = request.POST.get('item_name','')

    df=pd.read_excel(excel_file)

    result=[]
    item_list=[]
    part_no = []
    input_query=[]

    query_elements=query_item.split()

    if len(query_elements)==1 or len(query_elements)==0:
        for index, row in df.iterrows():
            new_row=row['ItemName'].split()
            for item in new_row:
                if query_item!='' and query_item.lower() == item.lower() :
                    input_query.append(query_item)
                    item_list.append(row['ItemName'])
                    result.append(row['Stock'])
                    part_no.append(row['ManufacturerPartNo'])
    else:
        for index, row in df.iterrows():
            it_check=0
            new_row=row['ItemName'].split()
            if len(query_elements)<len(new_row):
                for i in range(len(query_elements)):
                    if query_elements[i].lower()==new_row[i].lower():
                        it_check+=1

            else:
                for i in range(len(new_row)):
                    if query_elements[i].lower()==new_row[i].lower():
                        it_check+=1
            if len(query_elements)==it_check:
                    input_query.append(query_item)
                    item_list.append(row['ItemName'])
                    result.append(row['Stock'])
                    part_no.append(row['ManufacturerPartNo'])


    if len(item_list)==0:
        input_query=[query_item]
        result=[0]
        item_list=['Not Available']
        part_no=['Not Available']

    item_result_pairs = zip(input_query,part_no,item_list, result)

    #delete button implementation starts
    if request.method=='POST':
        if 'delete' in request.POST:
            query_item=request.POST.get('query_item')
            del_item=request.POST.get('del_part')

            for index, row in df.iterrows():
                if del_item==row['ManufacturerPartNo']:
                    df.drop(index,inplace=True)

            df.reset_index(drop=True, inplace=True)

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

            result=[]
            item_list=[]
            part_no = []
            input_query=[]

            query_elements=query_item.split()

            if len(query_elements)==1 or len(query_elements)==0:
                for index, row in df.iterrows():
                    new_row=row['ItemName'].split()
                    for item in new_row:
                        if query_item!='' and query_item.lower() == item.lower() :
                            input_query.append(query_item)
                            item_list.append(row['ItemName'])
                            result.append(row['Stock'])
                            part_no.append(row['ManufacturerPartNo'])
            else:
                for index, row in df.iterrows():
                    it_check=0
                    new_row=row['ItemName'].split()
                    if len(query_elements)<len(new_row):
                        for i in range(len(query_elements)):
                            if query_elements[i].lower()==new_row[i].lower():
                                it_check+=1

                    else:
                        for i in range(len(new_row)):
                            if query_elements[i].lower()==new_row[i].lower():
                                it_check+=1
                    if len(query_elements)==it_check:
                            input_query.append(query_item)
                            item_list.append(row['ItemName'])
                            result.append(row['Stock'])
                            part_no.append(row['ManufacturerPartNo'])


            if len(item_list)==0:
                input_query=[query_item]
                result=[0]
                item_list=['Not Available']
                part_no=['Not Available']

            item_result_pairs = zip(input_query,part_no,item_list, result)
    #delete button implementation completed


    
        elif 'edit' in request.POST:
            query_item=request.POST.get('query_item')
            edit_item=request.POST.get('edit_part')
            new_quantity=request.POST.get('new_quantity')

            for index, row in df.iterrows():
                if edit_item==row['ManufacturerPartNo']:
                    df.at[index, 'Stock']=new_quantity

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            
            result=[]
            item_list=[]
            part_no = []
            input_query=[]

            query_elements=query_item.split()

            if len(query_elements)==1 or len(query_elements)==0:
                for index, row in df.iterrows():
                    new_row=row['ItemName'].split()
                    for item in new_row:
                        if query_item!='' and query_item.lower() == item.lower() :
                            input_query.append(query_item)
                            item_list.append(row['ItemName'])
                            result.append(row['Stock'])
                            part_no.append(row['ManufacturerPartNo'])
            else:
                for index, row in df.iterrows():
                    it_check=0
                    new_row=row['ItemName'].split()
                    if len(query_elements)<len(new_row):
                        for i in range(len(query_elements)):
                            if query_elements[i].lower()==new_row[i].lower():
                                it_check+=1

                    else:
                        for i in range(len(new_row)):
                            if query_elements[i].lower()==new_row[i].lower():
                                it_check+=1
                    if len(query_elements)==it_check:
                            input_query.append(query_item)
                            item_list.append(row['ItemName'])
                            result.append(row['Stock'])
                            part_no.append(row['ManufacturerPartNo'])


            if len(item_list)==0:
                input_query=[query_item]
                result=[0]
                item_list=['Not Available']
                part_no=['Not Available']

            item_result_pairs = zip(input_query,part_no,item_list, result)


    return render(request,'admin_result_item.html',{'item_view':item_result_pairs})



@login_admin_successfull
def admin_result_part(request):
    query_part=request.POST.get('part_number','')
    
    df=pd.read_excel(excel_file)
    items=df['ManufacturerPartNo'].unique()

    if query_part in items:
        result_df=df[df['ManufacturerPartNo']==query_part]
        item_name=result_df['ItemName'].to_list()
        result_item=item_name[0]
        result_quantity=result_df['Stock'].sum()

    else:
        query_part='Not Available'
        result_item='Not Available'
        result_quantity=0

    if request.method == 'POST':
        if 'delete' in request.POST:
            del_part = request.POST.get('del_part')

            mask = df['ManufacturerPartNo'] == del_part

            df = df[~mask]

            df.reset_index(drop=True, inplace=True)

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

            query_part='Not Available'
            result_item='Not Available'
            result_quantity=0

            return render(request,'admin_result_part.html',{'query_part': query_part,'result_item':result_item, 'result_quantity': result_quantity})

        elif 'edit' in request.POST:
            edit_part=request.POST.get('edit_part')
            new_quant=request.POST.get('new_quantity')

            for index, row in df.iterrows():
                if edit_part==row['ManufacturerPartNo']:
                    df.at[index, 'Stock']=new_quant

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

            items=df['ManufacturerPartNo'].unique()

            if edit_part in items:
                result_df=df[df['ManufacturerPartNo']==edit_part]
                item_name=result_df['ItemName'].to_list()
                result_item=item_name[0]
                result_quantity=result_df['Stock'].sum()

            return render(request,'admin_result_part.html',{'query_part': edit_part,'result_item':result_item, 'result_quantity': result_quantity})


    return render(request,'admin_result_part.html',{'query_part': query_part,'result_item':result_item, 'result_quantity': result_quantity}) 





@login_admin_successfull
def update_stock(request):
    if request.method=='POST':
        Catergory=request.POST['Category']
        CatergoryUrl=request.POST['CategoryUrl']
        CatergoryDesc=request.POST['CategoryDesc']
        SubCategory=request.POST['SubCategory']
        SubCategoryUrl=request.POST['SubCategoryUrl']
        SubCategoryDesc=request.POST['SubCategoryDesc']
        ManufacturerPartNo=request.POST['ManufacturerPartNo']
        Manufacturer=request.POST['Manufacturer']
        ItemName=request.POST['ItemName']
        Description=request.POST['Description']
        Stock=request.POST['Stock']
        Price=request.POST['Price']
        Packaging=request.POST['Packaging']
        Series=request.POST['Series']
        DatasheetUrl=request.POST['DatasheetUrl']
        ImageUrls=request.POST['ImageUrls']
        Mounting_Type=request.POST['Mounting Type']
        Package_Case=request.POST['Package Case']
        AdditionalFields=request.POST['AdditionalFields']

        df=pd.read_excel(excel_file)
        column=df.columns.to_list()

        list_ins=[Catergory,CatergoryUrl,CatergoryDesc,SubCategory,SubCategoryUrl,SubCategoryDesc,ManufacturerPartNo,Manufacturer,ItemName,Description,Stock,Price,Packaging,Series,DatasheetUrl,ImageUrls,Mounting_Type,Package_Case,AdditionalFields]

        match_found=0
        for index,row in df.iterrows():
            if ManufacturerPartNo==row['ManufacturerPartNo']:
                match_found=1

        if match_found==1:
            return render(request, 'update_stock.html', {'error_message': 'Item is already in inventory'})

        else:
            new_data = pd.Series(list_ins, index=column)
            df = pd.concat([df, new_data.to_frame().T], ignore_index=True)

            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False, header=True)

            return redirect('home_admin')
        
    return render(request, 'update_stock.html')






def logout(request):

    if 'role' in request.session:
        del request.session['role']
    
    return redirect('login')