from django.db import models
from django.contrib.auth import settings

# 患者，全局唯一
class Patient(models.Model):
    """患者数据表"""
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
    
    '''扩展信息（如身高体重等），留以日后用'''
    
    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    #注意：任何情况下不要让系统或前后台允许删除patient数据。如果有筛选数据的必要，将其active设置为false即可
    active = models.BooleanField(default=True, verbose_name='启用')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patient_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    
# Dicom文件，与唯一的患者n:1对应。当Dicom的patient id在数据库中无法找到对应患者时，新建患者并挂载外键
class DicomFile(models.Model):
    """DICOM 文件表"""
    class Meta:
        verbose_name = 'Dicom文件'
        verbose_name_plural = 'Dicom文件'
    def __str__(self):
        if self.patient:
            return str(self.patient.name + ' ' +self.patient.Patient_ID + ' | dcm id:' + ' ' + str(self.id)) 
        else:
            return str(self.id)

    error_choice = (
        (0,'已解析'),
        (202,'未初始化解析'),
        (403,'识别为非手骨图'),
        (415,'无法解析为图像')
    )

    '''基础信息'''
    #如果已有DICOM 文件数据，请尽量不要修改保存路径方法（upload_to）。如有必要，请手动保存好所有已有dcm文件再重构数据库
    dcm = models.FileField(upload_to='BoneAge/DicomFiles/%Y/%m/', verbose_name='dcm源文件')
    patient = models.ForeignKey(Patient, null=True, blank=True, verbose_name="所属患者", on_delete=models.PROTECT)
    dcm_to_image = models.ImageField(null=True, blank=True, upload_to='BoneAge/DicomFiles/%Y/%m/', verbose_name='dcm转图像')
    error = models.IntegerField(default=202, choices=error_choice, verbose_name="错误类型")

    '''扩展信息'''
    brightness = models.IntegerField(default=100, verbose_name='亮度偏量（百分数）')
    contrast = models.IntegerField(default=100, verbose_name='对比度偏量（百分数）')
    SOP_Instance_UID = models.CharField(max_length=64, verbose_name='SOP Instance UID')
    Study_Date = models.DateField(verbose_name='Study Date')

    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dicomfile_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dicomfile_creater', verbose_name='创建者', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

# 骨龄标注任务（在前端名为‘task’），与唯一的Dicom文件1:1对应
class BoneAge(models.Model):
    """骨龄判断结果表"""
    class Meta:
        verbose_name = '骨龄判断结果'
        verbose_name_plural = '骨龄判断结果'
    def __str__(self):
        return str(self.dcm_file.patient.name + ' ' +self.dcm_file.patient.Patient_ID + ' | dcm id:' + ' ' + str(self.dcm_file.id)) 

    '''基础信息'''
    dcm_file = models.OneToOneField(DicomFile,on_delete=models.CASCADE,verbose_name='对应dcm')
    bone_age = models.FloatField(default=-1.0, verbose_name='骨龄')
    allocated_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='bone_age_allocated_to', verbose_name='任务分配给', on_delete=models.PROTECT)
    allocated_datetime = models.DateTimeField(null=True, blank=True, verbose_name="任务分配时间")
    closed = models.BooleanField(default=False, verbose_name='已完成')
    closed_date = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    remarks = models.TextField(null=True, blank=True, max_length=300, verbose_name="备注")

    '''系统信息'''
    id = models.AutoField(primary_key=True,verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='grade_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

# 每根骨头的详细数据，和唯一的task为n:1关系
class BoneDetail(models.Model):
    """骨具体信息"""
    class Meta:
        verbose_name = '骨骼具体数据'
        verbose_name_plural = '骨骼具体数据'
        unique_together = (('bone_age_instance','name'),)
    def __str__(self):
        return str(
            self.bone_age_instance.dcm_file.patient.name + 
            ' ' +self.bone_age_instance.dcm_file.patient.Patient_ID + 
            ' | dcm id:' + ' ' + 
            str(self.bone_age_instance.dcm_file.id) +
            ' | ' + self.name
        ) 

    '''基础信息'''
    bone_name_choice = (
        ('Radius','桡骨'),
        ('Ulna','尺骨'),
        ('First Metacarpal','第一掌骨'),
        ('First Proximal Phalange','第一近节指骨'),
        ('First Distal Phalange','第一远节指骨'),
        ('Third Metacarpal','第三掌骨'),
        ('Third Proximal Phalange','第三近节指骨'),
        ('Third Middle Phalange','第三中节指骨'),
        ('Third Distal Phalange','第三远节指骨'),
        ('Fifth Metacarpal','第五掌骨'),
        ('Fifth Proximal Phalange','第五近节指骨'),
        ('Fifth Middle Phalange','第五中节指骨'),
        ('Fifth Distal Phalange','第五远节指骨'),
    )
    bone_level_choice = (
        (-1,'未评级'),
        (0,'0级'),
        (1,'1级'),
        (2,'2级'),
        (3,'3级'),
        (4,'4级'),
        (5,'5级'),
        (6,'6级'),
        (7,'7级'),
        (8,'8级'),
        (9,'9级'),
        (10,'10级'),
        (11,'11级'),
        (12,'12级'),
        (13,'13级'),
        (14,'14级')
    )
    error_choice = (
        (0,'正常'),
        (202,'未初始化解析'),
        (404,'无法定位'),
    )
    bone_age_instance = models.ForeignKey(BoneAge, related_name='bone_age_instance', on_delete=models.CASCADE, verbose_name='所属骨龄记录')
    name = models.CharField(choices=bone_name_choice, max_length=23,verbose_name='骨名')
    level = models.IntegerField(default=-1, choices=bone_level_choice, verbose_name='RUS-CHN 14阶评级')
    error = models.IntegerField(default=202, choices=error_choice, verbose_name='定位状态')
    center_x = models.FloatField(default=-1, verbose_name='中心点x')
    center_y = models.FloatField(default=-1, verbose_name='中心点y')
    width = models.FloatField(default=-1, verbose_name='宽度')
    height = models.FloatField(default=-1, verbose_name='高度')
    remarks = models.TextField(null=True, blank=True, max_length=100, verbose_name='备注')

    '''系统信息'''
    id = models.AutoField(primary_key=True,verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bone_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')