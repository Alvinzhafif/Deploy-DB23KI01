from django.urls import path
from main.views import *


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login_user, name='show_login'),
    path('register/', show_register, name='show_register'),
    #path('register/admin/', register_admin, name='r_admin'),
    #path('register/child/', register_child, name='r_child'),
    #path('register/caregiver/', register_caregiver, name='r_caregiver'),
    #path('register/driver/', register_driver, name='r_driver'),
    path('register/admin/', register_admin, name='r_admin'),
    path('register/child/', register_child, name='r_child'),
    path('register/caregiver/', register_caregiver, name='r_caregiver'),
    path('register/driver/', register_driver, name='r_driver'),
    path('main/',User_Dash,name='User_Dash'),
    path('Admin/',Admin_Dash,name='Admin_Dash'),
    path('Daily-Report/<str:name>',DailyRep_Page,name='DailyRep_Page'),
    path('Program/',Program_Page,name='Program_Page'), #this
    path('Enrollment/',Enrollment_Page,name='Enrollment_Page'),
    #####
    path('extracurricular/', extracurricular_page, name='extracurricular_page'),
    path('extracurricular/add', extra_add, name='extra_add'),
    path('extracurricular/edit/<str:ex_id>/', extra_edit, name='extra_edit'),
    path('extracurricular/detail/<str:ex_id>/', extra_details, name='extra_details'),
    path('extracurricular/delete/<str:ex_id>/', extra_delete, name='extra_delete'),
    
    path('menu/', menu_page, name='menu_page'),
    path('menu/add', menu_add, name='menu_add'),
    path('menu/edit/<str:menu_id>/', menu_edit, name='menu_edit'),
    path('menu/delete/<str:menu_id>/', menu_delete, name='menu_delete'),

    path('payment-history-admin/', pay_history_admin, name='pay_history_admin'),
    #####
    path('main/payment-history/', pay_history_user, name='pay_history_user'),
    path('main/pay-form', payform, name='payform'),
    path('menu/', menu_page, name='menu_page'),
    path('pickupschedule/', pickup_schedule_page, name='pickup_schedule_page'),
    path('child_list/', Child_List, name='children_page'),
    path('Activity/', Activity_Page, name='Act_Page'),
    path('Activity/delete/<str:activityid>/', Activity_Delete, name='Activity_Delete'),
    path('Act-Form/', Activity_Form, name="Act_Form"),
    path('Edit-Act/<str:activity_id>/', Edit_Activity, name="Edit_Act"),
    path('Menu-List/',Admin_Menu,name="Admin_Menu"),
    path('Menu-Form/',Add_Menu,name="Menu_Form"),
    path('Edit-Menu/',Edit_Menu,name="Edit_Menu"),
    path('Offered-Programs/',Offered_Program,name="Offered_Program"),
    path('Offer-New/<int:year>/',Offer,name="New_Offer"),
    path('Details/<int:year>/<str:name>',Prog_Detail,name="Prog_Details"),
    path('Add-ActivitySchedule/<int:year>/<str:name>',New_ActSched,name="New_ActSched"),
    path('Add-MenuSchedule/<int:year>/<str:name>',New_MenuSched,name="New_MenuSched"),
    path('Class/', Class_Page, name='Class_Page'),
    path('ChildreninClassPage/<str:class_name>/<str:year>/<str:program_id>/', Children_in_Class_Page, name='Children_In_Class_Page'),
    path('ChildrenDailyReport/<str:name>/<str:year>/<str:class_name>/<str:program_id>/', Children_Daily_Report, name="ChildrenDailyReport"),
    path('staff_list/',StaffList,name="Staff_List"),
    path('Daily-Report-Form/<str:name>/<str:year>/<str:class_name>/<str:program_id>/', DailyRepForm_Page, name='DailyRepForm_Page'),
    path('Room-List/', Admin_Room, name="Admin_Room"),
    path('Admin-Room-Form', Admin_Room_Form, name='Admin_Room_Form'),
    path('userPageRender/', userPageRender, name='userPageRender'),
    path('Shuttle-Service-Form/', ShuttleServiceForm, name='Shuttle_Service_Form'),
    path('program-page/', ProgramPage, name="program_page"),
    path('program-form-page/', ProgramFormPage, name="Admin_Program_Form"),
    path('program-edit/', ProgramPageEdit, name="program_edit"),
    path('delete_program/<int:year>/<str:name>/', Delete_Program, name='delete_program'),
    path('Extra-List/',ChildExtra,name="ChildExtra"), #this
    path('register/program',register_program,name = 'r_program'),
    path('register/activity/<int:year>/<str:name>', register_activity, name = 'r_activity'),
    path('register/menu/<int:year>/<str:name>', register_menu, name='r_menu'),
    path('logout/', logout_view, name='logout'),
    path('room/delete/<int:no>/<str:area>',room_delete,name='room_del'),
    path('register/room',register_room, name = 'r_rooms'),
    path('regis/prog', programpages, name="Ppages" ),
    path('Delete/prog<str:name>', programpagedelete, name="Dpages"),
    path('editprog/form/<str:name>',progeditpage,name='prg_edit')

]