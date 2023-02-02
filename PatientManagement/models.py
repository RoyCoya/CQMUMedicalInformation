from django.contrib.auth import settings
from django.db import models

# 患者，全局唯一
class Patient(models.Model):
    class Meta:
        verbose_name = '患者'
        verbose_name_plural = '患者'
    def __str__(self):
        return str(self.name + ' ' +self.Patient_ID) 

    '''基础信息'''
    Patient_ID = models.CharField(max_length=64, unique=True, verbose_name='Dicom Patient ID')
    name = models.CharField(max_length=100, verbose_name='姓名')
    sex_choice = (('Male','男'),('Female','女'))
    sex = models.CharField(max_length=6, choices=sex_choice, verbose_name='性别')
    birthday = models.DateField(verbose_name='生日')
    
    '''扩展信息'''
    
    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    #注意：任何情况下不要让系统或前后台允许删除patient数据。如果有筛选数据的必要，将其active设置为false即可
    active = models.BooleanField(default=True, verbose_name='启用')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patient_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')