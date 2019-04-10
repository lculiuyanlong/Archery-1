from django.shortcuts import render
from sql.utils.resource_group import user_groups, user_instances
from django.contrib.auth.decorators import permission_required
from sql.engines import get_engine

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
            print(query_engine)
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
