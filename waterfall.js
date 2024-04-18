


ooption2 ={
    title: {
      text: 'Accumulated Waterfall Chart'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function (params) {
        let tar;
        if (params[1] && params[1].value !== '-') {
          tar = params[1];
        } else {
          tar = params[2];
        }
        return tar && tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
      }
    },
    legend: {
      data: ['Expenses', 'Income']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: (function () {
        let list = [];
        for (let i = 1; i <= 11; i++) {
          list.push('Nov ' + i);
        }
        return list;
      })()
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: 'Placeholder',
        type: 'bar',
        stack: 'Total',
        silent: true,
        itemStyle: {
          borderColor: 'transparent',
          color: 'transparent'
        },
        emphasis: {
          itemStyle: {
            borderColor: 'transparent',
            color: 'transparent'
          }
        },
        data: [0, 1784.0288, 4274.8337, 7583.1099, 6423.7188, 5277.8446, 4008.2922, 3714.4375, 7491.6204, 2242.8620, 4116.5159, 8504.7807, 
          9095.7788, 14055.2586, 3559.6872, 15252.9387, 11032.7411]
        
      },
      {
        name: 'Income',
        type: 'bar',
        stack: 'Total',
        label: {
          show: true,
          position: 'top'
        },
        data: [1784.0288, 2490.8049 , 3308.2762, '_', '_', '_', '_', 3777.1829, '_', 
        1873.6539, 4388.2648, 590.9981, 4959.4798,'_',11693.2515, '_']

      },
      {
        name: 'Expenses',
        type: 'bar',
        stack: 'Total',
        label: {
          show: true,
          position: 'bottom'
        },
        data:  ['_', '_', '_', 1159.3911, 1145.8742, 1269.5524, 293.8547, '_', 
        5248.7584,'_', '_', '_', '_', 10495.5714, '_',  4220.1976] 
      }
    ]
  };


 