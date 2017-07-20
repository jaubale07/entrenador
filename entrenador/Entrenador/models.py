from django.db import models


class Process(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre


class Fail(models.Model):
    process = models.ForeignKey('Process')
    name = models.CharField(max_length=50)
    pin = models.IntegerField()
    activo = models.BooleanField(default=False)

    def __unicode__(self):
        return self.process.name + ' > ' + self.name


class Solution(models.Model):
    fail = models.ForeignKey('Fail')
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.fail.process.name + ' > ' + self.fail.name + ' > ' + self.name


class Step(models.Model):
    solution = models.ForeignKey('Solution')
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.solution.name + ' > ' + self.name
