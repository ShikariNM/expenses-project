from django import forms

from .models import Category, Expense, Receipt


class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'usefulness', 'color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Enter title'}),
            'usefulness': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control-color',
                                            'type': 'color'})
        }


class PostExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'category', 'cost']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class PostReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['title', 'purchase_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Enter title'}),
            'purchase_time': forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                        'class': 'form-control'})
        }


class DateFromToForm(forms.Form):
    date_from = forms.DateTimeField(label='From', widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                                                    'class': 'form-control'}))
    date_to = forms.DateTimeField(label='To', widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                                                'class': 'form-control'}))
