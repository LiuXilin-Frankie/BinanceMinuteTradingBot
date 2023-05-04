/*
 Template Name: Zegva - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesdesign
 Website: www.themesdesign.in
 File: C3 Chart init js
 */
function Data_init(code){

!function($) {
    "use strict";

    var ChartC3 = function() {};

    ChartC3.prototype.init = function () {
          var data_ = 0
        $.ajax({
            type: "POST",
            url: "/rates_history",
            dataType: "json",
            contentType: "application/json",
            data:JSON.stringify({"account":code,"password":"123"}),
            headers:{'Content-Type':'application/json;charset=utf8','organId':'1333333333'},
            async: false,
            success: function (result) {  
            data_ = result;
            },
            error: function () {
            console.log("Get Rand Name Failed!");}
        });
                
        console.log(data_)        
        console.log(Object.keys(data_).length)
        var data_columns = [];
        for (var i =0;i<Object.keys(data_).length;i++){
        data_columns.push(data_[i]);

        }
        
        console.log(data_columns)


        //combined chart
        c3.generate({
            bindto: '#combine-chart',
            data: {
                x:'x',
                columns: data_columns
            },
            axis: {
                x: {
                    tick:{
                    values:data_columns[0].slice(1)},
                    type: 'timeseries'
                }
            }
        });
        
      


    },
    $.ChartC3 = new ChartC3, $.ChartC3.Constructor = ChartC3

}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.ChartC3.init()
}(window.jQuery);
}

var code;

     
 function set_ID(){
 code = document.getElementById("initial").value;
 code =  String(code);
 sessionStorage.setItem("account", code)
 console.log("获取了code")
 console.log(sessionStorage.getItem("account"))
 location.reload()

};




function show_init(){

code = sessionStorage.getItem("account")

if (code.length !== 0){ 
 document.getElementById("account").innerHTML = code;
 Data_init(code);
}};

show_init();


