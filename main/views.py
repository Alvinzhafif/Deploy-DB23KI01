from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import *
from main.models import *
from main.models import User
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import psycopg2
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db import DatabaseError
import psycopg2
from psycopg2 import errors
from datetime import datetime
#from main.forms import * 
def show_main(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    SELECT * FROM USERS;""")
    data = cur.fetchall()
    cur.close()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM STAFF""")
    data2 = cur.fetchall()
    print(data)
    print(data2)
    cur.close()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM DRIVER_DAY""")
    data3 = cur.fetchall()
    print(data3)
    cur.close()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM CLASS""")
    data4 = cur.fetchall()
    print(data4)
    cur.close()
    conn.close()

# commit the changes
    
# # executing queries to create table


#  commit the changes
    #conn.commit()
    #print("Task finished successfully")
    #cur.close()
    #conn.close()

    return render(request, 'main.html', context)
@csrf_exempt
def show_login(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'login.html', context)

def show_register(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'register.html', context)

def register_admin_temp(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'r_admin.html', context)

def register_child_temp(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'r_child.html', context)

def register_caregiver_temp(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'r_caregiver.html', context)

def register_driver_temp(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'r_driver.html', context)


def User_Dash(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'UserPage.html', context)

def Admin_Dash(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'AdminPage.html', context)

def DailyRep_Page(request, name):

    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT *
                FROM DAILY_REPORT DR
                join users u on u.userid = DR.userid
                WHERE CONCAT(u.first_name, ' ', u.last_name) = %s;
                """,[name])

    data =  cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': data,
    }
    cur.close()
    conn.close()

    return render(request, 'DailyReport.html', context)

def Program_Page(request):
    phone = request.user.phone_number
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        SELECT userid
        FROM users
        WHERE phone_number=%s;
    """, [phone])
    userid =  cur.fetchone()
    print(userid[0])

    cur.execute(rf"""
        set search_path to merahbirudaycare;
        SELECT
            c.userid AS child_id,
            p.name AS program_name,
            e.year AS program_year,
            e.class AS class_name,
            CONCAT(u.first_name, ' ', u.last_name) AS caregiver,
            e.pickup_hour AS shuttle_pickup_hour,
            d.driver_license_number AS driver_phone_number,
            e.date AS enrolled_on_date,
            et.extracurriculars_taken,
            ms.activity_schedule,
            mns.menu_schedule
        FROM
            enrollment e
        JOIN
            child c ON e.userid = c.userid
        JOIN
            program p ON e.programid = p.programid
        JOIN
            users u ON u.userid = c.userid
        LEFT JOIN
            caregiver cg ON cg.userid = u.userid
        LEFT JOIN
            driver d ON e.driverid = d.userid
        LEFT JOIN (
            SELECT
                userid,
                programid,
                year,
                class,
                STRING_AGG(ex.name, ', ') AS extracurriculars_taken
            FROM
                extracurricular_taking et
            JOIN
                extracurricular ex ON et.extracurricularid = ex.extracurricularid
            GROUP BY
                userid, programid, year, class
        ) et ON et.userid = e.userid AND et.programid = e.programid AND et.year = e.year AND et.class = e.class
        LEFT JOIN (
            SELECT
                programid,
                year,
                day,
                STRING_AGG(name, ', ') AS activity_schedule
            FROM
                activity_schedule
            JOIN
                activity a ON activity_schedule.activity_id = a.id
            GROUP BY
                programid, year, day
        ) ms ON ms.programid = p.programid AND ms.year = e.year
        LEFT JOIN (
            SELECT
                programid,
                year,
                day,
                hour,
                STRING_AGG(m.name, ', ') AS menu_schedule
            FROM
                menu_schedule
            JOIN
                menu m ON menu_schedule.menuid = m.id
            GROUP BY
                programid, year, day, hour
        ) mns ON mns.programid = e.programid AND mns.year = e.year
        WHERE
            e.userid = %s;
    """, [userid[0]])

    data = cur.fetchall()

    context = {
        'program_data': data,
    }

    cur.close()
    conn.close()

    return render(request, 'Program.html', context)

def Enrollment_Page(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'Enrollment.html', context)

def extracurricular_page(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT name, day, hour, extracurricularid
                FROM extracurricular;   
                """)

    data =  cur.fetchall()

    cur.execute(rf"""
                select distinct extracurricularid from extracurricular_taking;
                """)

    participant =  cur.fetchall()
    p_list = [item[0] for item in participant]
    context = {
        'data': data,
        'p_list' : p_list
    }
    cur.close()
    conn.close()
    return render(request, 'extracurricular.html', context)

@csrf_exempt
def extra_add(request):
    if request.method == "POST":
        exname = request.POST.get('exname')
        day = request.POST.get('day')
        hour = request.POST.get('hour')
        ex_uuid = str(uuid.uuid4())
        
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
            INSERT INTO EXTRACURRICULAR VALUES (%s, %s, %s, %s) 
        """, [ex_uuid, exname, day, hour])
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect('main:extracurricular_page')
    return render(request, 'extraAdd.html')

def extra_details(request, ex_id):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT name, day, hour, extracurricularid
                FROM extracurricular
                WHERE extracurricularid = %s;   
                """, [ex_id])

    data =  cur.fetchall()
    print(data)

    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT U.first_name || ' ' || U.last_name, ET.class
                FROM extracurricular_taking ET, users U
                WHERE U.userid=ET.userid AND ET.extracurricularid = %s;   
                """, [ex_id])

    participant = cur.fetchall()

    context = {
        'data': data,
        'participant': participant
    }
    cur.close()
    conn.close()
    return render(request, 'extraDetails.html', context)

@csrf_exempt
def extra_delete(request, ex_id):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                DELETE
                FROM extracurricular
                WHERE extracurricularid = %s;   
                """, [ex_id])


    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT name, day, hour, extracurricularid
                FROM extracurricular;   
                """)

    data =  cur.fetchall()
    context = {
        'data': data
    }
    conn.commit()
    cur.close()
    conn.close()
    return render(request, 'extracurricular.html', context)

