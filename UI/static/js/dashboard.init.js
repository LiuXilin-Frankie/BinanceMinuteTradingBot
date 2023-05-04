
!function($) {
  "use strict";

  var Dashboard = function() { 
        this.$body = $("body")
        };
  

   
    //左边更新OP表格
     Dashboard.prototype.show_OP = function(data) {
     
     var data_arry = [];
     for (let i in data){
     data_arry.push(JSON.parse(JSON.stringify(data[i])));//深拷贝
     }

           var tb = document.getElementById("operationhistory");//获取网页元素
           //当页面上的表格长度不等于最新数据长度时，删除整个表格，重新赋值
           
        //更新表格内容
          if (Object.keys(data).length != (tb.rows.length -1)){
          while(tb.rows.length>1){
          tb.rows[1].remove();}; 
          for(var i=0;i<data_arry.length;i++){
          var row = tb.insertRow(tb.FetchRowCount);
          row.insertCell(0).innerHTML = i+1;
          row.insertCell(1).innerHTML = data[i][0];
          row.insertCell(2).innerHTML = data[i][1];
          row.insertCell(3).innerHTML = data[i][2];
          row.insertCell(4).innerHTML = data[i][3];
          }}
          //如果长度和表格一致，就只修改表格内容
          
          else
          {for(var i=0;i<data_arry.length;i++){
          tb.rows[i+1].cells[0].innerHTML = i+1;
          tb.rows[i+1].cells[1].innerHTML = data[i][0];
          tb.rows[i+1].cells[2].innerHTML = data[i][1];
          tb.rows[i+1].cells[3].innerHTML = data[i][2];
          tb.rows[i+1].cells[4].innerHTML = data[i][3];
          }}
        },
    

     //右边更新TCA表格
     Dashboard.prototype.show_TCA = function(data) {
     
     var data_arry = [];
     for (let i in data){
     data_arry.push(JSON.parse(JSON.stringify(data[i])));//深拷贝
     }
           var tb = document.getElementById("TCA");//获取网页元素
           //当页面上的表格长度不等于最新数据长度时，删除整个表格，重新赋值   
        //更新表格内容
          if (Object.keys(data).length != (tb.rows.length -1)){
          while(tb.rows.length>1){
          tb.rows[1].remove();};
          for(var i=0;i<data_arry.length;i++){
          var row = tb.insertRow(tb.FetchRowCount);
          row.insertCell(0).innerHTML = i+1;
          row.insertCell(1).innerHTML = data[i][0];
          row.insertCell(2).innerHTML = data[i][1];
          }}
          //如果长度和表格一致，就只修改表格内容
          else
          {for(var i=0;i<data_arry.length;i++){
          
       //   var account_name = data_arry[i]["account"];
          
          tb.rows[i+1].cells[0].innerHTML = i+1;
          tb.rows[i+1].cells[1].innerHTML = data[i][0];
          tb.rows[i+1].cells[2].innerHTML = data[i][1];
          }}
          },


        Dashboard.prototype.getData_operation_history = function() {
        //op数据表格接口
         var data_oh = 0;
       function get_oh() {
                $.ajax({
                    type: "GET",
                    url: "/get_operationhistory",//数据地址
                    dataType: "json",
                    contentType: "application/json",
                    headers:{ 'Content-Type':'application/json;charset=utf8','organId':'1333333333'},
                    async: false,
                    success: function (result) {  
                    data_oh = result;},
                    error: function () {
                    console.log( "Get operationhistory Failed!");}
                });
                return data_oh;
            }
            get_oh();
            return data_oh
            
            },   


    
     Dashboard.prototype.getData_TCA = function() {
     //交易成分析数据接口
         var data_TCA = 0 ;
       function get_TCA() {
                $.ajax({
                    type: "GET",
                    url: "/get_TCA",//数据地址
                    dataType: "json",
                    contentType: "application/json",
                    headers:{ 'Content-Type':'application/json;charset=utf8','organId':'1333333333'},
                    async: false,
                    success: function (result) {  
                    data_TCA = result},
                    error: function () {
                    console.log( "Get TCA Failed!");}
                });
                return data_TCA;
            }
            get_TCA();
            return data_TCA
            },   

    
  
    //end plot graph
  
        //  前面已经写好了数据显示的格式 和 获取数据的接口， 下面是启动展示和交互的初始化部分
        //initializing various charts and components
        Dashboard.prototype.init = function() {
            //real time data representation
         this.show_OP(this.getData_operation_history()); //定义图像对象 传入数据
         this.show_TCA(this.getData_TCA()); //定义图像对象 传入数据
         
            var $this = this;
            
            function updatePlot() { //实时更新函数

                 $this.show_OP($this.getData_operation_history());//左边表格
                $this.show_TCA($this.getData_TCA());//右边表格

                setTimeout(updatePlot, $( 'html' ).hasClass( 'mobile-device' ) ? 1000 : 1000); //循环刷新
            }
            updatePlot();
        },

    //init Dashboard
    $.Dashboard = new Dashboard, $.Dashboard.Constructor = Dashboard

}(window.jQuery),

//initializing Dashboard
function($) {
    "use strict";
    $.Dashboard.init()
}(window.jQuery);
