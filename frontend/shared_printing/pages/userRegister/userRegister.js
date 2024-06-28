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
    universitys: ['请选择','中山大学','其他'],
    universityIndex: 0,
    regions: ['请选择','东校区','南校区','北校区','珠海校区','深圳校区'],
    regionIndex: 0,
    schools: ['请选择','生命科学学院','中国语言文学系','历史学系','哲学系',
    '社会学与人类学学院','博雅学院','岭南学院','外国语学院','法学院',
    '政治与公共事务管理学院','管理学院','马克思主义学院','心理学系',
    '新闻传播学院','信息管理学院','艺术学院','数学学院','物理学院','化学学院',
    '地理科学与规划学院','材料科学与工程学院','电子与信息工程学院','计算机学院',
    '国家保密学院','环境科学与工程学院','系统科学与工程学院','中山医学院','光华口腔医学院',
    '公共卫生学院','药学院','护理学院','体育部','继续教育学院','医学院','公共卫生学院（深圳）',
    '药学院（深圳）','材料学院','生物医学工程学院','电子与通信工程学院','智能工程学院',
    '航空航天学院','农业与生物技术学院','生态学院','集成电路学院','先进制造学院','先进能源学院',
    '网络空间安全学院','商学院 (创业学院)','理学院','柔性电子学院','中国语言文学系（珠海）','历史学系（珠海）',
    '哲学系（珠海）','国际金融学院','国际翻译学院','国际关系学院','旅游学院','数学学院（珠海）','物理与天文学院',
    '大气科学学院','海洋科学学院','地球科学与工程学院','化学工程与技术学院','海洋工程与技术学院','中法核工程与技术学院',
    '土木工程学院','微电子科学与技术学院','测绘科学与技术学院','人工智能学院','软件工程学院'],
    schoolIndex: 0,
    dormitorys: ['请选择','慎思园6号','慎思园5号','慎思园7号','慎思园8号','慎思园9号','慎思园10号',
    '明德园1号','明德园2号','明德园3号','明德园5号','明德园7号','明德园8号','明德园9号','明德园10号','明德园12号',
    '至善园1号','至善园2号','至善园3号','至善园4号','至善园5号','至善园6号','至善园7号','至善园8号','至善园9号','至善园10号',
    '格致园3号1单元','格致园3号2单元','格致园3号3单元','格致园3号4单元','其他'],
    dormitoryIndex: 0,
    isdisabled: true,
    isLegal: true //输入框内容是否合法
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
          console.log('注册成功',res.data)
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

  handleNameInput: function(e){
    const value = e.detail.value
    const regex = /^[\u4e00-\u9fa5a-zA-Z]+$/
    if (regex.test(value)) {
      this.setData({
        isLegal: true
      })
    } else {
      // 如果输入不合法，可以给用户提示，或者直接过滤非法字符
      wx.showToast({
        title: '仅允许中英文',
        icon: 'none',
        duration: 2000
      });
      this.setData({
        isLegal: false
      })
      //console.log(this.data.isLegal)
    }
  },

  handleTrim: function(value){
    let tableInfo = value
    tableInfo.nickname = tableInfo.nickname.trim()
    tableInfo.student_name = tableInfo.student_name.trim()
    tableInfo.student_id = tableInfo.student_id.trim()
    return tableInfo
  },


  onSubmit: function(e){
    let tableInfo = this.handleTrim(e.detail.value)
    var that = this
    const IDregex = /^\d{6,10}$/; // 正则表达式，限制6到10位的数字

    if(!(IDregex.test(tableInfo.student_id)) || !this.data.isLegal || !this.OnPickerLegal()
     || tableInfo.nickname == "" || tableInfo.student_name == "" || tableInfo.student_id == ""){//用户漏填昵称或姓名
      Notify({ type: 'primary', message: '信息未完善或非法' });
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

  OnPickerLegal: function(){//校验picker的合法性，即index非0
    if(this.data.universityIndex == 0 || this.data.regionIndex == 0 || this.data.schoolIndex == 0 || this.data.dormitoryIndex == 0){
      return false
    }else{
      return true
    }
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