# 名词解释

索引：相当于mysql中的表

文档：相当于mysql中的一条记录

es没有库这个概念，相当于所有索引（表）在同一个库中。只不过这个库是分布式的，可以设置分片与备份。

# 索引模板

es插入数据时不要求提前创建索引，如果es发现你的insert语句中的表不存在，它会自动帮你创建这个索引。

es会根据你插入的数据猜测各个字段类型，然后将索引创建出来，然后将本条数据插入。

你当然也可以提前将索引创建好，这样es就会严格按照你所创建的索引来执行插入了，如果待插入的数据格式不符合索引的格式，那么就插入失败。

我们经常遇到这种场景：每天需要一个新的索引，索引结构（各种字段类型）与之前的完全一样，只是索引名字不一样。比如今天创建的索引名字为log-20220714，明天为log-20220715，后天为log-20220716。

难道我们每天都要手动去创建索引么？或者提前将今年一整年的索引都提前创建好？当然不需要，别忘了es有自动创建索引的能力哦，只不过自动创建的时候是靠es猜测的，它有可能会猜错。

所以我们用索引模板来规范es猜测的过程，我们告诉es，如果你要创建名字符合`log-*`模式的索引的话，必须按照我给你的结构来创建。

```json
PUT _index_template/template_name
{
  "index_patterns": ["log-*"],
  "template": {
    "settings": {
      "number_of_shards": 1
    },
    "mappings": {
      "_source": {
        "enabled": true
      },
      "properties": {
        "type": {"type": "integer"},
        "log": {"type": "text"},
        "md5": {"type": "keyword"}
      }
    }
  },
  "priority": 500
}
```



# ILM索引生命周期管理

## rollover原理

ES有3个保存数据的原始文件，分别是`my-log-01  my-log-02  my-log-03`，别名`my-log`指向这3个文件，读取的时候，使用`my-log`会读取这三个文件，写入的时候，使用`my-log`会只写入`my-log-03`，因为设置别名的时候需要指定`写别名`，`写别名`只能指向1个原始文文件。

rollover的原理是，创建一个新的索引，然后将`写别名`指向这个新的索引。

## 索引生命周期

hot：这个阶段不受索引生命周期控制，只受rollover控制

warm：非`写别名`指向的索引，多长时间转为warm

clod：非`写别名`指向的索引，多长时间转为clod

delete：非`写别名`指向的索引，多长时间转为delete



es每隔10分钟，扫描一下被ILM管理的索引，如果索引的状态（数据大小、时间、文档数量）到达设置的值，则创建新的索引，将写别名指向新索引，取消旧索引的写别名。这样以后的数据就只会写到新的索引了。

```json
// 将索引生命周期的检查间隔设置为10S，默认是10分钟
PUT _cluster/settings
{
    "persistent": {
      "indices.lifecycle.poll_interval": "10s"
    }
}

// 创建ILM策略
PUT _ilm/policy/tanght_ilm_policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "set_priority": {
            "priority": 100
          },
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "30d",
            "max_docs": 5
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 50
          }
        }
      }
    }
  }
}

// 创建索引模板 在索引模板中使用刚刚创建好的ILM策略
PUT _index_template/tanght_index_template
{
  "index_patterns": ["tanght-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "tanght_ilm_policy",
      "index.lifecycle.rollover_alias": "tanght",
      "index.default_pipeline": "add_ts"
    },
    "mappings": {
      "_source": {
        "enabled": true
      },
      "properties": {
        "type": {"type": "integer"},
        "log": {"type": "text"},
        "md5": {"type": "keyword"},
        "@timestamp": {"type": "date"}
      }
    }
  }
}

// 创建初始索引并定义别名
// ILM主要负责创建新索引，将别名指向新索引，将新索引别名is_write_index设置为true，将旧索引的is_write_index设置为false
PUT tanght-000001
{
  "aliases": {
    "tanght": {
      "is_write_index": true
    }
  }
}
```





# Data Stream

