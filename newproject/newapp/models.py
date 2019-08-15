from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import time
# Create your models here.
class User(models.Model):
    uname = models.CharField(u'用户名',max_length=20,unique=True)
    upasswd = models.CharField(u'密码',max_length=150)
    ugender = models.CharField(u'性别',max_length=32, choices=(('male', '男'),('female', '女')), default='男')
    ubirth = models.CharField(u'出生日期',max_length=20)
    uaddress = models.CharField(u'地址',max_length=20)
    utel = models.CharField(u'电话',max_length=11,unique=True)
    uemail = models.EmailField(u'邮箱',unique=True)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    class Meta:
        verbose_name_plural='用户信息'
    def __str__(self):
        return self.uname
class Doctor(models.Model):
    dname = models.CharField(u'用户名',max_length=20)
    dpasswd = models.CharField(u'密码',max_length=150)
    dgender = models.CharField(u'性别',max_length=32, choices=(('male', '男'),('female', '女')), default='男')
    dbirth = models.DateField(u'出生日期')
    dlevel = models.CharField(u'级别',max_length=32, choices=(('1', '医师'),('2', '主治医师'),('3', '副主任医师'),('4', '主任医师')), default='医师')
    dphoto = models.ImageField(u'照片',max_length=150,upload_to='static/img')
    dtel = models.CharField(u'电话',max_length=11,unique=True)
    demail = models.CharField(u'邮箱',max_length=20,unique=True)
    dtext = models.TextField(u'医生介绍',max_length=5000)
    isdelete = models.BooleanField(u'是否删除',default=False)
    rid = models.ForeignKey(to="Room",on_delete=models.CASCADE)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    class Meta:
        verbose_name_plural='医生信息'
    def __str__(self):
        return self.dname
