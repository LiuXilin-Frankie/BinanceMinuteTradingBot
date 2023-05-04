/*
 Template Name: Zegva - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesdesign
 Website: www.themesdesign.in
 File: Float Js
 */


!function($) {
    "use strict";

    var FlotChart = function() {
        this.$body = $("body")
        this.$realData = []
    };

   
      FlotChart.prototype.getData = function() {
            var data = 0 ;
                function get_netvaluetemp() {
                  $.ajax({
                      type: "GET",
                      url: "/get_netvaluetemp",
                      dataType: "json",
                      contentType: "application/json",
                      headers: {'Content-Type':'application/json;charset=utf8','organId':'1333333333'},
                      async: false,
                      success: function (result) {  
                      data = result;
                     },
                      error: function () {
                      console.log("Get Rand Name Failed!");}
                  });
                  return data;  }    
      get_netvaluetemp();
      
      while (data.length < 300){
      data.unshift(data[0])}
      
      var res = [];
      for (var i = 0; i < data.length; ++i) {
        res.push([i, data[i]])
      }
      return res;
      },



    FlotChart.prototype.createRealTimeGraph = function(selector, data, colors) {
        var plot = $.plot(selector, [data], {
          colors: colors,
          series: {
            lines: {
              show: true,
              fill: true,
              lineWidth: 2,
              fillColor: {
                colors: [{
                  opacity: 0.45
                }, {
                  opacity: 0.45
                }]
              }
            },
            points: {
              show: false
            },
            shadowSize: 0
          },
          grid : {
				show : true,
				aboveData : false,
				color : '#dcdcdc',
				labelMargin : 15,
				axisMargin : 0,
				borderWidth : 0,
				borderColor : null,
				minBorderMargin : 5,
				clickable : true,
				hoverable : true,
				autoHighlight : false,
				mouseActiveRadius : 20
			},
			tooltip : true, //activate tooltip
			tooltipOpts : {
				content : "Value is : %y.0" + "%",
				shifts : {
					x : -30,
					y : -50
				}
			},
			yaxis : {
				//min : 0,
				//max : 100,
				color : 'rgba(0,0,0,0.1)'
			},
			xaxis : {
				show : false
			}
        });

        return plot;
    },
   

        //initializing various charts and components
        FlotChart.prototype.init = function() {

            //real time data representation
            var plot = this.createRealTimeGraph('#flotRealTime', this.getData() , ['#0e86e7']);
            plot.draw();
            var $this = this;
            function updatePlot() {
                plot.setData([$this.getData()]);
               // console.log($this.getData())
                // Since the axes don't change, we don't need to call plot.setupGrid()
                plot.draw();
                setTimeout(updatePlot, $( 'html' ).hasClass( 'mobile-device' ) ? 1000 : 1000);
            }
            updatePlot();
        },

    //init flotchart
    $.FlotChart = new FlotChart, $.FlotChart.Constructor = FlotChart

}(window.jQuery),

//initializing flotchart
function($) {
    "use strict";
    $.FlotChart.init()
}(window.jQuery);



