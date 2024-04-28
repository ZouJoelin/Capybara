// index.js
import Toast from '@vant/weapp/toast/toast';
import Notify from '@vant/weapp/notify/notify';
import { strLenOptiize } from '../../utils/util'

const app = getApp();
Page({  
  data: {  
    fileList: [],
    code : '',
    backend_status: false,
    filename: '',
    filename_forshow: '待上传文件 ( 推荐pdf格式 )',
    color_index: 0,  
    size_index: 0,
    danshuang_index: 0,
    color_array: ['黑白'],
    size_array: ['A4'],
    danshuang_array:['单面','双面长边','双面短边'],
    paper_type: 'A4',
    sides: 'one-sided',
    color: '黑白',
    qty: 1,
    pgnum: 0,
    price: 0,
    isupload: false
  },  
  afterRead:function(e){
    var that = this
    // console.log(e)
    // console.log(e.detail.file)
    let tmpName = e.detail.file.name
    let fileName = strLenOptiize(15,tmpName)
    this.setData({
      filename_forshow: fileName,
      filename:e.detail.file.name
    })
    wx.uploadFile({
      filePath: e.detail.file.url,
      name: 'file',
      url: 'https://capybara.mynatapp.cc/api/auto_count/pages',
      formData:{
        'fileName' : e.detail.file.name
      },
      header: {  
        'content-type': 'multipart/form-data',
        'Cookie' : app.globalData.Cookie  
      }, 
      success (res){
        // const data = res
        console.log(res)
        let responseData = JSON.parse(res.data)
        console.log(responseData)
        that.setData({
          pgnum : responseData.pages,
          isupload : true //更新“取消”按钮禁用状态
        })
        that.updatePgnum();
      }
    })
  },

  updatePgnum:function(){
    var that = this
    wx.request({
      url: 'https://capybara.mynatapp.cc/api/auto_count/fee',
      method: 'POST',
      data:{
        "pages" : that.data.pgnum,
        "paper_type" : that.data.paper_type,
        "color" : that.data.color,
        "sides" : that.data.sides,
        "copies" : that.data.qty
      },
      header : {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log(res.data)
        
        that.setData({
          price : res.data.fee
        })
      }
    })
  },
  cancel: function(e){
    console.log(e)
    wx.reLaunch({
      url: './index'
    })
  },
  submit:function(){
    if(this.data.pgnum == 0){
      Notify({ type: 'primary', message: '未上传文件' })
    }else{
      var url = '/pages/payment/payment?price='+this.data.price
      wx.navigateTo({
      url: url,
      })
    }
  },

  initialize:function(){
    var that = this
    return new Promise((resolve,reject) => {
      wx.request({
        url: 'https://capybara.mynatapp.cc/?code='+that.data.code,
        method: 'GET',
        success: (res) => {
          // console.log(res);
          // console.log(app.globalData)
          resolve(res);
        },
        fail: (error) => {
          reject(error);
        }
      });
    });
  },
  bindColorChange: function(e) {  
    this.setData({  
      color_index: e.detail.value  
    })  
  },
  bindSizeChange: function(e){
    this.setData({
      size_index: e.detail.value
    })
  },
  bindDanShuangChange: function(e){
    console.log(e.detail)
    let value = e.detail.value
    let tmpSides = ''
    if(value == 0){
      tmpSides = 'one-sided'
    }else if(value == 1){
      tmpSides = 'two-sided-long-edge'
    }else if(value == 2){
      tmpSides = 'two-sided-short-edge'
    }
    console.log(tmpSides)
    this.setData({
      danshuang_index: value,
      sides : tmpSides
    })
    this.updatePgnum()

  },
  onQtyChange: function(e){
    var that = this
    console.log(e.detail);
    Toast.loading({
      message: '加载中...',
      forbidClick:true});
    setTimeout(()=>{
      Toast.clear();
      this.setData({
        qty: e.detail
      })
      that.updatePgnum();
    },400)
   
  },
  
  getStatus: function(){
    var that = this
    wx.request({
      url: 'https://capybara.mynatapp.cc/api/status',
      method: 'GET',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        console.log(res.data)
        if(res.data.backend_status == "ok"){
          that.setData({
            backend_status : true
          });
          that.initialize().then((res) => {
            console.log('初始化会话：',res)
            app.globalData.Cookie = res.cookies[0]
            console.log(app.globalData)
          })
          .catch((error) => {
            console.error('初始化会话失败：',error)
          })
        }
      }
    })
  },
  
   /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // console.log(options);
    var that = this;
    wx.login({
      success: (result) => {
        console.log(result)
        that.setData({
          code : result.code
        })
        //console.log(result.code)
        that.getStatus();
      },
      fail: (err) => {
        console.error(err)
      },
      complete: (res) => {
        //console.log(res)
      },
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
})