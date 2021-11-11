const comment_users = data.series[0].fields.find((f) => f.name === 'comment_user.keyword').values.buffer
const be_commented_users = data.series[0].fields.find((f) => f.name === 'be_commented_user.keyword').values.buffer
const counts = data.series[0].fields.find((f) => f.name === 'Count').values.buffer

const comment_users1 = data.series[1].fields.find((f) => f.name === 'comment_user.keyword').values.buffer
const counts1 = data.series[1].fields.find((f) => f.name === 'Count').values.buffer

Max = counts1[0]
Min = counts1[counts1.length-1]
const k = (100 - 10) / (Max - Min)
counts11 = counts1.map((num) => {
 return 10 + k * (num - Min)
})

var dict_size = {}
for (var i=0; i<comment_users1.length; i++){
	dict_size[comment_users1[i]] = counts11[i]
}
var dict_count = {}
for (var i=0; i<comment_users1.length; i++){
	dict_count[comment_users1[i]] = counts1[i]
}

users = comment_users.concat(be_commented_users)
var hash = {};
total_users = users.reduce(function(item, next) {
    hash[next] ? '' : hash[next] = true && item.push(next);
    return item
}, [])


const data1 = total_users.map((d, i) => {
  const user = total_users[i]
  const size = dict_size[user]
  const value = dict_count[user]
  return {name:user, symbolSize:size, value:value}
})

const link1 = comment_users.map((d, i) => {
  const comment_user = comment_users[i]
  const be_commented_user = be_commented_users[i]
  const count = counts[i]
  return {source:comment_user, target:be_commented_user, value:count}
})


return  option = {
    title: {
      text: 'Les Miserables',
      subtext: 'Default layout',
      top: 'bottom',
      left: 'right'
    },
    tooltip: {},
    animationDuration: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        name: 'Les Miserables',
        type: 'graph',
        layout: 'force',
		force:{
			repulsion:300,
			edgeLength:100
		},
        draggable:true,
        data: Object.assign([], data1),
        links: Object.assign([], link1),
		focusNodeAdjacency: true,
        roam: true,
        label: {
          position: 'right',
          formatter: '{b}'
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 10
          }
        }
      }
    ]
  };
