import jsonfrom django import formsfrom django.conf import settingsfrom django.template.loader import render_to_stringfrom django.utils.encoding import smart_textfrom django.utils.safestring import mark_safefrom .models import Review, Orderfrom allauth.account.forms import LoginForm, SignupFormclass CustomSignupForm(SignupForm):    def __init__(self, *args, **kwargs):        super(CustomSignupForm, self).__init__(*args, **kwargs)        self.fields['username'].widget = forms.TextInput(attrs={            'type': 'text',            'placeholder': 'username',            'class': 'form-control',        })        self.fields['email'].widget = forms.TextInput(attrs={            'type': 'text',            'placeholder': 'e-mail',            'class': 'form-control',        })        self.fields['password1'].widget = forms.TextInput(attrs={            'type': 'text',            'placeholder': 'password',            'class': 'form-control',        })        self.fields['password2'].widget = forms.TextInput(attrs={            'type': 'text',            'placeholder': 'password',            'class': 'form-control',        })class CustomLoginForm(LoginForm):    def __init__(self, *args, **kwargs):        super(CustomLoginForm, self).__init__(*args, **kwargs)        self.fields['login'].widget = forms.TextInput(attrs={            'type': 'text',            'placeholder': 'username',            'class': 'form-control',        })        self.fields['password'].widget = forms.TextInput(attrs={            'type': 'password',            'placeholder': 'password',            'class': 'form-control',        })class ReviewForm(forms.ModelForm):    class Meta:        model = Review        fields = ['rating', 'message', 'photo']class OrderForm(forms.ModelForm):    class Meta:        model = Order        fields = ['address', 'phone']class PayForm(forms.ModelForm):    class Meta:        model = Order        fields = ('imp_uid',)    def as_iamport(self):        # 본 Form의 Hidden 필드 위젯        hidden_fields = mark_safe(''.join(smart_text(field) for field in self.hidden_fields()))        # IMP.request_pay의 인자로 넘길 인자 목록        fields = {            'merchant_uid': str(self.instance.merchant_uid),            'name': self.instance.name,            'amount': self.instance.amount,        }        return hidden_fields + render_to_string('food/_iamport.html', {            'json_fields': mark_safe(json.dumps(fields, ensure_ascii=False)),            'iamport_shop_id': settings.IAMPORT_SHOP_ID,  # FIXME: 각자의 상점 아이디로 변경 가능        })    def save(self):        order = super().save(commit=False)        order.update()  # IAMPORT API를 통한 갱신        return order