@csrf_exempt
def extra_edit(request, ex_id):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    
        SELECT name
        FROM EXTRACURRICULAR
        WHERE extracurricularid = %s;
    """, [ex_id])
    
    name =  cur.fetchall()
    context = {
        'name': name
    }
    cur.close()
    conn.close()
    
    if request.method == "POST":
        exname = request.POST.get('exname')
        day = request.POST.get('day')
        hour = request.POST.get('hour')
        
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        
            UPDATE extracurricular
            SET name = %s, day = %s, hour = %s
            WHERE extracurricularid = %s;
        """, [exname, day, hour, ex_id])
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect('main:extracurricular_page')
    return render(request, 'extraEdit.html', context)

def menu_page(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                select name, type, id from menu;
                """)

    data =  cur.fetchall()

    cur.execute(rf"""
                select distinct M.id
                from offered_program OP
                left join menu_schedule MS ON MS.programid=OP.programid
                left join menu M ON MS.menuid=M.id;
                """)

    inprogram =  cur.fetchall()
    ip_list = [item[0] for item in inprogram]
    context = {
        'data': data,
        'ip_list' : ip_list
    }
    cur.close()
    conn.close()
    return render(request, 'menu.html', context)

@csrf_exempt
def menu_add(request):
    if request.method == "POST":
        m_name = request.POST.get('m_name')
        m_type = request.POST.get('m_type')
        m_uuid = str(uuid.uuid4())
        
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
            INSERT INTO menu VALUES (%s, %s, %s) 
        """, [m_uuid, m_name, m_type])
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect('main:menu_page')
    return render(request, 'menuAdd.html')

@csrf_exempt
def menu_delete(request, menu_id):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                DELETE
                FROM menu
                WHERE id = %s;   
                """, [menu_id])


    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT name, type, id
                FROM menu;   
                """)

    data =  cur.fetchall()
    context = {
        'data': data
    }
    conn.commit()
    cur.close()
    conn.close()
    return redirect('main:menu_page')

@csrf_exempt
def menu_edit(request, menu_id):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    
        SELECT name
        FROM menu
        WHERE id = %s;
    """, [menu_id])
    
    name =  cur.fetchall()
    context = {
        'name': name
    }
    cur.close()
    conn.close()
    
    if request.method == "POST":
        m_name = request.POST.get('m_name')
        m_type = request.POST.get('m_type')
        
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        
            UPDATE menu
            SET name = %s, type = %s
            WHERE id = %s;
        """, [m_name, m_type, menu_id])
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect('main:menu_page')
    return render(request, 'menuEdit.html', context)

def pickup_schedule_page(request):
    return render(request, 'PickUpSchedule.html')
@login_required
def userPageRender(request):
    users = User.objects.filter(phone_number = str(request.user))
    user = users.first()
    context = {}
    print(users)
    print(user)
    phone_number = user.phone_number
    print(user.is_caregiver)
    #phone_number = str(request.user)
    print(user.phone_number)
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;""")
    cur.execute("""SELECT userid, password, phone_number, first_name, last_name, gender, birth_date, address FROM USERS WHERE phone_number = %s;""", [phone_number])
    data = cur.fetchall()
    id_user = data[0][0]
    context['password'] = data[0][1]
    context['phone_number'] = data[0][2]
    first_name = data[0][3]
    last_name = data[0][4]
    context['gender'] = data[0][5]
    context['birth_date'] = data[0][6]
    context['address'] = data[0][7]
    print(data)
    cur.close()
    cur = conn.cursor()


    if user.is_child:
        context['role'] = 'child'
        cur.execute("""SELECT Dad_Name, Mom_Name, Dad_Job, Mom_Job FROM CHILD WHERE userid=%s""", [id_user])
        data2 = cur.fetchall()
        context['father_name'] = data2[0][0]
        context['mother_name'] = data2[0][1]
        context['father_job'] = data2[0][2]
        context['mother_job'] = data2[0][3]
    elif user.is_caregiver:
        print("dashboard caregiver")
        context['role'] = 'caregiver'
        cur.execute("""SELECT nik, npwp, bank_account, bank_name FROM STAFF WHERE userid=%s""", [id_user])
        data2 = cur.fetchall()
        print(len(data2))
        context['nik'] = data2[0][0]
        context['npwp'] = data2[0][1]
        context['bank_account'] = data2[0][2]
        context['bank_name'] = data2[0][3]
        cur.close()
        cur = conn.cursor()
        cur.execute("""SELECT certificate_number, certificate_name, certificate_year, certificate_organizer FROM CAREGIVER_CERTIFICATE WHERE userid=%s""", [id_user])
        data3 = cur.fetchall()
        context['certificate_number'] = []
        context['certificate_name'] = []
        context['certificate_year'] = []
        context['certificate_organizer'] = []
        for i in range(len(data3)):
           context['certificate_number'].append(data3[i][0])
           context['certificate_name'].append(data3[i][1])
           context['certificate_year'].append(data3[i][2])
           context['certificate_organizer'].append(data3[i][3])
    elif user.is_driver:
        context['role'] = 'driver'
        cur.execute("""SELECT nik, npwp, bank_account, bank_name FROM STAFF WHERE userid=%s""", [id_user])
        data2 = cur.fetchall()
        print(len(data2))
        context['nik'] = data2[0][0]
        context['npwp'] = data2[0][1]
        context['bank_account'] = data2[0][2]
        context['bank_name'] = data2[0][3]
        cur.close()
        cur = conn.cursor()
        cur.execute("""SELECT driver_license_number FROM DRIVER WHERE userid=%s""", [id_user])
        data3 = cur.fetchall()
        context['driver_license_number'] = data3[0][0]
        cur.close()
        cur = conn.cursor()
        cur.execute("""SELECT day FROM DRIVER_DAY WHERE userid=%s""", [id_user])
        data4 = cur.fetchall()
        context['driver_day'] = []
        for i in range(len(data4)):
            context['driver_day'].append(data4[i][0])
    context['name'] = first_name + " " + last_name
    print(context)
    return render(request, 'UserPage.html', context)

def Child_List(request):

    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT * FROM USERS U
                JOIN CHILD C ON U.userid = C.userid;
                """)

    data =  cur.fetchall()
    cur.execute(rf"""
            set search_path to merahbirudaycare;
            UPDATE ENROLLMENT 
            set class = 'PreKindergarten-A'
            where userid = '4d26972e-f0ea-4879-80a7-f946635d781b';
            SELECT *
            FROM enrollment E
            JOIN CHILD C ON E.userid = C.userid;
                """)
    
    data2 = cur.fetchall()
    print(data2)
    conn.commit()
    data2_info = [row[3] for row in data2]

    # Combine the original data and the new information from data2
    combined_data = list(zip(data, data2_info))

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': combined_data

    }
    cur.close()
    conn.close()

    return render(request, 'ChildList.html', context)

