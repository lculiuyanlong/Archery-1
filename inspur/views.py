from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.db import connection, OperationalError
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
from sql.engines import get_engine
from sql.utils.resource_group import user_groups, user_instances
from inspur.models import UpdateLog
import simplejson as json

@permission_required('inspur.menu_sqlupdate', raise_exception=True)
def sqlupdate1(request):

    # 获取用户关联实例列表
    instances = [instance_name for instance_name in user_instances(request.user, 'all')]
    if request.POST.get('fiter')=='请输入数据库名称！':
        dbfiter = 'liu'
    elif (request.POST.get('fiter')):
        dbfiter = request.POST.get('fiter')
    else:
        dbfiter='liu'
    print("dbfiter")
    print(dbfiter)
    print(type(dbfiter))
    context = {'instances': instances}
    print(instances)
    print(type(instances))
    print("sqlupdate1获取的实例列表：")
    print(context)
    instance_list = {}
    database = []
    database_list = []
    for instance_name in instances:
            print(instance_name)
            query_engine = get_engine(instance=instance_name)
            db_list = query_engine.get_all_databases()
            if dbfiter=='liu':
                instance_list = {'instance': instance_name, 'database': db_list}
                print(instance_list)
                database_list.append(instance_list)
                print(database_list)
            else:

                for db in db_list:
                    if db == dbfiter:
                        newdb=[]
                        newdb.append(db)
                        instance_list = {'instance': instance_name, 'database': newdb}
                        print(instance_list)
                        database_list.append(instance_list)
                        print(database_list)

    print("获取的database_list如下：")
    print(database_list)
    print(type(database_list))
    return render(request, 'sqlupdate1.html', {'database_list': database_list})

def updatelog_save(username, db_name, instance_name, sql_content, cost_time, sql_result):

    # 成功的查询语句记录存入数据库

    update_log = UpdateLog()
    update_log.username = username
    update_log.db_name = db_name
    update_log.instance_name = instance_name
    update_log.sqllog = sql_content
    update_log.cost_time = cost_time
    update_log.effect_row = sql_result

    # 防止更新超时
    try:
        update_log.save()
    except:
        connection.close()
        update_log.save()


@permission_required('sql.menu_sqlupdate', raise_exception=True)
def updatelog(request):
    # 获取用户信息
    user = request.user

    # limit = int(request.POST.get('limit'))
    # offset = int(request.POST.get('offset'))
    # limit = offset + limit
    search = request.POST.get('search', '')

    # 查询个人记录，超管查看所有数据
    if user.is_superuser:
        sql_log_count = UpdateLog.objects.all().filter(
            Q(sqllog__contains=search) | Q(user_display__contains=search)).count()
        sql_log_list = UpdateLog.objects.all().filter(
            Q(sqllog__contains=search) | Q(user_display__contains=search)).order_by(
            '-id')
    else:
        sql_log_count = UpdateLog.objects.filter(username=user.username).filter(sqllog__contains=search).count()
        sql_log_list = UpdateLog.objects.filter(username=user.username).filter(sqllog__contains=search).order_by('-id')

    # QuerySet 序列化
    sql_log_list = serializers.serialize("json", sql_log_list)
    sql_log_list = json.loads(sql_log_list)
    sql_log = [log_info['fields'] for log_info in sql_log_list]

    result = {"total": sql_log_count, "rows": sql_log}
    # 返回查询结果
    return HttpResponse(json.dumps(result), content_type='application/json')


@permission_required('sql.menu_sqlupdate', raise_exception=True)
def dbfiter(request):
    dbfiter = json.loads(request.POST.get('fiter'))
    print(dbfiter)
    # 获取用户关联实例列表
    instances = [instance_name for instance_name in user_instances(request.user, 'all')]

    context = {'instances': instances}

    # db_name = request.POST.get('db_name')
    # result = {'status': 0, 'msg': 'ok', 'data': []}

    # try:        # 取出该实例的连接方式，为了后面连进去获取所有databases
    instance_list = {}
    database = []
    database_list = []
    while len(database_list) < len(instances):
        for instance_name in instances:
            query_engine = get_engine(instance=instance_name)
            db_list = query_engine.get_all_databases()
            print("+++++++++++++++++++++++++++++++++++++++++++=")
            print("dbfiter")
            print("____________________________")
            print(dbfiter)
            print(db_list)
            for db in db_list:
                if db == dbfiter:
                    instance_list = {'instance': instance_name, 'database': db}
                    print(instance_list)
                    database_list.append(instance_list)
                    print(database_list)
    print("获取的database_list如下：")
    print(database_list)
    print(type(database_list))
    return render(request, 'sqlupdate1.html', {'database_list': database_list})

def updatelog_save(username, db_name, instance_name, sql_content, cost_time, sql_result):

    # 成功的查询语句记录存入数据库

    update_log = UpdateLog()
    update_log.username = username
    update_log.db_name = db_name
    update_log.instance_name = instance_name
    update_log.sqllog = sql_content
    update_log.cost_time = cost_time
    update_log.effect_row = sql_result

    # 防止更新超时
    try:
        update_log.save()
    except:
        connection.close()
        update_log.save()


@permission_required('sql.menu_sqlupdate', raise_exception=True)
def updatelog(request):
    # 获取用户信息
    user = request.user

    search = request.POST.get('search', '')

    # 查询个人记录，超管查看所有数据
    if user.is_superuser:
        sql_log_count = UpdateLog.objects.all().filter(
            Q(sqllog__contains=search) | Q(user_display__contains=search)).count()
        sql_log_list = UpdateLog.objects.all().filter(
            Q(sqllog__contains=search) | Q(user_display__contains=search)).order_by(
            '-id')
    else:
        sql_log_count = UpdateLog.objects.filter(username=user.username).filter(sqllog__contains=search).count()
        sql_log_list = UpdateLog.objects.filter(username=user.username).filter(sqllog__contains=search).order_by('-id')

    # QuerySet 序列化
    sql_log_list = serializers.serialize("json", sql_log_list)
    sql_log_list = json.loads(sql_log_list)
    sql_log = [log_info['fields'] for log_info in sql_log_list]

    result = {"total": sql_log_count, "rows": sql_log}
    # 返回查询结果
    return HttpResponse(json.dumps(result), content_type='application/json')


@permission_required('sql.menu_sqlupdate', raise_exception=True)
def dbfiter(request):
    # dbfiter = request.POST.get('fiter')
    dbfiter = json.loads(request.POST.get('fiter'))
    print(dbfiter)
    # 获取用户关联实例列表
    instances = [instance_name for instance_name in user_instances(request.user, 'all')]
    # slave_instance = [instance_name for instance_name in user_instances(request.user, 'slave')]

    context = {'instances': instances}

    instance_list = {}
    database = []
    database_list = []
    while len(database_list) < len(instances):
        for instance_name in instances:
            query_engine = get_engine(instance=instance_name)
            db_list = query_engine.get_all_databases()
            print("+++++++++++++++++++++++++++++++++++++++++++=")
            print("dbfiter")
            print("____________________________")
            print(dbfiter)
            print(db_list)
            for db in db_list:
                if db == dbfiter:
                    instance_list = {'instance': instance_name, 'database': db}
                    print(instance_list)
                    database_list.append(instance_list)
                    print(database_list)

    print("获取的database_list如下：")
    print(database_list)
    print(type(database_list))
    return render(request, 'sqlupdate1.html', {'database_list': database_list})