class Room(models.Model):
    rname = models.CharField(u'科室名',max_length=20)
    rtext = models.TextField(u'科室介绍', max_length=5000)
    rtel = models.CharField(u'电话',max_length=20,unique=True)
    mon1 = models.CharField(u'周一上午',max_length=20,null=True,blank=True)
    mon2 = models.CharField(u'周一下午',max_length=20, null=True, blank=True)
    tue1 = models.CharField(u'周二上午',max_length=20, null=True, blank=True)
    tue2 = models.CharField(u'周二下午',max_length=20, null=True, blank=True)
    wed1 = models.CharField(u'周三上午',max_length=20, null=True, blank=True)
    wed2 = models.CharField(u'周三下午',max_length=20, null=True, blank=True)
    thu1 = models.CharField(u'周四上午',max_length=20, null=True, blank=True)
    thu2 = models.CharField(u'周四下午',max_length=20, null=True, blank=True)
    fri1 = models.CharField(u'周五上午',max_length=20, null=True, blank=True)
    fri2 = models.CharField(u'周五下午',max_length=20, null=True, blank=True)
    sat1 = models.CharField(u'周六上午',max_length=20, null=True, blank=True)
    sat2 = models.CharField(u'周六下午',max_length=20, null=True, blank=True)
    sun1 = models.CharField(u'周日上午',max_length=20, null=True, blank=True)
    sun2 = models.CharField(u'周日下午',max_length=20, null=True, blank=True)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    hid = models.ForeignKey(to="Hospital",on_delete=models.CASCADE)
    dsid = models.ForeignKey(to="DetailSubject",on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='科室信息'
    def __str__(self):
        return self.rname
class Subject(models.Model):
    sname = models.CharField(u'科名',max_length=20)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    class Meta:
        verbose_name_plural='疾病种类'
    def __str__(self):
        return self.sname
class DetailSubject(models.Model):
    dsname = models.CharField(u'详细科名',max_length=20)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    sid = models.ForeignKey(to="Subject",on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='详细疾病种类'
    def __str__(self):
        return self.dsname
class Illness(models.Model):
    iname = models.CharField(u'疾病名',max_length=20)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    sid = models.ForeignKey(to="Subject",on_delete=models.CASCADE)
    dsid = models.ForeignKey(to="DetailSubject",on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='疾病信息'
class Hospital(models.Model):
    hname = models.CharField(u'医院名',max_length=20)
    hlevel = models.CharField(u'等级',max_length=20,choices=(
        ('1', '三级甲等'),('2', '三级乙等'),('3', '三级丙等'),
        ('4', '二级甲等'),('5', '二级乙等'),('6', '二级丙等'),
        ('7', '一级甲等'),('8', '一级乙等'),('9', '一级丙等')),default='三级甲等')
    hphoto = models.ImageField(u'医院照片',max_length=150,upload_to='static/img')
    htel = models.CharField(u'电话', max_length=20, unique=True)
    haddress = models.CharField(u'医院地址',max_length=50)
    htext = models.TextField(u'医院介绍',max_length=5000)
    createtime = models.DateTimeField(u'创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    cid = models.ForeignKey(to="Country",on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='医院信息'
    def __str__(self):
        return self.hname
class Country(models.Model):
    cname = models.CharField(u'县/区',max_length=20)
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间',auto_now=True)
    isdelete = models.BooleanField(u'是否删除',default=False)
    class Meta:
        verbose_name_plural='县/市'
    def __str__(self):
        return self.cname
class News(models.Model):
    nname = models.CharField(u'标题',max_length=50)
    ntext = models.TextField(u'内容',max_length=5000)
    nphoto = models.ImageField(u'配图',upload_to='static/img')
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间', auto_now=True)
    isdelete = models.BooleanField(u'是否删除', default=False)
    nhospital = models.ForeignKey(to="Hospital",on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='公告信息'
    def __str__(self):
        return self.nname
class Message(models.Model):
    mname = models.CharField(u'日期',max_length=20)
    rid = models.ForeignKey(to='Room',on_delete=models.CASCADE)
    mprice = models.CharField(u'挂号价格',max_length=5)
    muid1 = models.IntegerField(u'挂号用户1',null=True,blank=True)
    mpay1 = models.CharField(u'用户1状态', max_length=32, choices=(('0', '无人预约'),('1', '未支付'),('2', '已支付')), default='0')
    muid2 = models.IntegerField(u'挂号用户2',null=True,blank=True)
    mpay2 = models.CharField(u'用户2状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid3 = models.IntegerField(u'挂号用户3',null=True,blank=True)
    mpay3 = models.CharField(u'用户3状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid4 = models.IntegerField(u'挂号用户4',null=True,blank=True)
    mpay4 = models.CharField(u'用户4状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid5 = models.IntegerField(u'挂号用户5',null=True,blank=True)
    mpay5 = models.CharField(u'用户5状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid6 = models.IntegerField(u'挂号用户6',null=True,blank=True)
    mpay6 = models.CharField(u'用户6状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid7 = models.IntegerField(u'挂号用户7',null=True,blank=True)
    mpay7 = models.CharField(u'用户7状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid8 = models.IntegerField(u'挂号用户8',null=True,blank=True)
    mpay8 = models.CharField(u'用户8状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid9 = models.IntegerField(u'挂号用户9',null=True,blank=True)
    mpay9 = models.CharField(u'用户9状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    muid10=models.IntegerField(u'挂号用户10',null=True,blank=True)
    mpay10 = models.CharField(u'用户10状态', max_length=32, choices=(('0', '无人预约'), ('1', '未支付'), ('2', '已支付')), default='0')
    mnumber = models.CharField(u'已挂号人数',max_length=10,default=0)
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间', auto_now=True)
    isdelete = models.BooleanField(u'是否删除', default=False)
    class Meta:
        verbose_name_plural='预约挂号信息'
    def __str__(self):
        return self.mname

class Board(models.Model):
    uid = models.ForeignKey(to='User',on_delete=models.CASCADE)
    did = models.ForeignKey(to='Doctor',on_delete=models.CASCADE)
    btext = models.TextField(u'患者留言')
    breply = models.TextField(u'医生回复',null=True,blank=True)
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True)
    updatetime = models.DateTimeField(u'修改时间', auto_now=True)
    isdelete = models.BooleanField(u'是否删除', default=False)
    class Meta:
        verbose_name_plural='留言板'
    def __str__(self):
        return self.uid


from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=150,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label='验证码')