def Activity_Page(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor()
    cur.execute("set search_path to merahbirudaycare;")
    cur.execute(rf"""
                select name, id from activity;
                """)

    data = cur.fetchall()
    context = {
        'data': data,
    }

    return render(request, 'Activity.html', context)

@csrf_exempt
def Activity_Form(request):
    if request.method == "POST":
        activityname = request.POST.get('Activity_Name')
        ex_uuid = str(uuid.uuid4())

        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

        cur = conn.cursor()
        cur.execute("set search_path to merahbirudaycare;")
        cur.execute(rf"""
                    INSERT INTO activity (id, name)
                    VALUES (%s, %s);
                    """, [ex_uuid, activityname])
        conn.commit()
        cur.close()
        conn.close()
        return redirect('main:Act_Page')
    return render(request, 'ActivityForm.html')

@csrf_exempt
def Activity_Delete(request, activityid):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                DELETE
                FROM activity
                WHERE id = %s;   
                """, [activityid])


    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT name, id
                FROM activity;   
                """)

    data =  cur.fetchall()
    
    context = {
        'data': data
    }
    conn.commit()
    cur.close()
    conn.close()
    return render(request, 'Activity.html', context)

@csrf_exempt
def Edit_Activity(request, activity_id):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    
        SELECT name
        FROM ACTIVITY
        WHERE id = %s;
    """, [activity_id])
    
    name =  cur.fetchall()
    context = {
        'name': name
    }
    cur.close()
    conn.close()
    
    if request.method == "POST":
        name = request.POST.get('Activity_Name')
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        
            UPDATE activity
            SET name = %s
            WHERE id = %s;
        """, [name, activity_id])
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect('main:Act_Page')
    return render(request, 'EditAct.html', context)

def Admin_Menu(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'AdminMenu.html', context)

def Add_Menu(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'AddMenu.html', context)

def Edit_Menu(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'EditMenu.html', context)

def Offered_Program(request):
    current_year = int(datetime.now().year)
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                    
                    SET search_path TO merahbirudaycare;
                    SELECT DISTINCT P.name, OP.year, OP.monthly_fee, OP.daily_fee,  NOT EXISTS(SELECT * FROM class where (programid,year) = (P.programid, OP.year))
                    FROM Program P
                    JOIN offered_program OP ON P.programid = OP.programid
                    ORDER BY OP.year DESC;
                """)


    data =  cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': data,
        'currentYear': current_year
    }
    cur.close()
    conn.close()

    return render(request, 'OfferedProgram.html', context)

def Delete_Program(request, year, name):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    context = {
        'year': year,
        'name': name,
    }

    cur = conn.cursor()

    # Set the search path
    cur.execute("SET search_path TO merahbirudaycare;")

    # Retrieve the program ID based on the provided name
    cur.execute("SELECT programid FROM Program WHERE name = %s LIMIT 1;", [name])
    program_id = cur.fetchone()

    if program_id:
        # Delete the corresponding entry in the offered_program table
        cur.execute("DELETE FROM offered_program WHERE programid = %s AND year = %s;", [program_id[0], year])

        cur.execute(rf"""
                    SET search_path TO merahbirudaycare;
                    SELECT DISTINCT P.name, OP.year, OP.monthly_fee, OP.daily_fee,  NOT EXISTS(SELECT * FROM class where (programid,year) = (P.programid, OP.year))
                    FROM Program P
                    JOIN offered_program OP ON P.programid = OP.programid
                    ORDER BY OP.year DESC;
                """)

        
        data =  cur.fetchall()
    current_year = int(datetime.datetime.now().year)
    conn.commit()
    cur.close()
    conn.close()

    return render(request, 'OfferedProgram.html', {'data' : data, 'currentYear': current_year,})





def Offer(request, year):

    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'

    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor()
    cur.execute("SET search_path TO merahbirudaycare;")
    cur.execute("SELECT p.name FROM program p WHERE p.programid NOT IN (SELECT programid FROM offered_program WHERE year = %s)", [year])
    programs = cur.fetchall()
    print(programs)
    context = {
        'year': year,
        'program':programs
    }
    cur.close()
    conn.close()
    return render(request, 'OffProg.html', context)

def register_program(request):
    if request.method == "POST":
        current_year = int(datetime.now().year)
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor()
    cur.execute("SET search_path TO merahbirudaycare;")
    name = request.POST.get('Menu_Type')
    Monthly_fee = request.POST.get('MonthlyFee')
    Daily_fee = request.POST.get('DailyFee')
    monthly_fee_value = int(Monthly_fee.replace('Rp', ''))
    daily_fee_value = int(Daily_fee.replace('Rp', ''))
    cur.execute("Select programid from program where name = %s ",[name])
    id = cur.fetchone()
    cur.execute("INSERT INTO offered_program (programid, year, monthly_fee, daily_fee) VALUES (%s, %s, CONCAT('Rp', %s), CONCAT('Rp', %s))", [id, current_year, monthly_fee_value, daily_fee_value])
    cur.execute(rf"""
                    
                    SET search_path TO merahbirudaycare;
                    SELECT DISTINCT P.name, OP.year, OP.monthly_fee, OP.daily_fee,  NOT EXISTS(SELECT * FROM class where (programid,year) = (P.programid, OP.year))
                    FROM Program P
                    JOIN offered_program OP ON P.programid = OP.programid
                    ORDER BY OP.year DESC;
                """)


    data =  cur.fetchall() 
    conn.commit()
    context = {
        'currentYear': current_year,
        'data': data

    }
    cur.close()
    conn.close()
    return render(request,'OfferedProgram.html', context)


def Prog_Detail(request, name, year):
    
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("SET search_path TO merahbirudaycare;")

    cur.execute(rf"""
        SELECT programid FROM Program WHERE name = %s LIMIT 1;
    """, [name])
    program_id = cur.fetchone()
    print(program_id[0])
    print(year)

    cur.execute("""
    
    SELECT A.name, AC.day, AC.start_hour, AC.end_hour
    FROM activity A
    JOIN activity_schedule AC ON AC.activity_id = A.id
    JOIN program P ON AC.programid = P.programid
    WHERE AC.programid = CAST(%s AS UUID) AND AC.year = %s;
