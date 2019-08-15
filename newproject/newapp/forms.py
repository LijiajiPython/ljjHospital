from django import forms
# from captcha.fields import CaptchaField
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    BIRTH_YEAR_CHOICES = (
        '1970','1971','1972','1973','1974','1975','1976','1977','1978','1979',
        '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
        '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
        '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
        '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019')
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="密码", max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    # captcha = CaptchaField(label='验证码')

    tel = forms.CharField(label="电话",max_length=11,widget=forms.TextInput(attrs={'class':'form-control'}))
    birth = forms.DateField(label="出生日期", widget=forms.SelectDateWidget(years=list(BIRTH_YEAR_CHOICES)))
    address = forms.CharField(label="地址",max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))