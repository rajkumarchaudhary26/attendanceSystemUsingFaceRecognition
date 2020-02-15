from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager
)
from django.core.validators import RegexValidator
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password = None, is_active = True, is_staff = False, is_admin = False):
        if not username:
            raise ValueError('users most provide user name')
        if not password:
            raise ValueError('password is required')
        user_obj = self.model(username = username)
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, username, password = None):
        user = self.create_user(username, password=password, is_staff=True)
        return user

    def create_superuser(self, username, password = None):
        user = self.create_user(username, password=password, is_staff=True, is_admin=True)
        return user



class User(AbstractBaseUser):
    mobile_no = models.CharField(unique=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    username = models.CharField(max_length=50, unique = True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique = True)
    address = models.CharField(max_length=50)
    # created_by = models.IntegerField()
    created_date = models.DateField(auto_now=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    
    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'
    REQUIRED_FEILDS = []
    
    objects = UserManager()

    def has_perm(self, perm, obj = None):
        return True

    
    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique = True)
    address = models.CharField(max_length=50)
    created_date = models.DateField(auto_now=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    def __str__(self):
        return self.first_name+" "+self.last_name

class Admin(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique = True)
    address = models.CharField(max_length=50)
    created_date = models.DateField(auto_now=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)


class Image(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return '{0}/{1}'.format(instance.student_id_id, filename)
    image = models.FileField(upload_to=user_directory_path, max_length=254)

class Attendence(models.Model):
     student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
     date = models.DateField( auto_now=True)
     time = models.TimeField(auto_now=True)
     status = models.BooleanField(default=False)