""", [program_id[0], year])
 
    data =  cur.fetchall()
    print(data)

    cur.execute("""
    
    SELECT M.name, MS.day, MS.hour
    from menu m
    join menu_schedule ms on m.id = ms.menuid
    where MS.programid = CAST(%s AS UUID) AND MS.year = %s;
""", [program_id[0], year])
    menu = cur.fetchall()
    print(menu)
    conn.commit()
    context = {
        'name': name,
        'class': 'PBP A',
        'year': year,
        'data': data,
        'menu':menu
    }
    cur.close()
    conn.close()

    return render(request, 'ProgDetail.html', context)

def New_ActSched(request, name, year):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("SET search_path TO merahbirudaycare;")
    cur.execute("Select name from activity")
    activity = cur.fetchall()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'act': activity,
        'name': name,
        'year': year,
    }
    cur.close()
    conn.close()
    return render(request, 'ActSched.html', context)

def register_activity(request, name, year):
    if request.method == "POST":
        try: 
            DB_NAME = 'railway'
            DB_USER = 'postgres'
            DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
            DB_HOST = 'monorail.proxy.rlwy.net'
            DB_PORT = '13998'
            conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

            cur = conn.cursor()
            cur.execute("SET search_path TO merahbirudaycare;")
            cur.execute("Select name from activity")
            activity = cur.fetchall()
            act = request.POST.get('Activity_Name')
            print(act)
            cur.execute("SELECT id from activity where name = %s;",[act])
            actid = cur.fetchone()
            print(actid)
            Day = request.POST.get('Day')
            sh = request.POST.get('Start_hour')
            eh = request.POST.get('End_hour')
            cur.execute("Select programid from program where name = %s;",[name]) 
            id = cur.fetchone()  
            cur.execute("Insert into activity_schedule values(%s, %s, %s, %s, %s, %s )",[id,year,Day,sh,eh,actid])     
            cur.execute(rf"""
                SELECT programid FROM Program WHERE name = %s LIMIT 1;
            """, [name])
            program_id = cur.fetchone()
            print(program_id[0])
            print(year)

            cur.execute("""
            
            SELECT A.name, AC.day, AC.start_hour, AC.end_hour
            FROM activity A
            JOIN activity_schedule AC ON AC.activity_id = A.id
            JOIN program P ON AC.programid = P.programid
            WHERE AC.programid = CAST(%s AS UUID) AND AC.year = %s;
        """, [program_id[0], year])
        
            data =  cur.fetchall()
            print(data)

            cur.execute("""
            
            SELECT M.name, MS.day, MS.hour
            from menu m
            join menu_schedule ms on m.id = ms.menuid
            where MS.programid = CAST(%s AS UUID) AND MS.year = %s;
        """, [program_id[0], year])
            menu = cur.fetchall()
            print(menu)
            conn.commit()
            context = {
                'name': name,
                'class': 'PBP A',
                'year': year,
                'data': data,
                'menu':menu
            }
            cur.close()
            conn.close()

            return render(request, 'ProgDetail.html', context)
        except errors.RaiseException as e:
            error_message = str(e)
            print(error_message)
            if "Intersecting duration with another activity schedule." in error_message:
                error_message_to_send = "An activity cant have conflicting schedules with another activity in the same day and program"
                return render(request, 'ActSched.html', {'error_message': error_message_to_send, 'year': year, 'name': name, 'act': activity})
            else:
                return render(request, 'ActSched.html', {'error_message': ' ', 'year': year, 'name': name, 'act': activity})
def New_MenuSched(request, name, year):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("SET search_path TO merahbirudaycare;")
    cur.execute("Select name from menu")
    menu = cur.fetchall()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'menu': menu,
        'name': name,
        'year': year,
    }
    cur.close()
    conn.close()
    return render(request, 'MenuSched.html', context)

def register_menu(request,name,year):
    if request.method == "POST":
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SET search_path TO merahbirudaycare;")
    day = request.POST.get('Day')
    hr1 = request.POST.get('Hour1')
    print(hr1)
    hr2 = request.POST.get('Hour2')
    print(hr2)
    hr3 = request.POST.get('Hour3')
    print(hr3)
    first = request.POST.get('Morning_Snack')
    second = request.POST.get('Lunch')
    Third = request.POST.get('Afternoon_Snack')
    cur.execute("Select id from menu where name = %s",[first])
    idmorn = cur.fetchone()
    cur.execute("Select id from menu where name = %s",[second])
    idlunch = cur.fetchone()
    cur.execute("Select id from menu where name = %s",[Third])
    idafternoon = cur.fetchone()
    cur.execute("Select programid from program where name = %s",[name])
    progid = cur.fetchone()
    cur.execute("Insert into menu_schedule values(%s, %s, %s, %s, %s)",[progid,year,day,hr1,idmorn])
    cur.execute("Insert into menu_schedule values(%s, %s, %s, %s, %s)",[progid,year,day,hr2,idlunch])
    cur.execute("Insert into menu_schedule values(%s, %s, %s, %s, %s)",[progid,year,day,hr3,idafternoon])
    cur.execute(rf"""
        SELECT programid FROM Program WHERE name = %s LIMIT 1;
    """, [name])
    program_id = cur.fetchone()
    print(program_id[0])
    print(year)

    cur.execute("""
    
    SELECT A.name, AC.day, AC.start_hour, AC.end_hour
    FROM activity A
    JOIN activity_schedule AC ON AC.activity_id = A.id
    JOIN program P ON AC.programid = P.programid
    WHERE AC.programid = CAST(%s AS UUID) AND AC.year = %s;
