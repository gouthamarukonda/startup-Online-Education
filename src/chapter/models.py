from __future__ import unicode_literals

from django.db import models

SUBJECT_MATHS = '0'
SUBJECT_PYHSICS = '1'
SUBJECT_CHEMISTRY = '2'

SUBJECT_CHOICES = (
	(SUBJECT_MATHS, 'maths'),
	(SUBJECT_PYHSICS, 'physics'),
	(SUBJECT_CHEMISTRY, 'chemistry'),
)

class Subject(models.Model):

	subject_id = models.AutoField("Subject ID", db_column = 'subject_id', primary_key = True)
	subject_name = models.CharField("Subject Name", max_length = 500)

	class Meta:
		db_table = 'subject'

	def __unicode__(self):
		return unicode(self.subject_name)


class Chapter(models.Model):

	chapter_id = models.AutoField("Chapter ID", db_column = 'chapter_id', primary_key = True)
	chapter_name = models.CharField("Chapter Name", max_length = 500)
	subject = models.ForeignKey(Subject, db_column = 'subject', on_delete = models.CASCADE)

	class Meta:
		db_table = 'chapter'

	def __unicode__(self):
		return unicode(self.chapter_name)
