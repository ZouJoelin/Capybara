// pages/coinRuleInfo/coinRuleInfo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    info: '<p><span style="color: #4e514e;;">&nbsp;&nbsp;&nbsp;&nbsp;印币是一种“代金券”，可以抵消打印费用。目前对于新注册的用户我们都会赠送3枚印币。此外在首页转发小程序分享给好友也能获得印币，每天有效转发次数1次，每次转发将获得3枚印币作为感谢。</span></p><p><span style="color: #4e514e;;"><br/></span></p><p><span style="color: #4e514e;;">&nbsp;&nbsp;&nbsp;&nbsp;在打印价格内，每枚印币抵扣0.10元。若价格抵消为0，需象征性收取0.01元</span></p><p><span style="color:  #4e514e;;"><br/></span></p><p><span style="color: #4e514e;;">&nbsp;&nbsp;&nbsp;&nbsp;例如打印费用为0.50元，输入6个印币，则实际扣除印币5枚，最终打印费用为0.01元</span></p><p><br/></p>'
  },

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