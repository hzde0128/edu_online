# Generated by Django 3.0.5 on 2020-11-24 16:13

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='课程名称')),
                ('image', models.ImageField(max_length=200, upload_to='courses/%y/%m/%d', verbose_name='课程封面')),
                ('study_time', models.IntegerField(default=0, verbose_name='学习时长')),
                ('love_num', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('desc', models.CharField(max_length=300, verbose_name='课程简介')),
                ('detail', DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情')),
                ('study_num', models.IntegerField(default=0, verbose_name='学习人数')),
                ('comment_num', models.IntegerField(default=0, verbose_name='评论人数')),
                ('level', models.CharField(choices=[('初级', '初级'), ('中级', '中级'), ('高级', '高级')], default='高级', max_length=10, verbose_name='课程难度')),
                ('course_category', models.CharField(choices=[('前端开发', '前端开发'), ('后端开发', '后端开发')], default='后端开发', max_length=15, verbose_name='课程类别')),
                ('click_num', models.IntegerField(default=0, verbose_name='访问量')),
                ('course_bull', models.CharField(blank=True, max_length=200, null=True, verbose_name='课程公告')),
                ('teacher_tell', models.CharField(blank=True, max_length=200, null=True, verbose_name='讲师提示')),
                ('need_known', models.CharField(blank=True, max_length=200, null=True, verbose_name='课程须知')),
                ('is_banner', models.BooleanField(default=False, verbose_name='是否轮播')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.OrgInfo', verbose_name='所属机构')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.TeacherInfo', verbose_name='所属教师')),
            ],
            options={
                'verbose_name': '课程信息',
                'verbose_name_plural': '课程信息',
                'db_table': 'edu_courses',
                'ordering': ['-add_time'],
            },
        ),
        migrations.CreateModel(
            name='LessonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseInfo', verbose_name='所属课程')),
            ],
            options={
                'verbose_name': '章节信息',
                'verbose_name_plural': '章节信息',
                'db_table': 'edu_lessons',
            },
        ),
        migrations.CreateModel(
            name='VideoInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='视频名称')),
                ('study_time', models.IntegerField(default=0, verbose_name='学习时长')),
                ('url', models.FileField(upload_to='courses/%y/%m/%d', verbose_name='视频链接')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.LessonInfo', verbose_name='所属章节')),
            ],
            options={
                'verbose_name': '视频信息',
                'verbose_name_plural': '视频信息',
                'db_table': 'edu_videos',
            },
        ),
        migrations.CreateModel(
            name='SourceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='资料名称')),
                ('download', models.FileField(max_length=200, upload_to='sources/%y/%m/%d', verbose_name='资料下载')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseInfo', verbose_name='所属课程')),
            ],
            options={
                'verbose_name': '资源信息',
                'verbose_name_plural': '资源信息',
                'db_table': 'edu_sources',
            },
        ),
    ]
