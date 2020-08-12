#mysql

#登录mysql的root用户
mysql -u root -p
#输入密码
......

#修改root密码为‘root’
update user set password=password('root') where user = 'root';

#新建jgs数据库
create database jgs;

#mysql操作结束



#Python3.7

#安装库（未说明的直接用pip安装最新版）
django=2.2, mysqlclient

#安装命令
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django==2.2
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple mysqlclient

#Python操作结束


#django2.2

#启动
#转到backend目录下
python manage.py runserver 端口号

#激活模型
#创建迁移文件
python manage.py makemigrations
#执行迁移
python manage.py migrate
#注意：任何对模型的修改都需要重新迁移

#django操作结束


#待更新……

