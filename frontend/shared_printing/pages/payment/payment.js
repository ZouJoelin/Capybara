const util = require('../../utils/util'); 
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    file_name : "filename.pdf",
    pages : 0,
    paper_type : "A4",
    color : "黑白",
    sides : "单面",
    copies : 0,
    price : 0,
    jsapi_sign : {}
  },
  pay: function(){
    console.log("pay")
  },
  prepay: function(){
    wx.request({
      url: 'https://capybara.mynatapp.cc/api/pay',
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log(res);
      },
      fail (err){
        console.error(err);
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    var that = this
    console.log(options)
    wx.request({
      url: 'https://capybara.mynatapp.cc/api/order',
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log(res.data);
        const info = res.data
        that.prepay();
        let tmpname = info.filename
        let filename = util.strLenOptiize(6,tmpname)
        that.setData({
          file_name : filename,
          pages : info.pages,
          paper_type : info.paper_type,
          color : info.color,
          sides : info.sides,
          copies : info.copies,
          price : info.price
        })
      }
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