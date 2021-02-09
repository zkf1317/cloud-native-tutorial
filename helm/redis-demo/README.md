## 本示例支持的发行版
- ubuntu 20.04.1 LTS

## 操作步骤
### 安装helm
```bash
chmod +x install-helm.sh
./install-helm.sh
```

### 添加仓库并找到redis chart
1.添加仓库: 这一步时间可能比较久，请耐心等待
```bash 
helm repo add stable https://charts.helm.sh/stable
```

2.查看已经添加的仓库
```bash 
helm repo list
```

3.搜索仓库有哪些chart
```bash 
helm search repo stable
```

4.更新仓库列表到本地
```bash
helm repo update
```

5.搜索redis
```bash 
helm search repo redis
```

6.查看redis chart详情
```bash 
helm show chart stable/redis
```

7.查看redis values（values：相当于chart的配置文件）
```bash
helm show values stable/redis
```

### redis chart安装/升级/回滚/卸载
1.建立单master的配置文件，名为only-master.values

2.--dry-run一下，看看生成出来的yaml文件是否存在问题
```bash
helm install redis-demo stable/redis -f ./only-master.values --dry-run
```

3.如果没有问题，则进行实际的安装
```bash
helm install redis-demo stable/redis -f ./only-master.values
```

4.安装成功之后，可以登录redis进行操作，做进一步的校验
```bash
redis-cli -h `kubectl get svc redis-demo-master -o=jsonpath="{.spec.clusterIP}"` -a admin
set name zhangsan
get name
info replication
# 可以看到这时候没有slave连接
```

5.建立master-slave配置文件，名为master-slave.values

6.--dry-run一下，看看生成出来的yaml文件是否存在问题; 由于在系统中已经有redis-demo的release，因此使用upgrade来进行升级
```bash
helm upgrade redis-demo stable/redis -f ./master-slave.values --dry-run
helm upgrade redis-demo stable/redis -f ./master-slave.values
```

7.检查slave是否安装成功，以及是否同步成功
```
redis-cli -h `kubectl get svc redis-demo-slave -o=jsonpath="{.spec.clusterIP}"` -a admin
get name
```

8.最后，回滚至单master模式
- 查看部署历史: ```helm history redis-demo```
- 回滚到对应的单master版本: ```helm rollback redis-demo REVISION```
- 再连接slave已经不成功了
```bash
redis-cli -h `kubectl get svc redis-demo-slave -o=jsonpath="{.spec.clusterIP}"` -a admin
```
- 只有master能连接
```bash
redis-cli -h `kubectl get svc redis-demo-master -o=jsonpath="{.spec.clusterIP}"` -a admin
# 测试一下
get age
```

9.卸载redis-demo
```bash
helm uninstall redis-demo
```