```json

// 将索引生命周期的检查间隔设置为10S，默认是10分钟
PUT _cluster/settings
{
    "persistent": {
      "indices.lifecycle.poll_interval": "10s"
    }
}

// 创建ILM策略
PUT _ilm/policy/tanght_ilm_policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "set_priority": {
            "priority": 100
          },
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "30d",
            "max_docs": 5
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 50
          }
        }
      }
    }
  }
}

// 创建索引模板 在索引模板中使用刚刚创建好的ILM策略
PUT _index_template/tanght_index_template
{
  "index_patterns": ["tanght*"],
  "data_stream": { },
  "template": {
    "settings": {
      "index.lifecycle.name": "tanght_ilm_policy",
      "index.default_pipeline": "add_ts"
    },
    "mappings": {
      "_source": {
        "enabled": true
      },
      "properties": {
        "type": {"type": "integer"},
        "log": {"type": "text"},
        "md5": {"type": "keyword"},
        "@timestamp": {"type": "date"}
      }
    }
  }
}

// 创建data stream
PUT _data_stream/tanght

// 向data stream中插入数据
POST /tanght/_doc/
{
  "log": "abc def haha",
  "md5": "assafsfgdfg",
  "type": 1
}

// 从data stream中查询数据
// 跟从普通索引中查数据是一样的
GET /tanght/_search
```



# FileBeat

```yaml
filebeat.inputs:
  - type: filestream
    id: log-a
    enabled: true
    paths:
      - /root/aaa/a*.log
    fields:
      log_type: "nginx"
    tags: ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
    fields_under_root: true

  - type: filestream
    id: log-b
    enabled: true
    paths:
      - /root/aaa/b*.log
    tags: ["bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"]

processors:
  - drop_fields:
      fields: ["input", "host", "agent", "ecs", "log"]
      ignore_missing: true


output.console:
  pretty: true
  enable: true


# output.elasticsearch:
#   enable: true
#   hosts: ["https://192.168.9.63:9200"]
#   username: "elastic"
#   password: "a*_+krCmmMKf*LR-dcbt"
#   ssl.certificate_authorities:
#     - C:\Users\tanght\Desktop\http_ca.crt
#   allow_older_versions: true
#   indices:
#     - index: "abc"
#       when.contains:
#         tags: "log-a"
#     - index: "deg"
#       when.contains:
#         tags: "log-a"


# # setup.template.enable: false
# setup.template.name: "template_name_tht2"
# setup.template.pattern: "template_name_tht2*"

```









```
POST /nginxlog/_doc/?pipeline=filebeat_nginx
{
  "message": "[27/Oct/2022:23:03:29 +0700] 1666970785.520 10.251.1.60 [POST /v1//background/msg_data/ HTTP/1.0] 18 19 20 21 22 23"
}
```





# 权限管理

es添加用户

```shell
# 创建一个新用户 -p指定密码, 密码不能全是数字
/bin/elasticsearch-users useradd xxxname -p a123456
# 给用户添加超级管理
/bin/elasticsearch-users roles -a superuser xxxname
# 给用户添加kibana，此用户可以通过kibana连接es
/bin/elasticsearch-users roles -a kibana_system xxxname
```



# Kibana

```shell
docker run -d --name kibana --network docker_ragflow -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01:9200" -e "ELASTICSEARCH_USERNAME=tht1" -e "ELASTICSEARCH_PASSWORD=a123456" kibana:8.11.3
```







# 安装

