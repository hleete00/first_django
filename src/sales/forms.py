from django import forms


# Make list of lists to hold possible choices for users.
CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)

RESULT_CHOICES = (
    ('#1', 'transaction'),
    ('#2', 'sales date'),
)
# Create form class to be called from sales/views.py and to take user search input
class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)