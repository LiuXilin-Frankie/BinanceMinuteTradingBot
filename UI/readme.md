### web端实时监控交易
#### 功能：
显示最近300S（交易时间）的净值走势  
展示最近10条交易操作，每秒刷新  
展示最近的交易成本分析指标，每秒更新

#### 部署
保持文件相对路径，主要是三大部分:backend.py+templates(网页)+static(静态文件)  
三种需要展示的数据 以需要的更新频率 写入到相应log文件里，格式与sample保持一致  
在本地运行UI_backend.py  
使用浏览器访问http://本地IP地址:1122/dashboard 即可  (请使用无痕模式！！！)  
如需查看动态效果，可运行UI_backend_randomdata.py
