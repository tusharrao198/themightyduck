from django.db import models
# from datetime import datetime
# from django.utils import timezone

class User(models.Model):
    name= models.CharField(max_length=200, blank=False, null=False)
    email= models.CharField(max_length=200, blank=False, null=False)
    password= models.CharField(max_length=200, blank=False, null=False)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number= models.IntegerField(unique=True, default=1)
    question_content = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.question_content}"



class options(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option_number = models.IntegerField(default=1)
    option_content = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.option_content}"
