from blog.models import Post
import pandas as pd
from mysite.models import Post
tmp_data=pd.read_csv('file.csv',sep=';')
#ensure fields are named~ID,Product_ID,Name,Ratio,Description
#concatenate name and Product_id to make a new field a la Dr.Dee's answer
products = [
    Post(
        name = tmp_data.ix[row]['Name'],
        description = tmp_data.ix[row]['Description'],
        price = tmp_data.ix[row]['price'],
    )
    for row in tmp_data['ID']
]
Post.objects.bulk_create(products)