# ros_dns_helper
公开抄袭的肉丝dns脚本，支持分流

1、启动  python3 maintain_domain
2、访问 http://你的ip:端口，端口在conf.json中
3、功能
   a 点击执行可以生成ros7的import文件，import文件的作用是设置ros的dns fw到另外一个ip
     当然，需要配合你的ros上的安全上网的通道
   b 可以自己在gfwlist的基础上添加域名，添加奈飞分流域名
   c 域名解析自动存入gfw_list或是nf_list的addresslist 方便您mark route
   d ros上设置下 dnsserver 的环境变量为你的特殊dns server
