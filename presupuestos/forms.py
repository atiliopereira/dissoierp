from django import forms

from presupuestos.models import DetalleDeItem, Item, DetalleDePresupuesto, Presupuesto


class DetalleDeItemForm(forms.ModelForm):
    class Meta:
        model = DetalleDeItem
        fields = '__all__'
        widgets = {
            "cantidad": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    costo = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False, label="Costo")
    subtotal = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto subtotal_iterable', 'data-a-sep': '.',
               'data-a-dec': ','}), required=False, label="Subtotal")

    def __init__(self, *args, **kwargs):
        super(DetalleDeItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.initial['costo'] = instance.get_costo()
            self.initial['subtotal'] = instance.get_subtotal()
        else:
            self.initial['costo'] = 0.0
            self.initial['subtotal'] = 0.0


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            "coeficiente_cantidad": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ',', 'value': '1,00'}),
            "cantidad_unidades": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ',', 'value': '1,00'}),
            "precio_venta": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
            "costo_item": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    precio_unitario_venta = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False, )
    costo_unitario = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False)
    costo_total = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['costo_item'].widget.attrs['readonly'] = True
        self.fields['precio_unitario_venta'].widget.attrs['readonly'] = True
        self.fields['costo_total'].widget.attrs['readonly'] = True
        self.fields['costo_unitario'].widget.attrs['readonly'] = True
        if not self.instance.id:
            self.fields['costo_item'].initial = 0.0
            self.fields['precio_unitario_venta'].initial = 0.0
            self.fields['costo_total'].initial = 0.0
            self.fields['costo_unitario'].initial = 0.0
        else:
            self.fields['precio_unitario_venta'].initial = self.instance.get_precio_unitario_venta()
            self.fields['costo_total'].initial = self.instance.get_costo_total()
            self.fields['costo_unitario'].initial = self.instance.get_costo_unitario()


class DetalleDePresupuestoForm(forms.ModelForm):
    class Meta:
        model = DetalleDePresupuesto
        fields = '__all__'
        widgets = {
            "cantidad": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12',
                       'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
            "precio_unitario": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12',
                       'class': 'auto', 'data-a-sep': '.', 'data-a-dec': ','}),
            "subtotal": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto subtotal_iterable', 'data-a-sep': '.',
                       'data-a-dec': ','}
            )
        }

    def __init__(self, *args, **kwargs):
        super(DetalleDePresupuestoForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(detalledepresupuesto__isnull=True)
        self.fields['precio_unitario'].widget.attrs['readonly'] = True
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['cantidad'].widget.attrs['readonly'] = True

        if self.instance.pk:
            self.fields['item'].queryset = Item.objects.filter(
                detalledepresupuesto__presupuesto_id=self.instance.presupuesto_id)

        else:
            self.initial['precio_unitario'] = 0.0
            self.initial['subtotal'] = 0.0
            self.initial['cantidad'] = 1.0


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = '__all__'
        widgets = {
            "descuento": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}
            ),
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}
            )
        }
