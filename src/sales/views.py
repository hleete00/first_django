from inspect import getcallargs
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
# Import pandas for use of Data Frames
import pandas as pd
# Import methods from sales/utils.py
from .utils import get_customer_from_id, get_salesman_from_id, get_chart, get_graph


# Create views to be called from the sales/urls.py file
@login_required
def home_view(request):
    # Create data frames from pandas.
    sales_df = None
    positions_df = None
    merged_df = None
    df = None

    chart = None

    no_data = None

    # Create a data input form for user to input search parameters and chart type
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    # When user presses search button, get input from form and populate data frames.
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        # Create Sales querySet from search values
        qs = Sale.objects.filter(
            created__date__lte=date_to, created__date__gte=date_from)

        # If the Sales querySet has any records, continue with populating data frames.
        if len(qs) > 0:

            # Populate the sales data frame with the Sales querySet.
            sales_df = pd.DataFrame(qs.values())

            # Take the id of the customer and salesman, use them to get name of customer and salesman from methods in sales/utils.py
            sales_df['customer_id'] = sales_df['customer_id'].apply(
                get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(
                get_salesman_from_id)

            # Format the created and updated dates to be more user friendly to read
            sales_df['created'] = sales_df['created'].apply(
                lambda x: x.strftime('%m-%d-%Y'))
            sales_df['updated'] = sales_df['updated'].apply(
                lambda x: x.strftime('%m-%d-%Y'))

            # Rename fields in the sales data frame
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman',
                            'id': 'sales_id'}, axis=1, inplace=True)

            # Create list to hold positions data from each sale.
            positions_data = []

            # Loop through each sale in the Sales querySet and add each position to the positions_data list.
            for sale in qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)

            # Populate positions data frame with the positions_data list.
            positions_df = pd.DataFrame(positions_data)

            # Merge the sales and positions data frames on the sales_id value in both of them.
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            # Run a group by on the merged data frame to get the total sale price on one line. Convert all data frames to html
            df = merged_df.groupby('transaction_id', as_index=False)[
                'price'].aggregate('sum')
            chart = get_chart(chart_type, sales_df, results_by)
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

        # Return no data if search terms didn't have any Sales.
        else:
            no_data = 'No data is available'

    # Create dictionary of all the things that will be sent to the sales/home.html file
    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'no_data': no_data,
    }

    # Call the sales/home.html file and send it the context dictionary
    return render(request, 'sales/home.html', context)

# List view to show all sales.


class SaleListView(LoginRequiredMixin, ListView):
    # Get all the sales and call the sales/main.html file
    model = Sale
    template_name = 'sales/main.html'


# Detail view to show more detailed information about one sale
class SaleDetailView(LoginRequiredMixin, DetailView):
    # Get the Sale that corresponds to the primary key that was passed and open the sales/details.html file
    model = Sale
    template_name = 'sales/detail.html'