""", [program_id[0], year])
 
    data =  cur.fetchall()
    print(data)

    cur.execute("""
    
    SELECT M.name, MS.day, MS.hour
    from menu m
    join menu_schedule ms on m.id = ms.menuid
    where MS.programid = CAST(%s AS UUID) AND MS.year = %s;
""", [program_id[0], year])
    menu = cur.fetchall()
    print(menu)
    conn.commit()
    context = {
        'name': name,
        'class': 'PBP A',
        'year': year,
        'data': data,
        'menu':menu
    }
    cur.close()
    conn.close()

    return render(request, 'ProgDetail.html', context)


def Class_Page(request):
    context = {}
    phone_number = str(request.user)
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    SELECT userid FROM USERS WHERE phone_number=%s""", [phone_number])
    cgid = cur.fetchall()
    cgid_data = cgid[0][0]
    print(cgid)
    print(cgid_data)
    cur.close()
    cur = conn.cursor()
    cur.execute("""SELECT class_name, year, room_no, programid FROM CLASS WHERE cgid=%s""", [cgid_data])
    data = cur.fetchall()
    print(data)
    context['row'] = []
    context['program_id'] = str(data[0][3])
    for i in range(len(data)):
        context['row'].append((data[i][0], data[i][1], data[i][2]))
    cur.close()
    conn.close()
    return render(request, 'ClassListPage.html', context)

def Children_in_Class_Page(request, class_name = 'a', year = 'a', program_id ='a'):
    context = {
        'class_name': class_name,
        'year': year,
        'program_id': program_id
    }
    phone_number = str(request.user)
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    SELECT total_children FROM CLASS WHERE class_name=%s AND year=%s""", [class_name, year])
    data = cur.fetchall()
    context['total_children'] = data[0][0]
    cur.close()
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT userid, type FROM ENROLLMENT WHERE class=%s AND year=%s""", [class_name, year])
    data2 = cur.fetchall()
    list_user = []
    context['type'] = []
    for i in range(len(data2)):
        list_user.append(data2[i][0])
        context['type'].append(data2[i][1])
    cur.close()
    context['name'] = []
    context['age'] = []
    context['birth_date'] = []
    print(list_user)
    for i in range(len(list_user)):
        cur = conn.cursor()
        cur.execute("""SELECT first_name, last_name, birth_date FROM USERS WHERE userid=%s""", [list_user[i]])
        data3 = cur.fetchall()
        print(data3)
        context['name'].append(data3[0][0] + ' ' + data3[0][1])
        current_age = datetime.strptime(str(data3[0][2]), '%Y-%m-%d')
        context['age'].append(str(2023-current_age.year))
        context['birth_date'].append(data3[0][2])
        cur.close()
    rows = []
    for i in range(len(context['name'])):
        row_data = (context['name'][i], context['age'][i], context['birth_date'][i], context['type'][i])
        rows.append(row_data)
    context['row'] = rows
    context.pop('name', None)
    context.pop('age', None)
    context.pop('birth_date', None)
    context.pop('type', None)
    return render(request, 'ChildreninClassPage.html', context)

def Children_Daily_Report(request, name, year = 'a', class_name = 'a', program_id= 'a'):
    context = {
        'name': name,
        'year': year,
        'class_name': class_name,
        'program_id': program_id
    }
    first_name, last_name = name.split(' ', 1)
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
    SELECT USERID, phone_number FROM USERS WHERE first_name=%s AND last_name=%s""", [first_name, last_name])
    print(first_name)
    print(last_name)
    data = cur.fetchall()
    print(data)
    id_user = data[0][0]
    phone_number = data[0][1]
    cur.close()
    cur = conn.cursor()
    context['row'] = []
    cur.execute("""SELECT date, activity_report, eating_report, link FROM daily_report WHERE class=%s AND year=%s AND userid=%s""", [class_name, year, id_user])
    data2 = cur.fetchall()
    for i in range(len(data2)):
        context['row'].append((data2[i][0], data2[i][1], data2[i][2], data2[i][3]))
    context['phone_number'] = phone_number
    return render(request, 'ChildrenDailyReport.html', context)

@csrf_exempt
def payform(request):
    phone = request.user.phone_number
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        SELECT userid
        FROM users
        WHERE phone_number=%s;
    """, [phone])
    userid =  cur.fetchone()
    print(userid[0])
    cur.close()
    conn.close()

    
    if request.method == "POST":
        try:
            paymentDate = request.POST.get('paymentDate')
            paymentType = request.POST.get('paymentType')
            amount = request.POST.get('amount')
            pay_uuid = str(uuid.uuid4())
            
            DB_NAME = 'railway'
            DB_USER = 'postgres'
            DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
            DB_HOST = 'monorail.proxy.rlwy.net'
            DB_PORT = '13998'
            conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
            cur = conn.cursor()
            cur.execute("""
                        SET SEARCH_PATH TO MERAHBIRUDAYCARE;
                        SELECT DISTINCT E.programid, E.year, E.class, OP.monthly_fee, OP.daily_fee
                        FROM enrollment E
                        LEFT JOIN offered_program OP ON OP.programid=E.programid
                        WHERE E.userid = %s;
                        """, [userid[0]])
            data = cur.fetchone()
            print(data)
            if data != None:
                cur.execute("""
                            INSERT INTO PAYMENT_HISTORY VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """, [pay_uuid, userid, data[0], data[1], data[3], paymentDate, paymentType, 0, amount])
                conn.commit()
                cur.close()
                conn.close()

                return redirect('main:User_Dash')
        except errors.RaiseException as e:
            error_message = str(e)
            print(error_message)
            if "Please pay the fine in exact amount." in error_message:
                error_message_to_send = "please pay the fine first"
                return render(request, 'PayForm.html', {'error_message': error_message_to_send})
            else:
                DB_NAME = 'railway'
                DB_USER = 'postgres'
                DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
                DB_HOST = 'monorail.proxy.rlwy.net'
                DB_PORT = '13998'
                conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
                cur = conn.cursor()
                cur.execute("""
                            SELECT DISTINCT E.programid, E.year, E.class, OP.monthly_fee, OP.daily_fee
                            FROM enrollment E
                            LEFT JOIN offered_program OP ON OP.programid=E.programid
                            WHERE E.userid = %s;
                            """, [userid[0]])
                data = cur.fetchone()
                cur.close()
                conn.close()
                error_message_to_send = "Expected Amount: "
                return render(request, 'ActSched.html', {'error_message': error_message_to_send, 'exp_amt': data[3]})

    return render(request, 'PayForm.html')

