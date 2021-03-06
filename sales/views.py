from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import salesSearchForm
import pandas as pd
from .utils import get_customer_name_from_id, get_salesman_name_from_id
# Create your views here.
def home_view(request):
    form = salesSearchForm(request.POST or None)
    sale_df = None
    pos_df = None
    merged_df = None
    m_df = None

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        
        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sale_df = pd.DataFrame(sale_qs.values())
            sale_df['customer_id'] = sale_df['customer_id'].apply(get_customer_name_from_id)
            sale_df['salesman_id'] = sale_df['salesman_id'].apply(get_salesman_name_from_id)
            sale_df['created'] = sale_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sale_df['updated'] = sale_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sale_df = sale_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1)
            
            print(sale_df)
            position_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    position_data.append(obj)
            pos_df = pd.DataFrame(position_data)
            merged_df = pd.merge(sale_df, pos_df, on='sales_id')
            m_df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

            pos_df = pos_df.to_html()
            merged_df = merged_df.to_html()
            sale_df = sale_df.to_html()
            m_df = m_df.to_html()
        
        else:
            print('No data')

    context = {
        'form': form,
        'sale_df': sale_df,
        'pos_df': pos_df,
        'merged_df': merged_df,
        'm_df': m_df,
    }
    return render(request, 'sales/home.html', context)


class SalesListView(ListView):
    model = Sale
    template_name = 'sales/main.html'


class SalesDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
