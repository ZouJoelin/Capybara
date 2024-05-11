// components/btn-group/btn-group.js
Component({

  options: {
    styleIsolation: 'isolated'//样式隔离
  },

  /**
   * 组件的属性列表
   */
  properties: {
    dataList:{
      type: Array,
      value: []
    },
    currentId: {
      type: String,
      value: ''
    },
  },

  /**
   * 组件的内部初始数据
   */
  data: {

  },

  /**
   * 组件的方法列表
   */
  methods: {
    switchBtn: function(e){
      // console.log('switchBtn',e.currentTarget.dataset)
      this.setData({
        currentId: e.currentTarget.dataset.id
      })
      var btnEventDeatil = {
        currentId:e.currentTarget.dataset.id//当前按钮id
      }//detail对象，提供给事件监听函数
      var btnEventOption = {}//触发事件的选项
      this.triggerEvent('btnEvent',btnEventDeatil,btnEventOption)
    }
  },

  lifetimes: {
    attached: function() {
      // 在组件实例进入页面节点树时执行
    },
    detached: function() {
      // 在组件实例被从页面节点树移除时执行
    },
  },
})