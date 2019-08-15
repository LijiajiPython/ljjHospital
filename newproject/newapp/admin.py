from django.contrib import admin
from .models import User,Doctor,Room,Hospital,Country,News,Subject,DetailSubject,Illness,Message,Board
# Register your models here.
admin.site.site_header="城市医院预约挂号系统后台管理"
admin.site.site_title="后台管理"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['pk','uname','upasswd','ugender','ubirth','uaddress','utel','uemail','createtime','updatetime','isdelete']
    list_per_page=20
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display=['pk','dname','dpasswd','dgender','dphoto','dbirth','dlevel','dtel','demail','createtime','updatetime','isdelete','rid']#显示字段
    list_per_page=20 #分页
    list_filter = ('rid', 'dlevel', 'createtime')
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['pk','rname','rtel','createtime','updatetime','isdelete','hid','dsid','mon1','mon2','tue1','tue2','wed1','wed2','thu1','thu2','fri1','fri2','sat1','sat2','sun1','sun2']
    list_per_page=20
    list_filter = ('hid', 'dsid', 'createtime')
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['pk', 'hname', 'hlevel','hphoto','htel','haddress', 'createtime','updatetime', 'isdelete','cid']
    list_per_page = 20
    list_filter = ('cid', 'hlevel', 'createtime')
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sname', 'createtime','updatetime', 'isdelete']
    list_per_page = 20
@admin.register(DetailSubject)
class DetailSubjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'dsname', 'createtime','updatetime', 'isdelete','sid']
    list_per_page = 20
    list_filter = ('sid','createtime')
@admin.register(Illness)
class IllnessAdmin(admin.ModelAdmin):
    list_display = ['pk', 'iname', 'createtime','updatetime', 'isdelete','sid','dsid']
    list_per_page = 20
    list_filter = ('sid', 'dsid')
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cname', 'createtime','updatetime','isdelete']
    list_per_page = 20
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nname','nphoto','nhospital', 'createtime', 'updatetime', 'isdelete','ntext']
    list_per_page = 20
    list_filter = ('nhospital', 'createtime')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'mname','rid','mprice','mnumber','muid1','mpay1','muid2','mpay2','muid3','mpay3','muid4','mpay4','muid5','mpay5','muid6','mpay6','muid7','mpay7','muid8','mpay8','muid9','mpay9','muid10','mpay10', 'createtime', 'updatetime', 'isdelete']
    list_per_page = 20
    list_filter = ('mname', 'rid', 'createtime')

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display =['pk','uid','did','btext','breply','createtime','updatetime','isdelete']
    list_per_page = 20
    list_filter = ('breply','did', 'createtime')