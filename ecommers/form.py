from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('product_name','product_desc','product_feature','product_rating','rate','selling_rate','stock_count','available','product_image1','product_image2','product_image3','category')

    