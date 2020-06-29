odoo.define('structure_modeule.structure_modeule', function (require) {
"use strict";

var form_widget = require('web.form_widgets');
var core = require('web.core');
var Model = require('web.Model');
var _t = core._t;
var QWeb = core.qweb;

form_widget.WidgetButton.include({
    on_click: function() {
         if(this.node.attrs.custom === "click"){

            var callback = new $.Deferred();
            new Model("project.task")
                .call("search_student")
                .then(function (result) {
                      // Result is having what you want..


                     console.log((JSON.parse(""+result+"")) )
                     const A= (JSON.parse(""+result+""))
                     var SPI=.1
                     var CPI= .7
                     var EAC =50.9

                    

                     var dataPoints1 = [];
                     var dataPoints2 = [];
                     var dataPoints3 = [];
                     dataPoints1.push({
                                x: new Date(A[A.length-1].start),
                                y: 0

                            });
                     dataPoints2.push({
                                x: new Date(A[A.length-1].start),
                                y: 0

                            });
                     dataPoints3.push({
                                x: new Date(A[A.length-1].start),
                                y: 0
                            });

                     for (var i = 0; i < A.length-1; i++) {
                            dataPoints1.push({
                                x: new Date(A[i].date),
                                y: A[i].EV
                            });
                            dataPoints2.push({
                                x: new Date(A[i].date),
                                y: A[i].PV
                            });
                            dataPoints3.push({
                                x: new Date(A[i].date),
                                y: A[i].AV
                            });
                            SPI = A[i].EV /  A[i].PV
                            CPI = A[i].EV /  A[i].AV
                        }
                      dataPoints2.push({
                                x: new Date(A[A.length-1].date),
                                y: A[A.length-1].PV,
                                indexLabel: "BAC"
                            });

                     SPI= 1-SPI
                     CPI= 1- CPI
                     EAC= A[A.length-1].PV + (CPI*A[A.length-1].PV)
                     var dEAC= (new Date( A[A.length-1].date)   )
                     console.log(dEAC)
                     console.log(SPI)

                     dataPoints3.push({
                                x: dEAC,
                                y: EAC,
                                indexLabel: "EAC(X + "+SPI +'Time , y)'


                            });
                     function toggleDataSeries(e){
                            if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                                e.dataSeries.visible = false;
                            }
                            else{
                                e.dataSeries.visible = true;
                            }
                            chart.render();
                        }
                     var chart = new CanvasJS.Chart("student_dev1", {
                                animationEnabled: true,
                                title:{
                                    text: "EV,PV,AV"
                                },
                                axisX: {
                                    valueFormatString: "DD MMM,YY"
                                },
                                axisY: {
                                    title: "Cost",
                                    includeZero: false,
                                    suffix: ""
                                },
                                legend:{
                                    cursor: "pointer",
                                    fontSize: 16,
                                    itemclick: toggleDataSeries
                                },
                                toolTip:{
                                    shared: true
                                },
                                data: [{
                                    name: "EV",
                                    type: "spline",
                                    yValueFormatString: "#0.## °C",
                                    showInLegend: true,
                                    dataPoints: dataPoints1
                                },
                                {
                                    name: "PV",
                                    type: "spline",
                                    yValueFormatString: "#0.## °C",
                                    showInLegend: true,
                                    dataPoints: dataPoints2
                                },
                                {
                                    name: "AV",
                                    type: "spline",
                                    yValueFormatString: "#0.## °C",
                                    showInLegend: true,
                                    dataPoints: dataPoints3
                                }]
                            });
                     chart.render();











                 });









            return;
         }
         this._super();
    },
});
});
