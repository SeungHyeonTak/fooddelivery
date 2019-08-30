from allauth.account.forms import LoginFormfrom django import formsfrom django.template.loader import render_to_stringfrom django.utils.encoding import smart_textfrom django.utils.safestring import mark_safefrom django.conf import settingsfrom .models import *from .widgets import RateitjsWidgetimport jsonclass CustomLoginForm(LoginForm):    def __init__(self, *args, **kwargs):        super(CustomLoginForm, self).__init__(*args, **kwargs)        self.fields['login'].widget = forms.TextInput(            attrs={                'placeholder': '아이디를 입력해주세요111',                'class': 'form-control',            }        )        # self.fields['']class ReviewForm(forms.ModelForm):    class Meta:        model = Review        fields = ['rating', 'message', 'photo']        widgets = {            'rating': RateitjsWidget,        }class OrderForm(forms.ModelForm):    class Meta:        model = Order        fields = ['address', 'phone']        widget = {            'address': forms.TextInput(                attrs={                    'class': 'form-control',                    'placeholder': '주소를 입력하세요',                }            ),            'phone': forms.TextInput(                attrs={                    'class': 'form-control',                    'placeholder': '번호를 입력하세요'                }            )        }class PayForm(forms.ModelForm):    class Meta:        model = Order        fields = ('imp_uid',)    def as_iamport(self):        hidden_fields = mark_safe(''.join(smart_text(field) for field in self.hidden_fields()))        fields = {            'merchant_uid': str(self.instance.merchant_uid),            'name': self.instance.name,            'amount': self.instance.amount,        }        return hidden_fields + render_to_string('food/_iamport.html', {            'json_fields': mark_safe(json.dumps(fields, ensure_ascii=False)),            'iamport_shop_id': settings.IAMPORT_SHOP_ID,  # FIXME: 각자의 상점 아이디로 변경 가능        })    def save(self):        order = super().save(commit=False)        order.update()  # IAMPORT API 갱신        return order