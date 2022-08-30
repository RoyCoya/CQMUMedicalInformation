from django.db import models
from django.contrib.auth import settings

from DICOMManagement.models import DicomFile as dicomfile_base_class
    
# 骨龄专用Dicom文件扩展信息
class DicomFile(models.Model):
    class Meta:
        verbose_name = '骨龄用Dicom信息'
        verbose_name_plural = '骨龄用Dicom信息'
    def __str__(self):
        return str(self.base_dcm.patient.name + str(self.id))

    # 父类来自Dicom管理app
    base_dcm = models.OneToOneField(dicomfile_base_class, related_name='BoneAge_DicomFile_base', verbose_name='DICOM信息基类', on_delete=models.CASCADE)

    '''基础信息'''
    #如果已有DICOM 文件数据，请尽量不要修改保存路径方法（upload_to）。如有必要，请手动保存好所有已有dcm文件再重构数据库
    error_choice = (
        (0,'已解析'),
        (202,'未初始化解析'),
        (403,'识别为非手骨图'),
        (415,'无法解析为图像')
    )
    error = models.IntegerField(default=202, choices=error_choice, verbose_name="错误类型")

    '''扩展信息'''
    brightness = models.IntegerField(default=100, verbose_name='亮度偏量（百分数）')
    contrast = models.IntegerField(default=100, verbose_name='对比度偏量（百分数）')

    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='BoneAge_DicomFile_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='BoneAge_DicomFile_creater', verbose_name='创建者', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

# 骨龄标注任务（在前端名为‘task’），与唯一的Dicom文件1:1对应
class BoneAge(models.Model):
    class Meta:
        verbose_name = '骨龄判断结果'
        verbose_name_plural = '骨龄判断结果'
    def __str__(self):
        return str(self.dcm_file.base_dcm.patient.name + ' ' +self.dcm_file.base_dcm.patient.Patient_ID + ' | dcm id:' + ' ' + str(self.dcm_file.id)) 

    '''基础信息'''
    dcm_file = models.OneToOneField(DicomFile,on_delete=models.CASCADE,verbose_name='对应dcm')
    bone_age = models.FloatField(default=-1.0, verbose_name='骨龄')
    allocated_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='BoneAge_BoneAge_allocated_to', verbose_name='任务分配给', on_delete=models.PROTECT)
    allocated_datetime = models.DateTimeField(null=True, blank=True, verbose_name="任务分配时间")
    closed = models.BooleanField(default=False, verbose_name='已完成')
    closed_date = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    remarks = models.TextField(null=True, blank=True, max_length=300, verbose_name="备注")

    '''系统信息'''
    id = models.AutoField(primary_key=True,verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='BoneAge_BoneAge_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

# 每根骨头的详细数据，和唯一的task为n:1关系
class BoneDetail(models.Model):
    class Meta:
        verbose_name = '骨骼具体数据'
        verbose_name_plural = '骨骼具体数据'
        unique_together = (('bone_age_instance','name'),)
    def __str__(self):
        return str(
            self.bone_age_instance.dcm_file.base_dcm.patient.name + 
            ' ' +self.bone_age_instance.dcm_file.base_dcm.patient.Patient_ID + 
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
    bone_age_instance = models.ForeignKey(BoneAge, related_name='BoneAge_BoneDetail_bone_age_instance', on_delete=models.CASCADE, verbose_name='所属骨龄记录')
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
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='BoneAge_BoneDetail_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

# 用户个人偏好设置
class Preference(models.Model):
    class Meta:
        verbose_name = '偏好设置'
        verbose_name_plural = '偏好设置'
    def __str__(self):
        return str()

    '''基础设置'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='用户', on_delete=models.PROTECT, primary_key=True)
    standard_choice = (
        ('RUS','RUS-CHN标准'),
        ('CHN','CHN标准'),
    )
    standard = models.CharField(choices=standard_choice, max_length=10, default='RUS',verbose_name='默认骨龄标准')
    default_bone_choice = (
        ('RUS_radius','RUS 桡骨'),
        ('RUS_ulna','RUS 尺骨'),
        ('RUS_first-metacarpal','RUS 第一掌骨'),
        ('RUS_third-metacarpal','RUS 第三掌骨'),
        ('RUS_fifth-metacarpal','RUS 第五掌骨'),
        ('RUS_first-proximal-phalange','RUS 第一近节指骨'),
        ('RUS_third-proximal-phalange','RUS 第三近节指骨'),
        ('RUS_fifth-proximal-phalange','RUS 第五近节指骨'),
        ('RUS_third-middle-phalange','RUS 第三中节指骨'),
        ('RUS_fifth-middle-phalange','RUS 第五中节指骨'),
        ('RUS_first-distal-phalange','RUS 第一远节指骨'),
        ('RUS_third-distal-phalange','RUS 第三远节指骨'),
        ('RUS_fifth-distal-phalange','RUS 第五远节指骨'),
    )
    default_bone = models.CharField(choices=default_bone_choice, max_length=100, default='RUS_radius',verbose_name='默认骨骼')
    shortcut = models.BooleanField(default=True, verbose_name='启用快捷键')
    bone_order_RUS = models.CharField(
        default='Radius|Ulna|First Metacarpal|Third Metacarpal|Fifth Metacarpal|'
        'First Proximal Phalange|Third Proximal Phalange|Fifth Proximal Phalange|'
        'Third Middle Phalange|Fifth Middle Phalange|'
        'First Distal Phalange|Third Distal Phalange|Fifth Distal Phalange',
        max_length= 500,
        verbose_name="RUS 骨骼排序"
    )
