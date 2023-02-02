from django.contrib.auth import settings
from django.db import models

from PatientManagement.models import Patient

# Dicom文件，与唯一的患者n:1对应。当Dicom的patient id在数据库中无法找到对应患者时，新建患者并挂载外键
class DicomFile(models.Model):
    class Meta:
        verbose_name = 'Dicom文件'
        verbose_name_plural = 'Dicom文件'
    def __str__(self):
        if self.patient:
            return str(self.patient.name + ' ' +self.patient.Patient_ID + ' | dcm id:' + ' ' + str(self.id)) 
        else:
            return str(self.id)

    '''基础信息'''
    #如果已有DICOM 文件数据，请尽量不要修改保存路径方法（upload_to）。如有必要，请手动保存好所有已有dcm文件再重构数据库
    dcm = models.FileField(upload_to='DicomFiles/%Y/%m/', verbose_name='dcm源文件')
    patient = models.ForeignKey(Patient, null=True, blank=True, verbose_name="所属患者", on_delete=models.PROTECT)
    dcm_to_image = models.ImageField(null=True, blank=True, upload_to='DicomFiles/%Y/%m/', verbose_name='dcm转图像')

    '''扩展信息'''
    SOP_Instance_UID = models.CharField(null=True, blank=True, unique=True, max_length=64, verbose_name='SOP Instance UID')
    Study_Date = models.DateField(null=True, blank=True, verbose_name='Study Date')

    '''系统信息'''
    id = models.AutoField(primary_key=True, verbose_name='ID')
    modify_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dicomfile_modifier', verbose_name='最后修改者', on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dicomfile_creater', verbose_name='创建者', on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')