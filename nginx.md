```nginx

#user  nobody;
worker_processes  1;   #设置值和CPU核心数一致，开启多少个子进程

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;

events {
	#use epoll;     #事件驱动模型
    worker_connections  2048;
    accept_mutex on;
    multi_accept on; 
}



http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;
    #keepalive_timeout  0;
    keepalive_timeout  65;
    gzip  on;
	
	#在一次长连接上所允许请求的资源的最大数量
    keepalive_requests 3;
	#resolver 127.0.0.1;
	
	#负载均衡模组入口，网页访问入口 http://localhost:8072
	server {
		listen  8072;
		server_name  localhost;
		location / {
			proxy_pass http://server_group/;  #请求转向server_group定义的服务器列表
		}
	}
	#负载均衡模组
	upstream server_group {	   
	    # weight;     #轮询，默认就是轮询
		#ip_hash;   #同一个IP的访客固定访问一个后端服务器
		#	server 192.168.123.1:80 	 weight=4 max_fails=2 fail_timeout=30s;
		#	server 192.168.10.121:3333 backup;  #热备
		#weigth参数表示权值，权值越高被分配到的几率越大
		server 127.0.0.1:8076 	weight=4 max_fails=2 fail_timeout=30s;
		server 127.0.0.1:8083    	weight=4 max_fails=2 fail_timeout=30s;
		server 127.0.0.1:8086    	weight=4 max_fails=2 fail_timeout=30s;
	}	

    server {
	    #安标建web项目
        listen       8092;
        server_name  localhost;

        #charset koi8-r;
        #access_log  logs/host.access.log  main;
		
		#前端html
		location / {
			root D:\IIS_Publish\an.biao.jian.web.front;   #静态页面根目录
            index index.html;   #首页
        }

		#后台webapi
		location /abj_api/ {
		    #代理转发请求
			proxy_pass  http://localhost:8084/abj_api/;     # 注：proxy_pass的结尾有/,效果：会在请求时将/abj_api/*后面的路径直接拼接到后面
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
       #error_page   500 502 503 504  /50x.html;
       #location = /50x.html {
       #    root   html;
       #}

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

    }

    # nginx状态页  http://localhost:8000/nginx_status
    server {
        listen  *:8000; 
        server_name  www.nginxcheck.com;
	    location /nginx_status {
		    stub_status;
		  #  allow 127.0.0.1;
		  #  deny all;
	    }
    }
	
	    #html测试页面，测试跨域
		server {
			listen  9000; 
			server_name  localhost;
			#前端html
			location / {
				root D:\IIS_Publish\ceshi.kuayu;   #静态页面根目录
				index index.html;   #首页
			}
		}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}
	

}


```

# root与alias的区别

```nginx
{
	location /haha/ {
                alias /home/tanght/www/;
            }
}
```

前端访问/haha/123.html，服务器就会将/home/tanght/www/123.html文件发送给前端

```nginx
{
	location /haha/ {
                root /home/tanght/www/;
            }
}
```

前端访问/haha/123.html，服务器就会将/home/tanght/www/haha/123.html文件发送给前端

也就是说，root的话，url会被当成路径的一部分

http://www.tanght.xyz:8266/about



# 源码分析

