// pages/user/user.js
const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: null,
    isLogin : false
  },


  contactAdmin:function(){
    //联系管理员，后续跳转到一个静态页面即可
    wx.navigateTo({
      url: '/pages/contactAdmin/contactAdmin',
    })
  },

  userLogin:function(){
    wx.navigateTo({
      url: '/pages/userRegister/userRegister',
    })
  },

  handleUserCoin:function(){
    wx.navigateTo({
      url: '/pages/coinRuleInfo/coinRuleInfo',
    })
  },

  getUserInfo: function(){ //向后台获取用户信息
    wx.request({
      url: curDomain+'api/get_user_info?open_id='+app.globalData.openid,
      method: 'GET',
      header : {
        'Cookie' : app.globalData.Cookie
      },
      success: (res) => {
        if(res.statusCode == 403){
          console.log('getUserInfo>>>',res.data.error_message)
        }else if(res.statusCode == 200){
          console.log('当前用户已注册',res.data)
          app.globalData.isLogin = true
          app.globalData.userInfo= res.data
        }
      },
      fail: (error) => {
        console.error(error)
      }
    });
  },

  updateUserStatus:function(){//从app.js中维护更新用户登录状态和用户信息
    this.setData({
      isLogin: app.globalData.isLogin,
      userInfo: app.globalData.userInfo
    })
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.getUserInfo();
    // this.updateUserStatus()
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
    this.updateUserStatus();
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