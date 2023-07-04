# ros_dns_helper
批量导入ros的dns列表，该列表解析fwd到您指定的dns server</br>

脚本全程抄袭，遵循被抄袭对象的所有协议</br>

原理阐述<br>

routeos的dns服务器本身支持把域名解析forward到另外一个dns服务器，语法为： </br>

```ip dns static add forward-to=8.8.8.8 type=FWD address-list=your_address_list match-subdomain=yes  name=1-apple.com.tw```</br>

其中address-list应该是ros 7.x的新特性，即把解析的结果加入到 /ip/firewall/adresslist中名为 your_address_list的列表中

为了让它好好的工作，我们需要做两件事情</br>

0、假设你自己做好了一个安全的路由，这个路由一定要支持payload加密(否则被投毒), 这个路由名字叫做 vip_route</br>

1、把到8.8.8.8的流量mark一下，走vip通道 </br>

   mark ros本身到 8.8.8.8的流量</br>
   ` chain=output action=mark-routing new-routing-mark=vip_route 
      passthrough=no dst-address=8.8.8.8 log=no log-prefix="121" `</br>

   mark ros内网到 8.8.8.8的流量</br>
   ` chain=prerouting action=mark-routing new-routing-mark=vip_route 
      passthrough=no dst-address=8.8.8.8 log=no log-prefix="121" `</br>

2、如果想实现匹配域名列表的ip自动走vip通道，在去mangle里面 mark一下route</br>

     chain=prerouting action=mark-routing new-routing-mark=vip_route
      passthrough=no src-address=192.168.0.0/16 dst-address=!192.168.0.0/16 
      dst-address-list=your_address_list log=no log-prefix="vip_log" ```</br>

重锁周知，需要处理的域名列表太多太麻烦，为此提供了一个工具可以干这活</br>

1、简单看下conf.json 启动  python3 maintain_domain</br>

2、访问 http://你的ip:端口，端口在conf.json中</br>

3、功能</br>

   a 点击执行可以生成ros7的import文件</br>

     import文件您可以稍微阅读一下，就是实现了一堆域名的添加而已

   b 可以自己在gfwlist的基础上添加域名，添加奈飞分流域名</br>

   c 域名解析自动存入gfw_list或是nf_list的addresslist 方便您mark route<br>

   d fwd的dnsserver 为conf.json中的</br>

建议这个工具部署在外网

