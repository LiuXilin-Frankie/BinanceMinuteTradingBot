/*
 Template Name: Zegva - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesdesign
 Website: www.themesdesign.in
 File: C3 Chart init js
 */


!function($) {
    "use strict";

    var ChartC3 = function() {};

    ChartC3.prototype.init = function () {
          
  
        var data_ = 0
        $.ajax({
            type: "GET",
            url: "/dashboard_c3_rates_history",
            dataType: "json",
            contentType: "application/json",
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


