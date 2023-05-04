/*
 Template Name: Zegva - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesdesign
 Website: www.themesdesign.in
 File: Datatable js
 */
function filltables(){

var data_1 = {};
 function getdata_1() {
 
                $.ajax({
                    type: "POST",
                    url: "/account_table",
                    dataType: "json",
                    contentType: "application/json",
                    data:JSON.stringify({"account":code,"password":"123"}),
                    headers:{'Content-Type':'application/json;charset=utf8','organId':'1333333333'},
                    async: false,
                    success: function (result) {  
                    data_1 = result;
                    console.log(data_1);},
                    error: function () {
                    console.log("Get Rand Name Failed!");}
                });
                return data_1;
            }          
   getdata_1();
   console.log("已完成数据获取"); 

   var table_data =[];
   
   for (var i =0; i<Object.keys(data_1).length; i++){
   table_data.push(data_1[i]);
   }

    $('#datatable').DataTable({
    

        data: table_data
    });
   
} 



var code;

 
function set_ID(){

var code = document.getElementById("batch_add_delete_variations_number").value;
code =  String(code);
sessionStorage.setItem("account", code)
console.log("获取了code")
console.log(sessionStorage.getItem("account"))
location.reload()

};




function show_init(){

code = sessionStorage.getItem("account")
console.log(typeof(code))
console.log(code)

if (code.length !== 0){ 
 document.getElementById("account").innerHTML = code;
 filltables();
}};

show_init();