def pay_history_admin(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT U.first_name || ' ' ||U.last_name, P.payment_date, P.type, P.fine, P.amount
                FROM payment_history P, users U
                WHERE P.userid=U.userid;
                """)

    data =  cur.fetchall()

    context = {
        'data': data
    }
    cur.close()
    conn.close()

    return render(request, 'PaymentHistoryAdmin.html', context)

def pay_history_user(request):
    phone = request.user.phone_number
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        SELECT userid
        FROM users
        WHERE phone_number=%s;
    """, [phone])
    userid =  cur.fetchone()
    print(userid[0])
    cur.execute(rf"""
                set search_path to merahbirudaycare;
                SELECT P.name, E.year, E.class, PH.payment_date, PH.type, PH.fine, PH.amount
                FROM payment_history PH
                LEFT JOIN enrollment E ON PH.userid=E.userid
                LEFT JOIN program P ON E.programid=P.programid
                WHERE E.userid = %s;
                """, [userid])

    data =  cur.fetchall()
    
    context = {
        'data': data
    }

    cur.close()
    conn.close()

    return render(request, 'PaymentHistoryChild.html', context)

def StaffList(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("set search_path to merahbirudaycare;")
    cur.execute(rf"""
                SELECT u.first_name, u.last_name, s.nik, s.npwp, s.bank_account, s.bank_name
                FROM users u
                JOIN caregiver c ON c.userid = u.userid
                JOIN staff s ON u.userid = s.userid;

                """)
    cgdata = cur.fetchall()
    cur.execute(rf"""
                SELECT u.first_name, u.last_name, s.nik, s.npwp, s.bank_account, s.bank_name
                FROM users u
                JOIN driver d ON d.userid = u.userid
                JOIN staff s ON u.userid = s.userid;

                """)
    drdata = cur.fetchall()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'cgdata': cgdata,
        'drdata': drdata,
    }

    return render(request, 'StaffList.html', context)

def DailyRepForm_Page(request, name, year='a', class_name='a', program_id='a'):
    print(program_id)
    if request.method == 'POST':
        child_name = request.POST.get('child_name')
        first_name, last_name = child_name.split(' ', 1)
        birth_date = request.POST.get('birth_date')
        activity_report = request.POST.get('activity_report')
        eating_report = request.POST.get('eating_report')
        photo_link = request.POST.get('photo_link')
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        SELECT USERID FROM USERS WHERE first_name=%s AND last_name=%s""", [first_name, last_name])
        data = cur.fetchall()
        id_user = data[0][0]
        cur.close()
        cur = conn.cursor()
        cur.execute("""INSERT INTO DAILY_REPORT VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", [id_user, program_id, year, class_name, birth_date, activity_report, eating_report, photo_link])
        conn.commit()
        cur.close()
        conn.close()
        return render(request, 'DailyReportFormPage.html', context)
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'DailyReportFormPage.html', context)

def Admin_Room(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute(rf"""
                    
                    SET search_path TO merahbirudaycare;
                    Select room_no, area, NOT EXISTS(SELECT * FROM class where room_no = r.room_no)  from room r;
                """)


    data =  cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': data,
    }
    cur.close()
    conn.close()

    return render(request, 'AdminRoom.html', context)

def room_delete(request, no, area):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()

    # Set the search path
    cur.execute("SET search_path TO merahbirudaycare;")

    cur.execute("Delete from room where room_no = %s and area = %s;",[no, area])
    cur.execute(rf"""
                    Select room_no, area, NOT EXISTS(SELECT * FROM class where room_no = r.room_no)  from room r;
                """)


    data =  cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': data,
    }
    cur.close()
    conn.close()

    return render(request, 'AdminRoom.html', context)
def Admin_Room_Form(request):

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'AdminRoomForm.html', context)

def register_room(request):
    if request.method == "POST":
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor()
    cur.execute("Set search_path to merahbirudaycare;")
    no = request.POST.get('roomNumber')
    area = request.POST.get('area')
    cur.execute("Insert into room values(%s, %s);",[no, area])
    cur.execute(rf"""
                    Select room_no, area, NOT EXISTS(SELECT * FROM class where room_no = r.room_no)  from room r;;
                """)


    data =  cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': data,
    }
    cur.close()
    conn.close()

    return render(request, 'AdminRoom.html', context)


def ShuttleServiceForm(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'ShuttleServiceForm.html', context)

def ProgramPage(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("Set search_path to merahbirudaycare;")
    cur.execute("Select * from program")
    data = cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'data': data,
    }
    cur.close()
    conn.close()

    return render(request, 'ProgramPage.html', context)

def programpages(request):
    return render(request, 'ProgramFormPage.html')
def ProgramFormPage(request):
    if request.method == "POST":
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

        cur = conn.cursor()
        prog_uuid = str(uuid.uuid4())
        name = request.POST.get("programName")
        minage = request.POST.get("area1")
        maxage = request.POST.get("area2")
        cur.execute("Set search_path to merahbirudaycare;")
        cur.execute("Insert into program values(%s, %s, %s, %s);",[prog_uuid, name, minage, maxage])
        cur.execute("Select * from program")
        data = cur.fetchall()
        print(data)
        conn.commit()
        context = {
            'name': name,
            'class': 'PBP A',
            'data': data,
        }
        cur.close()
        conn.close()

        return render(request, 'ProgramPage.html', context)

