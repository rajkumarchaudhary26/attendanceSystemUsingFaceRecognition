from django.contrib import admin
from AttendanceApp.models import User, Student, Image, Attendence
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.models import Group
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render,redirect
import os
# from AttendanceApp.faces import face_recognizer

# Register your models here.

User = get_user_model()


class AttendenceAdmin(admin.ModelAdmin):
    list_display = ('student_id_id','student_name','date','time','Student_status' )
    list_filter = ('student_id_id','date')
    search_fields =('student_id_id','date')
    ordering = ('date',)
   
    def Student_status(self,obj):
        return 'Present' if obj.status == 1 else 'Absent'
    def  student_name(self,obj):
        return Student.objects.get(id=obj.student_id_id)
    # student_last_name.admin_order_field = 'student__name'
# ---------------------------------------
# --------------------------------------

class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
    list_display = ('id','username', 'admin','staff', 'active')
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','address')}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email','mobile_no','password1', 'password2')}
        ),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def has_add_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False


    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(id=request.user.id)

# class ImageInline(admin.StackedInline):
#     model = Image
#     extra = 1

class StudentAdmin(admin.ModelAdmin):

    list_display = ('id','first_name', 'last_name','email', 'address')

    def get_urls(self):
        urls = super(StudentAdmin, self).get_urls()
        my_urls = [
            # url(r'^my_view/$', self.my_view, name="custom_view"),
            url(r'^my_view2/$', self.my_view2, name="custom_view2"),
            # url(r'^generate_dataset/$', self.generate_dataset, name="dataset"),
        ]
        return my_urls + urls

    def my_view2(self,request):
       print(os.system("python faces.py"))
       return HttpResponse("recognizing")
   
    # def my_view2(self, request):
        
    #     face_cascade=cv2.CascadeClassifier("C:/Users/Raj/Desktop/cascades/data/haarcascade_frontalface_alt2.xml")
    #     recognizer=cv2.face.LBPHFaceRecognizer_create()
    #     recognizer.read("trainer.yml")
    #     labels={}
    #     with open("labels.pkl","rb") as f:
    #         og_labels=pickle.load(f)
    #         labels={v:k for k,v in og_labels.items()}
    #     cap=cv2.VideoCapture(0)
    #     while True:
    #         ret,frame=cap.read()
    #         gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #         faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    #         for x,y,w,h in faces:
    #             roi_gray=gray[y:y+h,x:x+w]
    #             roi_color=frame[y:y+h,x:x+w]
    #             id_,conf=recognizer.predict(roi_gray)
    #             if conf>=45:
    #                 print(id_)
    #                 print(labels[id_])
    #                 print(conf)
    #                 font=cv2.FONT_HERSHEY_SIMPLEX
    #                 name=labels[id_]
    #                 color=(0,255,0)
    #                 stroke=2
    #                 cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
    #             my_item=cv2.imwrite("17.jpg",roi_gray)
    #             my_item = cv2.imwrite("18.jpg", roi_color)
    #             color=(255,0,0)
    #             stroke=2
    #             cv2.rectangle(frame,(x,y),(x+w,y+h),color,stroke)
    #         cv2.imshow('frame',frame)
    #         if cv2.waitKey(20) & 0xFF == ord('q') or cv2.waitKey(20) & 0xFF == ord('Q'):
    #             break
    #     cap.release()
    #     cv2.destroyAllWindows()
        # return HttpResponse("OK")

    def generate_dataset(self, request):
        return HttpResponse("OK")



        # return render(request, '/home/iampk/Desktop/lab3.py')


# class ImageAdmin(admin.ModelAdmin):

#     raw_id_fields = ('student_id',)
#     list_display = ('id','student_id', 'image')
#     # search_fields = ('Student',)


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Attendence,AttendenceAdmin)
# admin.site.register(Image, ImageAdmin)


admin.site.unregister(Group)