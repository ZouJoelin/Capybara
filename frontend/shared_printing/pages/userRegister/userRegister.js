// pages/userRegister/userRegister.js
import Notify from '@vant/weapp/notify/notify';
const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},//用户填写
    universitys: ['中山大学','其他'],
    universityIndex: 0,
    regions: ['东校区','南校区','北校区'],
    regionIndex: 0,
    schools: ['生命科学学院','中国语言文学系','历史学系','哲学系',
    '社会学与人类学学院','博雅学院','岭南学院','外国语学院','法学院',
    '政治与公共事务管理学院','管理学院','马克思主义学院','心理学系',
    '新闻传播学院','信息管理学院','艺术学院','数学学院','物理学院','化学学院',
    '地理科学与规划学院','材料科学与工程学院','电子与信息工程学院','计算机学院',
    '国家保密学院','环境科学与工程学院','系统科学与工程学院','中山医学院','光华口腔医学院',
    '公共卫生学院','药学院','护理学院','体育部','继续教育学院'],
    schoolIndex: 0,
    dormitorys: ['慎思园6号','慎思园5号','慎思园7号','慎思园8号','慎思园9号','慎思园10号',
    '明德园1号','明德园2号','明德园3号','明德园5号','明德园7号','明德园8号','明德园9号','明德园10号','明德园12号',
    '至善园1号','至善园2号','至善园3号','至善园4号','至善园5号','至善园6号','至善园7号','至善园8号','至善园9号','至善园10号',
    '格致园3号1单元','格致园3号2单元','格致园3号3单元','格致园3号4单元'],
    dormitoryIndex: 0,
    isdisabled: true
  },

  completeUserRegister: function(){ //向后台获取用户信息，并返回用户页
    wx.request({
      url: curDomain+'api/get_user_info?open_id='+app.globalData.openid,
      method: 'GET',
      header : {
        'Cookie' : app.globalData.Cookie
      },
      success: (res) => {
        if(res.statusCode == 403){
          console.log(res.data.error_message)
        }else if(res.statusCode == 200){
          console.log('当前用户已注册',res.data)
          app.globalData.isLogin = true
          app.globalData.userInfo= res.data
          wx.reLaunch({
            url: '../user/user'
          })
        }
      },
      fail: (error) => {
        console.error(error)
      }
    });
  },

  postConvertInfo: function(tableInfo){//用于转换用户提交的信息并传给后端
    var that = this
    this.setData({
      userInfo:{
        openid:app.globalData.openid,
        nickname: tableInfo.nickname,
        student_name: tableInfo.student_name,
        student_id: tableInfo.student_id,
        university: this.data.universitys[tableInfo.university],
        region: this.data.regions[tableInfo.region],
        school: this.data.schools[tableInfo.school],
        dormitory: this.data.dormitorys[tableInfo.dormitory]
      }
    })
    let userInfo = this.data.userInfo
    console.log('用户提交的信息',userInfo)
    wx.request({
      url: curDomain+'api/complete_user_info',
      method: 'POST',
      data:{
        "open_id" : userInfo.openid,
        "nickname" : userInfo.nickname,
        "student_name" : userInfo.student_name,
        "student_id" : userInfo.student_id,
        "university" : userInfo.university,
        "region" : userInfo.region,
        "school" : userInfo.school,
        "dormitory" : userInfo.dormitory
      },
      header : {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log('触发postConvertInfo',res.data)
        if(res.statusCode == 200){//注册成功
          that.completeUserRegister()
        }else if(res.statusCode == 400){
          Notify('学号仅支持数字喔');
        }
      },
      fail (err){
        console.log(err)
      }
    })
  },

  onSubmit: function(e){
    let tableInfo = e.detail.value
    //console.log(tableInfo)
    var that = this
    if(tableInfo.nickname == "" || tableInfo.student_name == ""){//用户漏填昵称或姓名
      Notify({ type: 'primary', message: '昵称或姓名未填' });
    }else{
      wx.showModal({
        title: '请确认用户信息',
        content: '提交成功后无法再修改',
        success (res) {
          if (res.confirm) {
            that.postConvertInfo(tableInfo)
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }
    
  },

  onReset: function(){
    this.setData({
      universityIndex:0,
      regionIndex:0,
      schoolIndex:0,
      dormitoryIndex:0
    })
  },

  onUniversityChange: function(e){
    this.setData({
      universityIndex: e.detail.value
    })
  },

  onRegionChange: function(e){
    this.setData({
      regionIndex: e.detail.value
    })
  },

  onSchoolChange: function(e){
    this.setData({
      schoolIndex: e.detail.value
    })
  },

  onDormitoryChange: function(e){
    this.setData({
      dormitoryIndex: e.detail.value
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    if(app.globalData.isLogin == false){ //若用户未注册，则激活提交按钮
      this.setData({
        isdisabled:false
      })
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})