from django.db import models

"""
用户表
"""


class User(models.Model):
    # 性别枚举值
    gender = (
        ("male", "男"),
        ("female", "女"),
    )

    name = models.CharField("姓名", max_length=128, unique=True)
    password = models.CharField("密码", max_length=256)
    email = models.EmailField("邮箱", unique=True)
    sex = models.CharField("性别", max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        #按创建时间倒序排列
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
