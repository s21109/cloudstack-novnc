cloudstack-novnc
================
CloudStack 的VNC除了浏览器兼容性能好一点，其他的体验都不是很好，利用retspen的webvirtmgr小改了一版。<br> 
https://github.com/retspen/webvirtmgr <br> 
mkdir  -p /var/www;cd /var/www <br> 
wget https://github.com/s21109/cloudstack-novnc/archive/master.zip <br> 
unzip master.zip<br> 
cd cloudstack-novnc-master<br> 
rpm -ivh  http://mirrors.hustunique.com/epel/6/x86_64/epel-release-6-8.noarch.rpm<br> 
sudo yum -y install git python-pip libvirt-python libxml2-python python-websockify supervisor nginx -y<br> 
sudo python-pip install -r requirements.txt<br> 
touch  /etc/nginx/conf.d/webvirtmgr.conf<br> 

#添加内容
vim   /etc/nginx/conf.d/webvirtmgr.conf <br> 
<pre>
server {
    listen 80 default_server;
    server_name $hostname;
    #access_log /var/log/nginx/webvirtmgr_access_log;
    location /static/ {
        root /var/www/xiangcloudvirtmgr/xiangcloud; # or /srv instead of /var
        expires max;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Forwarded-Proto $remote_addr;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        client_max_body_size 1024M; # Set higher depending on your needs 
    }
}
</pre>
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak <br> 
sudo  chkconfig nginx on <br> 
sudo chown -R nginx:nginx /var/www/xiangcloudvirtmgr <br> 
sudo service nginx restart <br> 
vim /etc/supervisord.conf <br> 
#Add these lines to end of file /etc/supervisord.conf <br> 
<pre>
[program:webvirtmgr]
command=/usr/bin/python /var/www/xiangcloudvirtmgr/manage.py run_gunicorn -c /var/www/xiangcloudvirtmgr/conf/gunicorn.conf.py
directory=/var/www/xiangcloudvirtmgr
autostart=true
autorestart=true
logfile=/var/log/supervisor/webvirtmgr.log
log_stderr=true
user=nginx

[program:webvirtmgri-novnc]
command=/usr/bin/python /var/www/xiangcloudvirtmgr/console/webvirtmgr-novnc
directory=/var/www/xiangcloudvirtmgr
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/webvirtmgr-nonvc.log
redirect_stderr=true
user=nginx
</pre>
sudo service supervisord restart <br> 
chkconfig supervisord on <br> 
#查看novnc服务是否启动
netstat -anp|grep 6080 <br> 
/sbin/iptables -A INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT <br> 
iptables-save > /etc/sysconfig/iptables <br> 
service iptables restart <br> 
#JAVA 调用
Base64依赖库版本 <br> 

<dependency> <br> 
        <groupId>commons-codec</groupId> <br> 
        <artifactId>commons-codec</artifactId> <br> 
        <version>1.9</version> <br> 
</dependency> <br> 

<pre>
@RequestMapping(method = RequestMethod.GET)
public String openvnc(ServletRequest request) {
        String token = null;
        try {
                String host = "192.168.30.59"; //测试宿主机的IP地址
                String instance = "i-2-176-VM"; //测试虚机的instance name
                String display = "test";  //Novnc 显示的title
                String str = host +"|"+instance+"|"+display;
                token = Base64.encodeBase64String(str.getBytes());
        } catch (Exception e) {
                e.printStackTrace();
        }
        return  "redirect:http://192.168.30.57/console/?token="+token;
}
</pre>

#Django 调用
<pre>
function open_vnc() {
    window.open('{% url 'console' %}?token={{token}}', '', 'width=850,height=485')
}
</pre>
