from django.db import models
import uuid

class User(models.Model):

	PENDING = 'PN'
	ACTIVE = 'AC'
	ACCOUNT_STATUS = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
    )

	name = models.CharField(max_length=40)
	email = models.EmailField(max_length=40)
	contactNo = models.IntegerField()
	status = models.CharField(
        max_length=2,
        choices=ACCOUNT_STATUS,
        default=PENDING,
    )
	key = models.PositiveSmallIntegerField(default=0)
	uniqueKey = models.UUIDField(unique = True, default=uuid.uuid4, editable=False)

	def __str__(self):
		return self.email

