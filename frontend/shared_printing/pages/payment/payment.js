import { strLenOptiize } from '../../utils/util'
import Toast from '@vant/weapp/toast/toast';
const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名
Page({

  /**
   * 页面的初始数据
   */
  data: {
    file_name: "文件名加载中……",
    pages: 0,
    paper_type: "A4",
    color: "黑白",
    sides: "单面",
    copies: 0,
    price: 0,
    spend_coins: 0,
    jsapi_sign: {},
    out_trade_no: '', //每个订单在商户后端的唯一标识
<<<<<<< HEAD
    isOK: true //判断是否能从后端获取支付信息，默认为true
=======
    isdisabled : true //用于禁用支付按钮
>>>>>>> dev
  },
  
  cancel: function(){//用户取消打印则调用该函数
    var that = this
    wx.showModal({
      title: '是否确定取消打印',
      content: '取消打印将返回首页',
      success (res) {
        if (res.confirm) {
          wx.request({
            url: curDomain+'api/close_print_order?out_trade_no='+that.data.out_trade_no,
            method: 'GET',
            header: {
              'content-type': 'application/json',
              'Cookie' : app.globalData.Cookie
            },
            success (res){
              console.log('调用关闭订单接口成功',res)
            },
            fail (err){
              console.error('调用关闭订单接口失败',err)
            }
          })
          wx.reLaunch({
            url: '../index/index'
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },

  print: function(){
<<<<<<< HEAD
    var that = this
    let out_trade_no = that.data.out_trade_no
    wx.request({
      url: curDomain+'api/print_file?out_trade_no='+out_trade_no,
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log('调用打印接口成功',res)
        that.setData({
          isOK : true
        })
        wx.redirectTo({
          url: '../subpayment/subpayment?filename='+ that.data.file_name
        })
      },
      fail (err){
        console.log('调用打印接口失败',err)
      }
    })
  },

  pay: function(){
    const signObj = this.data.jsapi_sign
    var that = this
    if(this.data.isOK){
      wx.requestPayment({
        timeStamp: signObj.timestamp,
        nonceStr: signObj.nonceStr,
        package: signObj.package,
        signType: signObj.signType,
        paySign: signObj.paySign,
        success (res) { 
          console.log('支付成功',res)
          that.print()
        },
        fail (err) {
          console.error('支付失败',err)
         }
      })
    }else{
      wx.showToast({
        title: '支付信息错误',
      })
    }
  },

=======
    var that = this
    let out_trade_no = that.data.out_trade_no
    wx.request({
      url: curDomain+'api/print_file?out_trade_no='+out_trade_no,
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log('api/print_file SUCCESS >>>',res)
        wx.redirectTo({
          url: '../subpayment/subpayment?filename='+ that.data.file_name
        })
      },
      fail (err){
        console.log('api/print_file ERROR >>>',err)
      }
    })
  },

  pay: function(){
    const signObj = this.data.jsapi_sign
    var that = this
    wx.requestPayment({
      timeStamp: signObj.timestamp,
      nonceStr: signObj.nonceStr,
      package: signObj.package,
      signType: signObj.signType,
      paySign: signObj.paySign,
      success (res) { 
        console.log('支付成功',res)
        that.print()
      },
      fail (err) {
        console.error('支付失败',err)
        }
    })
  },

>>>>>>> dev
  prepay: function(){// 获取调取支付需要的参数字段
    var that = this
    wx.request({
      url: curDomain+'api/pay?out_trade_no='+this.data.out_trade_no,
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log("api/pay GET success >>>",res.data);
        var signObj = res.data.jsapi_sign
<<<<<<< HEAD
        that.setData({
          jsapi_sign: signObj,
          out_trade_no: res.data.out_trade_no
        })
      },
      fail (err){//支付信息获取异常
        console.error("api/pay GET error >>>",err);
        this.setData({
          isOK : false
        })
        wx.showModal({
          title: '域名解析异常',
          content: '点击确认即可免费打印',
          showCancel: false,
          complete: (res) => {
            if (res.confirm) {
              console.log('用户点击确认')
              that.print()
            }
          }
        })
=======
        if(signObj != undefined){
          that.setData({
            jsapi_sign: signObj,
            isdisabled : false
          })
        }else{ //DNS解析失败或其他原因，导致后端返回500
          wx.showModal({
            title: '后台响应异常',
            content: '点击确定免费打印',
            showCancel: false,
            complete: (res) => {
              if (res.confirm) {
                console.log('用户点击确认')
                that.print()
              }
            }
          })
        }
      },
      fail (err){
        console.error("api/pay GET error >>>",err);
>>>>>>> dev
      }
    })
  },

  getTradeInfo: function(){ //获取支付需要的打印订单和支付信息，用于onload
    var that = this
    wx.request({
      url: curDomain+'api/pay',
      method: 'POST',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
<<<<<<< HEAD
        console.log('getTradeInfo success >>>',res.data);
=======
        console.log('api/pay POST success >>>',res.data);
>>>>>>> dev
        that.setData({
          out_trade_no : res.data.out_trade_no
        })
        that.prepay();
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    wx.hideShareMenu({
      menus: ['shareAppMessage', 'shareTimeline']
    })
    var that = this
    
    wx.request({
      url: curDomain+'api/print_order_info',
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log('后端输出打印信息>>>',res.data);
        const info = res.data
        that.getTradeInfo();//获取预信息
        //that.prepay();
<<<<<<< HEAD
        let filename = strLenOptiize(12,info.filename)
=======
        let filename = strLenOptiize(15,info.filename)
>>>>>>> dev
        that.setData({
          file_name : filename,
          pages : info.pages,
          paper_type : info.paper_type,
          color : info.color,
          sides : info.sides,
          copies : info.copies,
          price : info.price,
          spend_coins : info.spend_coins
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