# 测试验证 istio locality load balance
## 需求来源
当集群跨zone或region部署时，服务间的调用需要跨zone甚至region，会导致延迟增大，zone或region之间的专线带宽占用，等后果。   
因此调用需要优先发生在zone或region内部。  

## 实验描述
模拟在不同region/zone的服务，调用发生在region/zone内的场景
### 实验步骤
参照：https://betterprogramming.pub/locality-based-load-balancing-in-kubernetes-using-istio-a4a9defa05d3  

# 参考资料
- https://istio.io/latest/docs/reference/config/networking/destination-rule/#LocalityLoadBalancerSetting-Distribute  
- https://betterprogramming.pub/locality-based-load-balancing-in-kubernetes-using-istio-a4a9defa05d3  