```shell
# 1. 创建网络环境
docker network create elastic

# 2. 运行es
docker run --name elastic-es01 --net elastic -p 9200:9200 -it -m 1GB elasticsearch:8.17.4

# 3. 从屏幕信息中找到 Password 和 enrollment token
# 屏幕中将出现下列日志，从日志中找到 Password 和 enrollment token
# 将 enrollment token 填写到 kibana 页面上
# 然后使用 用户名:elastic 密码: xxx 进行登录
# ✅ Elasticsearch security features have been automatically configured!
# ✅ Authentication is enabled and cluster connections are encrypted.

# ℹ️  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
#   +4ArfA3WhuFc9+sPQx5d

# ℹ️  HTTP CA certificate SHA-256 fingerprint:
#   531d30a58ca0b748a5a4f0366f91e2a302ced28ade2f1145af52842164d6f565

# ℹ️  Configure Kibana to use this cluster:
# • Run Kibana and click the configuration link in the terminal when Kibana starts.
# • Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
#   eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTcyLjE5LjAuMjo5MjAwIl0sImZnciI6IjUzMWQzMGE1OGNhMGI3NDhhNWE0ZjAzNjZmOTFlMmEzMDJjZWQyOGFkZTJmMTE0NWFmNTI4NDIxNjRkNmY1NjUiLCJrZXkiOiJwVnEyQ1pZQjlHZkk1TjJxc2RLajpwMHE3MlRWVFNXYVEyTVdLdnJpRld3In0=

# ℹ️ Configure other nodes to join this cluster:
# • Copy the following enrollment token and start new Elasticsearch nodes with `bin/elasticsearch --enrollment-token <token>` (valid for the next 30 minutes):
#   eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTcyLjE5LjAuMjo5MjAwIl0sImZnciI6IjUzMWQzMGE1OGNhMGI3NDhhNWE0ZjAzNjZmOTFlMmEzMDJjZWQyOGFkZTJmMTE0NWFmNTI4NDIxNjRkNmY1NjUiLCJrZXkiOiJwMXEyQ1pZQjlHZkk1TjJxc2RLajp3RGdocWRhQ1FyeUlyTHNqMERqSjR3In0=

#   If you're running in Docker, copy the enrollment token and run:
#   `docker run -e "ENROLLMENT_TOKEN=<token>" docker.elastic.co/elasticsearch/elasticsearch:8.17.4`

# 4. 启动 Kibana
docker run --name elastic-kib01 --net elastic -p 5601:5601 kibana:8.17.4

# 5. 屏幕出现如下信息，使用浏览器 Go to http://0.0.0.0:5601/?code=347626
# Kibana is currently running with legacy OpenSSL providers enabled! For details and instructions on how to disable see https://www.elastic.co/guide/en/kibana/8.17/production.html#openssl-legacy-provider
# {"log.level":"info","@timestamp":"2025-04-06T06:46:06.486Z","log.logger":"elastic-apm-node","ecs.version":"8.10.0","agentVersion":"4.10.0","env":{"pid":7,"proctitle":"/usr/share/kibana/bin/../node/glibc-217/bin/node","os":"linux 5.15.167.4-microsoft-standard-WSL2","arch":"x64","host":"c0c254481b25","timezone":"UTC+00","runtime":"Node.js v20.18.2"},"config":{"active":{"source":"start","value":true},"breakdownMetrics":{"source":"start","value":false},"captureBody":{"source":"start","value":"off","commonName":"capture_body"},"captureHeaders":{"source":"start","value":false},"centralConfig":{"source":"start","value":false},"contextPropagationOnly":{"source":"start","value":true},"environment":{"source":"start","value":"production"},"globalLabels":{"source":"start","value":[["git_rev","57a32881bd4c7055491b10f3c957e7dcef2f1bf0"]],"sourceValue":{"git_rev":"57a32881bd4c7055491b10f3c957e7dcef2f1bf0"}},"logLevel":{"source":"default","value":"info","commonName":"log_level"},"metricsInterval":{"source":"start","value":120,"sourceValue":"120s"},"serverUrl":{"source":"start","value":"https://kibana-cloud-apm.apm.us-east-1.aws.found.io/","commonName":"server_url"},"transactionSampleRate":{"source":"start","value":0.1,"commonName":"transaction_sample_rate"},"captureSpanStackTraces":{"source":"start","sourceValue":false},"secretToken":{"source":"start","value":"[REDACTED]","commonName":"secret_token"},"serviceName":{"source":"start","value":"kibana","commonName":"service_name"},"serviceVersion":{"source":"start","value":"8.17.4","commonName":"service_version"}},"activationMethod":"require","message":"Elastic APM Node.js Agent v4.10.0"}
# Native global console methods have been overridden in production environment.
# [2025-04-06T06:46:08.318+00:00][INFO ][root] Kibana is starting
# [2025-04-06T06:46:08.368+00:00][INFO ][node] Kibana process configured with roles: [background_tasks, ui]
# [2025-04-06T06:46:17.907+00:00][INFO ][plugins-service] The following plugins are disabled: "cloudChat,cloudExperiments,cloudFullStory,dataUsage,investigateApp,investigate,profilingDataAccess,profiling,searchHomepage,searchIndices,securitySolutionServerless,serverless,serverlessObservability,serverlessSearch".
# [2025-04-06T06:46:17.980+00:00][INFO ][http.server.Preboot] http server running at http://0.0.0.0:5601
# [2025-04-06T06:46:18.106+00:00][INFO ][plugins-system.preboot] Setting up [1] plugins: [interactiveSetup]
# [2025-04-06T06:46:18.123+00:00][INFO ][preboot] "interactiveSetup" plugin is holding setup: Validating Elasticsearch connection configuration…
# [2025-04-06T06:46:18.149+00:00][INFO ][root] Holding setup until preboot stage is completed.


# i Kibana has not been configured.

# Go to http://0.0.0.0:5601/?code=347626 to get started.

# 6. 在页面中输入 enrollment token

# 7. 在页面中输入 用户名+密码

```



如果启动es的时候在屏幕日志中找不到password和enrollment token，可以通过下列方法重新生成

```shell
# 重新创建 password
docker exec -it elastic-es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

# 重新创建 enrollment token
docker exec -it elastic-es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

