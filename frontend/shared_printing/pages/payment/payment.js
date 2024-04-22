import { strLenOptiize } from '../../utils/util'
const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    file_name: "filename.pdf",
    pages: 0,
    paper_type: "A4",
    color: "黑白",
    sides: "单面",
    copies: 0,
    price: 0,
    jsapi_sign: {},
    out_trade_no: '' //每个订单在商户后端的唯一标识
  },
  
  cancel: function(){
    wx.showModal({
      title: '是否确定取消打印',
      content: '取消打印将返回首页',
      success (res) {
        if (res.confirm) {
          wx.reLaunch({
            url: '../index/index'
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  pay: function(){
    const signObj = this.data.jsapi_sign
    wx.requestPayment({
      timeStamp: signObj.timeStamp,
      nonceStr: signObj.nonceStr,
      package: signObj.package,
      signType: signObj.signType,
      paySign: signObj.paySign,
      success (res) { 
        console.log(res)
      },
      fail (err) {
        console.error(err)
       }
    })
  },
  prepay: function(){
    var that = this
    wx.request({
      url: 'https://capybara.mynatapp.cc/api/pay',
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log(res.data);
        const signObj
        try {
          signObj = JSON.parse(res.data.jsapi_sign)
        } catch (error) {
          console.error('解析JSON失败：',error)
        }
        that.setData({
          jsapi_sign: signObj,
          out_trade_no: res.data.out_trade_no
        })
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
        let filename = strLenOptiize(6,info.filename)
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