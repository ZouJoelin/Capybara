import { strLenOptiize } from '../../utils/util'
const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名
Page({

  /**
   * 页面的初始数据
   */
  data: {
    webUrl: curDomain + 'local_upload'
  },

  getMessage:function(e){
    let pages = getCurrentPages();
    let prePage = pages[ pages.length - 2 ]
    let data = e.detail.data[0]
    //console.log('getMessage：',data)
    prePage.setData({
    filename: data.fileName,
    filename_forshow: strLenOptiize(18,data.fileName),
    pgnum: data.pages,
    islocal : true,
    isupload: true,
    qty: 1 
    })
  },

  getLoad:function(e){
    //console.log('getLoad:e>>>',e)
  },

  getError:function(e){
    //console.error('getError:e>>>',e)
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