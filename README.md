# edu_online 在线教育网

基于Django3和xadmin开发的在线教育网站

## 开发环境

- Python3.8
- Django3
- Xadmin
- DjangoUeditor

## 安装

```bash
pip install -r requirements.txt
```

## 运行

1. 修改数据库配置和邮件等相关信息

   ```bash
   vim admin/settings.py
   ```

2. 数据迁移

   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

3. 创建管理员账号

   ```bash
   python manag.py createsuperuser
   ```

4. 运行

   ```bash
   python3 manage.py runserver 
   ```

