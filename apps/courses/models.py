from datetime import datetime

from django.db import models

from orgs.models import OrgInfo, TeacherInfo


# Create your models here.
class CourseInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name="课程名称")
    image = models.ImageField(upload_to='courses/%y/%m/%d', verbose_name="课程封面", max_length=200)
    study_time = models.IntegerField(default=0, verbose_name="学习时长")
    love_num = models.IntegerField(default=0, verbose_name="收藏数")
    desc = models.CharField(max_length=300, verbose_name="课程简介")
    detail = models.TextField(verbose_name="课程详情")
    study_num = models.IntegerField(default=0, verbose_name="学习人数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数")
    level = models.CharField(choices=(('初级', '初级'), ('中级', '中级'), ('高级', '高级')), max_length=10, verbose_name="课程难度",
                             default='高级')
    course_category = models.CharField(choices=(('前端开发', '前端开发'), ('后端开发', '后端开发')), verbose_name="课程类别", max_length=15,
                                       default='后端开发')
    click_num = models.IntegerField(default=0, verbose_name="访问量")
    org = models.ForeignKey(OrgInfo, on_delete=models.CASCADE, verbose_name="所属机构")
    teacher = models.ForeignKey(TeacherInfo, on_delete=models.CASCADE, verbose_name="所属教师")
    course_bull = models.CharField(max_length=200, verbose_name="课程公告", null=True, blank=True)
    teacher_tell = models.CharField(max_length=200, verbose_name="讲师提示", null=True, blank=True)
    need_known = models.CharField(max_length=200, verbose_name="课程须知", null=True, blank=True)
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gl_course_info'
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class LessonInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name="章节名称")
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, verbose_name="所属课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gl_lesson_info'
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name


class VideoInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name="视频名称")
    study_time = models.IntegerField(default=0, verbose_name="学习时长")
    url = models.URLField(max_length=200, verbose_name="视频链接")
    lesson = models.ForeignKey(LessonInfo, on_delete=models.CASCADE, verbose_name="所属章节")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gl_video_info'
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name


class SourceInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name="资料名称")
    download = models.FileField(upload_to='sources/%y/%m/%d', max_length=200, verbose_name="资料下载")
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, verbose_name="所属课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gl_source_info'
        verbose_name = '资源信息'
        verbose_name_plural = verbose_name
