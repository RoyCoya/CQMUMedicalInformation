from django.contrib.auth import settings
from django.db import models
from django.apps import apps

from PatientManagement.models import Patient

# Dicom文件，与唯一的患者n:1对应。当Dicom的patient id在数据库中无法找到对应患者时，新建患者并挂载外键
class DicomFile(models.Model):
    class Meta:
        verbose_name = 'DICOM文件'
        verbose_name_plural = 'DICOM文件'
    def __str__(self):
        if self.patient:
            return str(self.patient.name + ' ' +self.patient.Patient_ID + ' | dcm id:' + ' ' + str(self.id)) 
        else:
            return str(self.id)

    '''基础信息'''
    #如果已有DICOM 文件数据，请尽量不要修改保存路径方法（upload_to）。如有必要，请手动保存好所有已有dcm文件再重构数据库
    dcm = models.FileField(upload_to='DicomFiles/%Y/%m/', max_length=1000, verbose_name='dcm源文件')
    patient = models.ForeignKey(Patient, null=True, blank=True, verbose_name="所属患者", on_delete=models.PROTECT)
    dcm_to_image = models.ImageField(null=True, blank=True, upload_to='DicomFiles/%Y/%m/', max_length=1000, verbose_name='dcm转图像')
    SOP_Instance_UID = models.CharField(null=True, blank=True, unique=True, max_length=64, verbose_name='SOP Instance UID')

    # 扩展信息。只抽取一些重要的tag，不重要的需要时再去读取dicom文件
    Study_Date = models.DateField(null=True, blank=True, default=None, verbose_name='Study Date')
    Study_Time = models.TimeField(null=True, blank=True, default=None, verbose_name='Study Time')
    Window_Center = models.CharField(null=True, blank=True, default=None, max_length=500, verbose_name='Window Center')
    Window_Width = models.CharField(null=True, blank=True, default=None, max_length=500, verbose_name='Window Width')

    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='DICOMManagement_DicomFile_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='DICOMManagement_DicomFile_creator', verbose_name='创建者', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

class PACS(models.Model):
    """
    远程PACS配置。每一个PACS相当于Orthanc中的一个modality
    """
    class Meta:
        verbose_name = '远程PACS'
        verbose_name_plural = '远程PACS'
    def __str__(self):
        return str(self.id) + '|' + str(self.name)
    
    '''基础信息'''
    name = models.CharField(max_length=50, verbose_name='服务器名称')
    description = models.CharField(null=True, blank=True, max_length=500, verbose_name='描述')
    remote_ip = models.GenericIPAddressField(protocol='both', verbose_name='IP')
    remote_port = models.PositiveIntegerField(verbose_name='端口号')
    remote_AET = models.CharField(max_length=50, verbose_name='实体名（AE title）')

    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    status_choice = (
        ('Running', '正常运行'),
        ('Suspending', '挂起'),
        ('Closed', '关闭'),
    )
    status = models.CharField(choices=status_choice, max_length=50)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='DICOMManagement_PACS_creator', verbose_name='创建者', on_delete=models.PROTECT)
    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

class PACS_conf(models.Model):
    """
    自动生成的Orthanc config记录。暂未启用。
    """
    class Meta:
        verbose_name = 'PACS配置记录'
        verbose_name_plural = 'PACS配置记录'
    def __str__(self):
        return str(self.create_date_time)
    
    '''基础信息'''
    # 配置描述
    # 建议格式：[操作:更改字段]详情
    description = models.CharField(null=True, blank=True, max_length=500, verbose_name='描述')
    path = models.CharField(max_length=1000, verbose_name='配置文件保存路径')

    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='DICOMManagement_PACS_conf_creator', verbose_name='创建者', on_delete=models.PROTECT)
    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
# # PACS交互记录
# class PACS_log(models.Model):
#     class Meta:
#         verbose_name = 'PACS交互记录'
#         verbose_name_plural = 'PACS交互记录'
#     def __str__(self):
#         return str(self.pacs.name) + '|' + str(self.id)
    
#     pacs = models.ForeignKey(PACS, on_delete=models.PROTECT)
#     app_choice = (app_config.name for app_config in apps.get_app_configs() if app_config.name)
#     app = models.IntegerField(choices=app_choice, verbose_name='发起操作的子系统')
#     status_choice = (
#         (102, '处理中'),
#         (200, '成功'),
#         (502, '失败'),
#     )
#     status = models.PositiveIntegerField(verbose_name='状态')
#     type_choice = ('C-ECHO', 'C-MOVE')
#     type = models.CharField(choices=type_choice, max_length=50, verbose_name='交互类型')
#     data = models.CharField(max_length=10000,null=True, blank=True, verbose_name='交互输入')
#     result = models.CharField(max_length=10000,null=True, blank=True, verbose_name='交互结果')

#     '''系统信息'''
#     id = models.AutoField(primary_key=True, verbose_name='ID')
#     create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='交互时间')