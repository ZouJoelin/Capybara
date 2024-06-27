// pages/user/user.js
import Toast from '@vant/weapp/toast/toast';

const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: null,
    isLogin : false, //默认为false，从app文件中更新
    show : false,
    shareTimes : 10 //用户今日转发次数，先设为一个“极大值”
  },


  contactAdmin:function(){
    //联系管理员，后续跳转到一个静态页面即可
    wx.navigateTo({
      url: '/pages/contactAdmin/contactAdmin',
    })
  },

  userLogin:function(){
    setTimeout(()=>{
      wx.navigateTo({
        url: '/pages/userRegister/userRegister',
      })
    },500)
  },

  handleUserCoin:function(){
    wx.navigateTo({
      url: '/pages/coinRuleInfo/coinRuleInfo',
    })
  },

  updateUserStatus:function(){//从app.js中维护更新用户登录状态和用户信息
    this.setData({
      isLogin: app.globalData.isLogin,
      userInfo: app.globalData.userInfo,
      show : !app.globalData.isLoading,
      shareTimes: app.globalData.shareTimes
    })
  },

  // shareIncentive:function(){
  //   var that = this
  //   wx.request({
  //     url: curDomain+'api/share_incentive?open_id='+app.globalData.openid+'&incentive='+app.globalData.incentive,
  //     method: 'GET',
  //     header: {
  //       'content-type': 'application/json',
  //       'Cookie' : app.globalData.Cookie
  //     },
  //     success(res){
  //       console.log('api/share_incentive GET >>>',res)
  //       that.updateUserStatus();
  //     }
  //   })
  // },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    wx.hideShareMenu({
      menus: ['shareAppMessage', 'shareTimeline']
    })
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
  //   if(this.data.shareTimes < app.globalData.shareTimesLimit){
  //     this.shareIncentive()
  //   }

  //   const promise = new Promise(resolve => {
  //     resolve({
  //       title: '我发现了个超好用的共享打印',
  //       path: '/pages/index/index', // 转发的路径
  //       imageUrl: '/images/头像默认.png'
  //     })
  //   })

  //   return {
  //     title: '我发现了个超好用的共享打印',
  //     path: '/pages/index/index', // 转发的路径
  //     imageUrl: '/images/头像默认.png',
  //     promise
  //   };
  }
})