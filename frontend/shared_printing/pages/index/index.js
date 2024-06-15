// index.js
import Toast from '@vant/weapp/toast/toast';
import Notify from '@vant/weapp/notify/notify';
import { strLenOptiize,handleErrorMessage } from '../../utils/util'

const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名
Page({  
  data: {
    btnList:[
      {
        id: '0',
        text: '单面',
      },
      {
        id: '1',
        text: '双面长边',
      },
      {
        id: '2',
        text: '双面短边',
      },
    ],
    colorList:[
      {
        id: '0',
        text: '黑白'
      }
    ],
    sizeList:[
      {
        id: '0',
        text: 'A4'
      }
    ],
    fileList: [],
    code : '',
    backend_status: false,
    filename: '',
    filename_forshow: '待上传文件 ( pdf格式 )',
    offlineInfo:'待连接至打印机',
    paper_type: 'A4',
    sides: 'two-sided-long-edge',
    color: '黑白',
    qty: 1,
    pgnum: 0, //页数
    coins: 0,//印币，默认为0
    useCoins:0,//用户在stepper选择的，不一定等于实际使用的
    price: 0,
    isupload: false,
    islocal: false,
    isusecoin: false
  }, 
  oversize:function(e){
    console.error('文件太大',e)
    Notify({ type: 'warning', message: '文件太大（限制50MB以内' })
  } ,
  beforeRead:function(e){
    const { file, callback } = e.detail;
    let name = file.name
    let fileType = name.slice(-3)
    if (fileType == 'pdf') {
      callback(true)
    }else{
      Notify({ type: 'warning', message: '当前仅支持pdf格式' })
    }
  },
  afterRead:function(e){
    var that = this
    // console.log(e)
    console.log(e.detail.file)
    let tmpName = e.detail.file.name
    let fileName = strLenOptiize(18,tmpName)
    this.setData({
      filename_forshow: fileName,
      filename:e.detail.file.name
    })
    wx.uploadFile({
      filePath: e.detail.file.url,
      name: 'file',
      url: curDomain+'api/auto_count/pages',
      formData:{
        'fileName' : e.detail.file.name
      },
      header: {  
        'content-type': 'multipart/form-data',
        'Cookie' : app.globalData.Cookie  
      }, 
      success (res){
        // const data = res
        console.log('上传文件成功',res)
        /*
          上传文件格式不正确
          取出返回对象中data字段的json
        */
        if (res.statusCode == 400) {
          handleErrorMessage(res.data)
        }
        let responseData = JSON.parse(res.data)
        // console.log(responseData)
        that.setData({
          pgnum : responseData.pages,
          isupload : true //更新“取消”按钮禁用状态
        })
        that.updatePgnum();
      }
    })
  },

  localSubmit:function(e){
    console.log('本地上传',e)
    wx.navigateTo({
      url: '/pages/localSubmit/localSubmit',
    })
  },

  updatePgnum:function(){
    var that = this
    wx.request({
      url: curDomain+'api/auto_count/fee',
      method: 'POST',
      data:{
        "pages" : that.data.pgnum,
        "paper_type" : that.data.paper_type,
        "color" : that.data.color,
        "sides" : that.data.sides,
        "copies" : that.data.qty,
        "spend_coins" : that.data.useCoins
      },
      header : {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log('触发updatePgnum',res.data)
        
        that.setData({
          price : res.data.fee
        })
      }
    })
  },
  cancel: function(e){
    //console.log(e)
    wx.reLaunch({
      url: './index'
    })
  },
  submit:function(){ //打印按钮
    if(this.data.pgnum == 0){
      Notify({ type: 'primary', message: '未上传文件' })
    }else{
      if(this.data.useCoins != 0){//使用了印币
        this.setData({
          isusecoin : true
        })
      }
      var url = '/pages/payment/payment?price='+this.data.price
      wx.navigateTo({
      url: url,
      })
    }
  },

  initialize:function(){ //在getStatus用于初始化
    var that = this
    return new Promise((resolve,reject) => {
      wx.request({
        url: curDomain+'?code='+that.data.code,
        method: 'GET',
        success: (res) => {
          app.globalData.Cookie = res.cookies[0]
          app.globalData.openid = res.data.open_id
          // console.log(app.globalData)
          resolve(res);
        },
        fail: (error) => {
          reject(error);
        }
      });
    });
  },
  // bindDanShuangChange: function(e){
  //   console.log(e.detail)
  //   let value = e.detail.value
  //   let tmpSides = ''
  //   if(value == 0){
  //     tmpSides = 'two-sided-long-edge'
  //   }else if(value == 1){
  //     tmpSides = 'one-sided'
  //   }else if(value == 2){
  //     tmpSides = 'two-sided-short-edge'
  //   }
  //   console.log(tmpSides)
  //   this.setData({
  //     danshuang_index: value,
  //     sides : tmpSides
  //   })
  //   if (this.data.isupload) {
  //     this.updatePgnum()
  //   }else{
  //     Notify({ type: 'primary', message: '未上传文件' })
  //   }
  // },

  handleBtnEvent(e){
    // 按钮组点击触发，接收子组件传过来的数据，进行操作
    //console.log('handleBtnEvent：',e.detail)
    let currentId = e.detail.currentId
    let tmpSides = ''
    if(currentId === "0"){
      tmpSides = 'one-sided'
    }else if(currentId === "1"){
      tmpSides = 'two-sided-long-edge'
    }else if(currentId === "2"){
      tmpSides = 'two-sided-short-edge'
    }
    console.log(tmpSides)
    this.setData({
      sides: tmpSides
    })
    if (this.data.isupload) {
      this.updatePgnum()
    }else{
      Notify({ type: 'primary', message: '未上传文件' })
    }
  },

  onCoinsChange:function(e){
    var that = this
    Toast.loading({
      message: '加载中...',
      forbidClick:true});
    setTimeout(()=>{
      Toast.clear();
      this.setData({
        useCoins: e.detail
      })
      that.updatePgnum();
    },400)
  },

  onQtyChange: function(e){
    var that = this
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
  
  getUserInfo: function(){ //向后台获取用户信息
    //console.log(app.globalData.Cookie)
    var that = this
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
          that.setData({
            coins:res.data.coins
          })
        }
      },
      fail: (error) => {
        console.error(error)
      }
    });
  },

  getStatus: function(){ //获取打印机状态
    var that = this
    wx.request({
      url: curDomain+'api/status',
      method: 'GET',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success (res) {
        //console.log('获取打印机状态：',res)
        let status = res.data.backend_status
        if(status == "ok"){
          that.setData({
            backend_status : true
          });
          that.initialize().then((res) => {
            console.log('初始化会话：',res)
            that.getUserInfo()
          })
          .catch((error) => {
            console.error('初始化会话失败：',error)
          })
        }else if(res.statusCode == 404 && res.data.includes("Tunnel")){
          that.setData({
            offlineInfo: '服务器掉线'
          })
        }else if(res.statusCode == 503){
          let info = ''
          switch(status){
            case 'door_open':
              info = '打印机盖未闭合'
              break
            case 'out_of_paper':
              info = '纸张不足'
              break
            case 'out_of_toner':
              info = '墨粉不足'
              break
            case 'jam':
              info = '纸张堵塞'
              break
            case 'offline':
              info = '打印机未连接'
              break
            case 'unknown_error':
              info = '未知错误'
              break
            default:
              console.error('前端未知错误',status)
          }
          that.setData({
            offlineInfo: info
          })
        }else{
          that.setData({
            offlineInfo: '应用框架异常'
          })
        }
      }
    })
  },

  localPost: function(){ //本地上传
    var that = this
    wx.request({
      url: curDomain+'local_upload',
      method: 'POST',
      data:{
        "fileName" : that.data.filename,
        "pages" : that.data.pgnum 
      },
      header : {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie' : app.globalData.Cookie 
      },
      success(res){
        console.log('触发localPost：',res)
        that.updatePgnum()
      }
    })
  },
  
   /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log('当前环境使用域名：',curDomain)
    var that = this;
    wx.login({
      success: (result) => {
        console.log('wx.login success',result)
        that.setData({
          code : result.code
        })
        app.globalData.code = result.code
        that.getStatus()
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
    this.btnGroup = this.selectComponent("#btn-group")
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    //console.log('onShow: ',app.globalData.Cookie)
    if(this.data.islocal){
      this.localPost();
      //本地上传的，先传cookie再获取打印费用
    }
    if(this.data.isusecoin){//本页面点击支付时用了硬币就重新获取用户信息（哪怕在支付页面返回了），用于刷新印币
      console.log('使用了印币，重新获取用户信息')
      this.setData({
        isusecoin : false
      })
      this.getUserInfo()
    }
  },
})