var SystemMenu = [{
	title: '业务管理',
	icon: '&#xe63f;',
	isCurrent: true,
	menu: [{
		title: '承运商管理',
		icon: '&#xe620;',
		isCurrent: true,
		children: [{
			title: '首页',
			href: 'workbench.html',
			isCurrent: true
		},{
			title: '承运商录入',
			href: 'process.html'
		},{
			title: '承运商管理',
			href: 'providers.html'
		},{
			title: '承运商其他1',
			href: 'providers1.html'
		},{
			title: '承运商其他2',
			href: 'basic_info.html'
		},{
			title: '二级页面',
			children: [{
				title: '三级页面1',
				href: 'workbench.html'
			}]
		}]
	},{
		title: '订单管理',
		icon: '&#xe625;',
		href: 'basic_info.html',
		children: []
	},{
		title: '客户管理',
		icon: '&#xe62f;',
		children: [{
			title: '客户管理',
			href: 'providers.html'
		},{
			title: '客户专家',
			href: 'providers1.html'
		}]
	},{
		title: '货件管理',
		icon: '&#xe62f;',
		children: [{
			title: '历史查询',
			href: 'providers.html'
		},{
			title: '货件实时GPS',
			href: 'providers1.html'
		}]
	}]
}
// ,{
// 	title: '组织管理',
// 	icon: '&#xe60d;',
// 	menu: [{
// 		title: '领导组织',
// 		icon: '&#xe647;',
// 		children: [{
// 			title: '公司领导管理',
// 			href: 'index.html',
// 			isCurrent: true
// 		},{
// 			title: '企业荣誉',
// 			href: 'index.html'
// 		},{
// 			title: '组织架构',
// 			href: 'index.html'
// 		},{
// 			title: '自定义',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '系统设置',
// 		icon: '&#xe611;',
// 		children: [{
// 			title: '权限设置',
// 			href: 'process.html'
// 		},{
// 			title: '角色设置',
// 			href: 'process.html'
// 		},{
// 			title: '职务设置',
// 			href: 'process.html'
// 		},{
// 			title: '自定义',
// 			href: 'process.html'
// 		},{
// 			title: '采购组',
// 			href: 'process.html'
// 		}]
// 	},{
// 		title: '专家库',
// 		icon: '&#xe62f;',
// 		children: [{
// 			title: '专家管理',
// 			href: 'process.html'
// 		},{
// 			title: '添加专家',
// 			href: 'process.html'
// 		},{
// 			title: '审核专家',
// 			href: 'process.html'
// 		}]
// 	}]
// },{
// 	title: '主数据',
// 	icon: '&#xe61e;',
// 	menu: [{
// 		title: '数据信息',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '数据管理',
// 			href: 'process.html',
// 			isCurrent: true
// 		},{
// 			title: '企业荣誉',
// 			href: 'index.html'
// 		},{
// 			title: '组织架构',
// 			href: 'index.html'
// 		},{
// 			title: '自定义',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '数据表',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '供应商管理',
// 	icon: '&#xe620;',
// 	menu: [{
// 		title: '供应商列表',
// 		icon: '&#xe647;',
// 		children: [{
// 			title: '供应链条',
// 			href: 'providers.html',
// 			isCurrent: true
// 		},{
// 			title: '供应组织',
// 			href: 'index.html'
// 		},{
// 			title: '运输渠道',
// 			href: 'index.html'
// 		},{
// 			title: '自定义',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '供应客户',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '采购商开发',
// 	icon: '&#xe625;',
// 	menu: [{
// 		title: '采购商主页',
// 		icon: '&#xe647;',
// 		children: [{
// 			title: '采购管理',
// 			href: 'providers1.html',
// 			isCurrent: true
// 		},{
// 			title: '采购列表',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '数据表',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '采购寻源',
// 	icon: '&#xe64b;',
// 	menu: [{
// 		title: '寻源管理',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '自定义',
// 			href: 'basic_info.html',
// 			isCurrent: true
// 		},{
// 			title: '采购分析',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '统计图',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '合同管理',
// 	icon: '&#xe64c;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'basic_info.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '自定义',
// 	icon: '&#xe646;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'index.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '自定义',
// 	icon: '&#xe646;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'workbench.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// }
,{
	title: '自定义1',
	icon: '&#xe646;',
	menu: [{
		title: '合同归档',
		icon: '&#xe647;',
		isCurrent: true,
		children: [{
			title: '合同发布',
			href: 'basic_info.html',
			isCurrent: true
		},{
			title: '合同制度管理',
			href: 'index.html'
		}]
	},{
		title: '合同信息',
		icon: '&#xe611;',
		href: 'basic_info.html',
		children: []
	}]
}];