def programpagedelete(request, name):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

    cur = conn.cursor()
    cur.execute("Set search_path to merahbirudaycare;")
    cur.execute("Delete from program where name = %s;",[name])
    cur.execute("Select * from program")
    data = cur.fetchall()
    print(data)
    conn.commit()
    context = {
        'name': name,
        'class': 'PBP A',
        'data': data,
    }
    cur.close()
    conn.close()

    return render(request, 'ProgramPage.html', context)

def progeditpage(request, name):
    context = {'name': name}
    return render(request, 'ProgramPageEdit.html', context)

def ProgramPageEdit(request):
    if request.method == "POST":
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

        cur = conn.cursor()
        prog_uuid = str(uuid.uuid4())
        name = request.POST.get("programName")
        minage = request.POST.get("area1")
        maxage = request.POST.get("area2")
        print(minage, maxage)
        cur.execute("Set search_path to merahbirudaycare;")
        cur.execute("UPDATE program SET age_min = %s, age_max = %s WHERE name = %s;", (minage, maxage, name))
        cur.execute("Select * from program")
        data = cur.fetchall()
        print(data)
        conn.commit()
        context = {
            'name': name,
            'class': 'PBP A',
            'data': data,
        }
        cur.close()
        conn.close()

        return render(request, 'ProgramPage.html', context)
@csrf_exempt
def register_admin(request):
    print("enter")
    if request.method == "POST":
        print("enter")
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = User.objects.create_user(phone_number, password)
        user.is_admin = True
        user.save()
        print("account created")
        messages.success(request, 'Your account has been successfully created!')
        return redirect('main:Admin_Dash')
    context = {}
    return render(request, 'r_admin.html', context)
@csrf_exempt
def register_child(request):

    if request.method == "POST":
        phone_number = request.POST.get('parent_phone')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        random_uuid = str(uuid.uuid4())
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        try:
            cur = conn.cursor()
            cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
                INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                """, [random_uuid, password, phone_number, first_name, last_name, gender, dob, address])
            cur.execute("""INSERT INTO CHILD VALUES (%s, %s, %s, %s, %s)""", [random_uuid, father_name, mother_name, father_occupation, mother_occupation])
            cur.execute("""SELECT * FROM USERS;""")
            data = cur.fetchall()
            cur.execute("""SELECT * FROM CHILD;""")
            data2 = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            print(data)
            print(data2)
            user = User.objects.create_user(phone_number, password)
            user.is_child = True
            child = ChildProfile.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, gender=gender, dob=dob, father_name=father_name, father_occupation=father_occupation, mother_name=mother_name, mother_occupation=mother_occupation)
            child.save()
            user.save()
            messages.success(request, 'Your account has been successfully created!')
            authenticated_user = authenticate(request, username=phone_number, password=password)
            login(request, authenticated_user)
            response = HttpResponseRedirect(reverse("main:userPageRender"))
            return response
        except errors.RaiseException as e:
            error_message = str(e)
            print(error_message)
            if "Password must contain at least one uppercase letter AND at least one number" in error_message:
                error_message_to_send = "Password must contain at least one uppercase letter AND at least one number"
                return render(request, 'r_child.html', {'error_message': error_message_to_send})
            else:
                return render(request, 'r_child.html', {'error_message': ' '})
    context = {}
    return render(request, 'r_child.html', context)
@csrf_exempt
def register_caregiver(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        nik = request.POST.get('nik')
        npwp = request.POST.get('npwp')
        bank_name = request.POST.get('bank_name')
        bank_account_number = request.POST.get('bank_account_number')
        random_uuid = str(uuid.uuid4())
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        try:
            cur = conn.cursor()
            cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
                INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                """, [random_uuid, password, phone_number, first_name, last_name, gender, dob, address])
            cur.execute("""INSERT INTO STAFF VALUES (%s, %s, %s, %s, %s)""", [random_uuid, nik, npwp, bank_account_number, bank_name])
            cur.execute("""INSERT INTO CAREGIVER VALUES (%s)""", [random_uuid])
            certificate_count = int(request.POST.get('certificate_count'))
            for i in range(1, certificate_count + 1):
                certificate = Certificate.objects.create(
                    caregiver = caregiver,
                    name=request.POST.get(f'certificate{i}_name'),
                    number=request.POST.get(f'certificate{i}_number'),
                    year=request.POST.get(f'certificate{i}_year'),
                    organizer=request.POST.get(f'certificate{i}_organizer'),
            )
                certificate_name = request.POST.get(f'certificate{i}_name')
                certificate_number = request.POST.get(f'certificate{i}_number')
                certificate_year = request.POST.get(f'certificate{i}_year')
                certificate_organizer = request.POST.get(f'certificate{i}_organizer')
                certificate.save()
                cur.execute("""INSERT INTO CAREGIVER_CERTIFICATE VALUES (%s, %s, %s, %s, %s)""", [random_uuid, certificate_number, certificate_name, certificate_year, certificate_organizer])
            conn.commit()
            cur.close()
            conn.close()
            messages.success(request, 'Your account has been successfully created!')
            user = User.objects.create_user(phone_number, password)
            user.is_caregiver = True
            caregiver = CaregiverProfile.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, gender=gender, dob=dob, nik=nik, npwp=npwp, bank_name=bank_name, bank_account_number=bank_account_number)
            caregiver.save()
            user.save()
            authenticated_user = authenticate(request, username=phone_number, password=password)
            login(request, authenticated_user)
            response = HttpResponseRedirect(reverse("main:userPageRender"))
            return response
        except errors.RaiseException as e:
            error_message = str(e)
            print(error_message)
            if "Password must contain at least one uppercase letter AND at least one number" in error_message:
                error_message_to_send = "Password must contain at least one uppercase letter AND at least one number"
                return render(request, 'r_caregiver.html', {'error_message': error_message_to_send})
            else:
                return render(request, 'r_caregiver.html', {'error_message': ' '})
    context = {}
    return render(request, 'r_caregiver.html', context)
