
/**BAR CHART  */
    var myChart = document.getElementById('myChart').getContext('2d');
        //Global Options
    Chart.defaults.font.family = 'Lato';
    Chart.defaults.font.size = 18;
    Chart.defaults.font.color = '#777';
   
    var allChart = new Chart(myChart, {
        type:'bar',//bar, pie chart, line..etc.
        data:{
            labels:['Total Hours Reached','Required Hours: 500'],
            datasets:[{
                label:'Hour Indicator for OJT Worktime',
                data:[
                100,
                500
                ],
                
                backgroundColor:[
                'rgb(100, 149, 237)',
                'rgb(159, 226, 191)'
                ],
                borderWidth:1,
                borderColor:'#777',
                hoverBorderWidth:3,
                hoverBorderColor:'#000'
            }]
        },
        options:{
            plugins: {
                                    legend:{
                                        display:true,
                                        position :'top',
                                            labels:{
                                            fontColor:'black'
                                            
                                            }
                                         },
                                         layout:{
                                        padding:{
                                          /**  left:100,
                                            right:100,
                                            bottom:100,
                                            top:0*/
                                        },                                      
                                         },
             title:{
                display:true,
                text:'New Era University On-The-Job Training Required Worktime',
                font:{
                    size:25
                }
        }
        }
            
    }
    });



/**PIE CHART  */

var myPie = document.getElementById('myPie').getContext('2d');
//Global Options
Chart.defaults.font.family = 'Lato';
Chart.defaults.font.size = 18;
Chart.defaults.font.color = '#777';

var allChart = new Chart(myPie, {
type:'pie',//bar, pie chart, line..etc.
data:{
    labels:['Total Hours Reached','Required Hours: 500'],
    datasets:[{
        label:'Hour Indicator for OJT Worktime',
        data:[
        100,
        500
        ],
        
        backgroundColor:[
        'rgb(100, 149, 237)',
        'rgb(159, 226, 191)'
        ],
        borderWidth:1,
        borderColor:'#777',
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
    }]
},
options:{
    plugins: {
                            legend:{
                                display:true,
                                position :'right',
                                    labels:{
                                    fontColor:'black'
                                    
                                    }
                                 },
                                 layout:{
                                padding:{
                                  /**  left:100,
                                    right:100,
                                    bottom:100,
                                    top:0*/
                                },                                      
                                 },
     title:{
        display:true,
        text:'New Era University On-The-Job Training Required Worktime',
        font:{
            size:25
        }
}
}
    
}
});


/**LINE  */
var myLine = document.getElementById('myLine').getContext('2d');
//Global Options
Chart.defaults.font.family = 'Lato';
Chart.defaults.font.size = 18;
Chart.defaults.font.color = '#777';

var allChart = new Chart(myLine, {
type:'line',//bar, pie chart, line..etc.
data:{
    labels:['Total Hours Reached','Required Hours: 500'],
    datasets:[{
        label:'Hour Indicator for OJT Worktime',
        data:[
        100,
        500
        ],
        
        backgroundColor:[
        'rgb(100, 149, 237)',
        'rgb(159, 226, 191)'
        ],
        borderWidth:1,
        borderColor:'#777',
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
    }]
},
options:{
    plugins: {
                            legend:{
                                display:true,
                                position :'top',
                                    labels:{
                                    fontColor:'black'
                                    
                                    }
                                 },
                                 layout:{
                                padding:{
                                  /**  left:100,
                                    right:100,
                                    bottom:100,
                                    top:0*/
                                },                                      
                                 },
     title:{
        display:true,
        text:'New Era University On-The-Job Training Required Worktime',
        font:{
            size:25
        }
}
}
    
}
});