@csrf_exempt
def register_driver(request):
    if request.method == "POST":
        print(request.POST)
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        nik = request.POST.get('nik')
        npwp = request.POST.get('npwp')
        bank_name = request.POST.get('bank_name')
        bank_account_number = request.POST.get('bank_account_number')
        driver_license_number = request.POST.get('driver_license_number')
        selected_days = request.POST.getlist('working_days[]')
        print(selected_days)
        selected_working_days = WorkingDay.objects.filter(day_name__in=selected_days)
        working_days = set(selected_working_days)
        random_uuid = str(uuid.uuid4())
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        try: 
            cur = conn.cursor()
            cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
                INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                """, [random_uuid, password, phone_number, first_name, last_name, gender, dob, address])
            cur.execute("""INSERT INTO STAFF VALUES (%s, %s, %s, %s, %s)""", [random_uuid, nik, npwp, bank_account_number, bank_name])
            cur.execute("""INSERT INTO DRIVER VALUES (%s, %s)""", [random_uuid, driver_license_number])
            for i in range(len(selected_days)):
                print("enter")
                cur.execute("""INSERT INTO DRIVER_DAY VALUES (%s, %s)""", [random_uuid, selected_days[i]])
            conn.commit()
            cur.close()
            conn.close()
            messages.success(request, 'Your account has been successfully created!')
            user = User.objects.create_user(phone_number, password)
            user.is_driver = True
            driver = DriverProfile.objects.create(user=user, first_name=first_name, last_name=last_name, address=address, gender=gender, dob=dob, nik=nik, npwp=npwp, bank_name=bank_name, bank_account_number=bank_account_number, driver_license_number=driver_license_number)
            driver.available_working_days.set(selected_working_days)
            driver.save()
            user.save()
            authenticated_user = authenticate(request, username=phone_number, password=password)
            login(request, authenticated_user)
            response = HttpResponseRedirect(reverse("main:userPageRender"))
            return response
        except errors.RaiseException as e:
            error_message = str(e)
            print(error_message)
            if "Password must contain at least one uppercase letter AND at least one number" in error_message:
                error_message_to_send = "Password must contain at least one uppercase letter AND at least one number"
                return render(request, 'r_driver.html', {'error_message': error_message_to_send})
            else:
                return render(request, 'r_driver.html', {'error_message': ' '})
    context = {}
    return render(request, 'r_driver.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        print("enter login")
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        DB_NAME = 'railway'
        DB_USER = 'postgres'
        DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
        DB_HOST = 'monorail.proxy.rlwy.net'
        DB_PORT = '13998'
        conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
        cur = conn.cursor()
        cur.execute("""SET SEARCH_PATH TO MERAHBIRUDAYCARE;
        SELECT userid FROM USERS WHERE phone_number=%s AND password=%s""", [phone_number, password])
        id_use = cur.fetchall()
        if len(id_use) != 0:
            id_user = id_use[0][0]
        cur.close()
        if id_use:
            print("enter id_use")
            user2 = User.objects.get_or_create(phone_number=phone_number, password=password)
            user = User.objects.get(phone_number=phone_number)
            print(user, "after entering id_use")
            current_user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                print("enter")
                cur = conn.cursor()
                cur.execute("""SELECT userid FROM CHILD WHERE userid=%s """, [id_user])
                check_child = cur.fetchall()
                cur.close()
                if len(check_child) == 1:
                    current_user_role = 'child'
                    user.is_child = True
                cur = conn.cursor()
                cur.execute("""SELECT userid FROM CAREGIVER WHERE userid=%s """, [id_user])
                check_caregiver = cur.fetchall()
                cur.close()
                if len(check_caregiver) == 1:
                    print("this is caregiver")
                    current_user_role = 'caregiver'
                    user.is_caregiver = True
                cur = conn.cursor()
                cur.execute("""SELECT userid FROM DRIVER WHERE userid=%s """, [id_user])
                check_driver = cur.fetchall()
                cur.close()
                if len(check_driver) == 1:
                    current_user_role = 'driver'
                    user.is_driver = True
                user.save()
                login(request, user)
                response = HttpResponseRedirect(reverse("main:userPageRender"))
                return response
        else:
            user = authenticate(request, username=phone_number, password=password)
            if user is not None and user.is_admin == True:
                login(request, user)
                response = HttpResponseRedirect(reverse("main:Admin_Dash"))
                return response
            else:
                messages.info(request, 'Sorry, incorrect username or password. Please try again.')
                context = {'error_message': 'wrong phone number and password'}
                return render(request, 'login.html', context)
    context = {}
    return render(request, 'login.html', context)

def ChildExtra(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, 'ChildExt.html', context)

# main/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
@csrf_exempt
def logout_view(request):
    logout(request)
    # Redirect to the main page or any other desired page
    return redirect('main:show_main')

def pickup_schedule_page(request):
    DB_NAME = 'railway'
    DB_USER = 'postgres'
    DB_PASS = 'C1CfFB-c5fb4feA3eE3FbdECe**-6d36'
    DB_HOST = 'monorail.proxy.rlwy.net'
    DB_PORT = '13998'
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor()
    cur.execute("set search_path to merahbirudaycare;")
    cur.execute(rf"""
        SELECT
            U_child.first_name || ' ' || U_child.last_name AS "Child Name",
            E.pickup_hour AS "Pickup Hour",
            U_driver.first_name || ' ' || U_driver.last_name AS "Driver Name"
        FROM
            merahbirudaycare.users U_child
        JOIN
            merahbirudaycare.enrollment E ON U_child.userid = E.userid
        JOIN
            merahbirudaycare.users U_driver ON E.driverid = U_driver.userid
        WHERE
            E.pickup_hour IS NOT NULL;
    """)

    pickup_schedule_data = cur.fetchall()
    context = {
        'pickup_schedule_data': pickup_schedule_data,
    }

    return render(request, 'PickUpSchedule.html', context)
