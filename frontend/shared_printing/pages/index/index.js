// index.js
import Toast from '@vant/weapp/toast/toast';
import Notify from '@vant/weapp/notify/notify';
import { strLenOptiize, handleErrorMessage } from '../../utils/util'

const app = getApp();
const curDomain = app.globalData.domain //配置当前页面使用域名
Page({
  data: {
    btnList: [
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
    colorList: [
      {
        id: '0',
        text: '黑白'
      }
    ],
    sizeList: [
      {
        id: '0',
        text: 'A4'
      }
    ],
    fileList: [],
    code: '',
    backend_status: false,
    filename: '',
    filename_forshow: '待上传文件 ( pdf格式 )',
    offlineInfo: '待连接至打印机',
    // color_index: 0,  
    // size_index: 0,
    // danshuang_index: 0,
    // color_array: ['黑白'],
    // size_array: ['A4'],
    // danshuang_array:['双面长边','单面','双面短边'],
    paper_type: 'A4',
    sides: 'two-sided-long-edge',//传给后端主要是用sides属性
    color: '黑白',
    qty: 1,
    pgnum: 0, //页数
    price: 0,
    isupload: false,
    islocal: false
  },
  oversize: function (e) {//文件太大
    console.error('文件太大', e)
    Notify({ type: 'warning', message: '文件太大（限制50MB以内' })
  },
  beforeRead: function (e) {//文件上传前校验
    const { file, callback } = e.detail;
    let name = file.name
    let fileType = name.slice(-3)
    if (fileType == 'pdf') {
      callback(true)
    } else {
      Notify({ type: 'warning', message: '当前仅支持pdf格式' })
    }
  },
  afterRead: function (e) {
    var that = this
    // console.log(e)
    console.log(e.detail.file)
    let tmpName = e.detail.file.name
    let fileName = strLenOptiize(18, tmpName)
    this.setData({
      filename_forshow: fileName,
      filename: e.detail.file.name
    })
    wx.uploadFile({
      filePath: e.detail.file.url,
      name: 'file',
      url: curDomain + 'api/auto_count/pages',
      formData: {
        'fileName': e.detail.file.name
      },
      header: {
        'content-type': 'multipart/form-data',
        'Cookie': app.globalData.Cookie
      },
      success(res) {
        // const data = res
        console.log('上传文件成功', res)
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
          pgnum: responseData.pages,
          isupload: true //更新“取消”按钮禁用状态
        })
        that.updatePgnum();
      }
    })
  },

  localSubmit: function (e) {
    console.log('本地上传', e)
    wx.navigateTo({
      url: '/pages/localSubmit/localSubmit',
    })
  },

  updatePgnum: function () {
    var that = this
    wx.request({
      url: curDomain + 'api/auto_count/fee',
      method: 'POST',
      data: {
        "pages": that.data.pgnum,
        "paper_type": that.data.paper_type,
        "color": that.data.color,
        "sides": that.data.sides,
        "copies": that.data.qty
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie': app.globalData.Cookie
      },
      success(res) {
        console.log('触发updatePgnum', res.data)

        that.setData({
          price: res.data.fee
        })
      }
    })
  },
  cancel: function (e) {
    console.log(e)
    wx.reLaunch({
      url: './index'
    })
  },
  submit: function () {
    if (this.data.pgnum == 0) {
      Notify({ type: 'primary', message: '未上传文件' })
    } else {
      var url = '/pages/payment/payment?price=' + this.data.price
      wx.navigateTo({
        url: url,
      })
    }
  },

  initialize: function () { //在getStatus重用于初始化
    var that = this
    return new Promise((resolve, reject) => {
      wx.request({
        url: curDomain + '?code=' + that.data.code,
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
  // bindColorChange: function(e) {  
  //   this.setData({  
  //     color_index: e.detail.value  
  //   })
  //   if (this.data.isupload) {
  //     //this.updatePgnum() 因只有黑色，暂不启用
  //   }else{
  //     Notify({ type: 'primary', message: '未上传文件' })
  //   }
  // },
  // bindSizeChange: function(e){
  //   this.setData({
  //     size_index: e.detail.value
  //   })
  //   if (this.data.isupload) {
  //     //this.updatePgnum() 因只有A4，暂不启用
  //   }else{
  //     Notify({ type: 'primary', message: '未上传文件' })
  //   }
  // },
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

  handleBtnEvent(e) {
    // 按钮组点击触发，接收子组件传过来的数据，进行操作
    //console.log('handleBtnEvent：',e.detail)
    let currentId = e.detail.currentId
    let tmpSides = ''
    if (currentId === "0") {
      tmpSides = 'one-sided'
    } else if (currentId === "1") {
      tmpSides = 'two-sided-long-edge'
    } else if (currentId === "2") {
      tmpSides = 'two-sided-short-edge'
    }
    console.log(tmpSides)
    this.setData({
      sides: tmpSides
    })
    if (this.data.isupload) {
      this.updatePgnum()
    } else {
      Notify({ type: 'primary', message: '未上传文件' })
    }
  },

  onQtyChange: function (e) {
    var that = this
    // console.log(e.detail);
    Toast.loading({
      message: '加载中...',
      forbidClick: true
    });
    setTimeout(() => {
      Toast.clear();
      this.setData({
        qty: e.detail
      })
      that.updatePgnum();
    }, 400)

  },

  getStatus: function () { //获取打印机状态
    var that = this
    wx.request({
      url: curDomain + 'api/status',
      method: 'GET',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        console.log('获取打印机状态：', res)
        let status = res.data.backend_status
        if (status == "ok") {
          that.setData({
            backend_status: true
          });
          that.initialize().then((res) => {
            console.log('初始化会话：', res)
            app.globalData.Cookie = res.cookies[0]
            // console.log(app.globalData)
          })
            .catch((error) => {
              console.error('初始化会话失败：', error)
            })
        } else if (res.statusCode == 404 && res.data.includes("Tunnel")) {
          that.setData({
            offlineInfo: '服务器掉线'
          })
        } else if (res.statusCode == 503) {
          let info = ''
          info = res.data.error_message
          that.setData({
            offlineInfo: info
          })
        } else {
          that.setData({
            offlineInfo: '应用框架异常'
          })
        }
      }
    })
  },

  localPost: function () { //本地上传
    var that = this
    //console.log(that.data.filename,that.data.pgnum)
    wx.request({
      url: curDomain + 'local_upload',
      method: 'POST',
      data: {
        "fileName": that.data.filename,
        "pages": that.data.pgnum
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'Cookie': app.globalData.Cookie
      },
      success(res) {
        console.log('触发localPost：', res)
        that.updatePgnum()
      }
    })
  },

  /**
  * 生命周期函数--监听页面加载
  */
  onLoad(options) {
    console.log(curDomain)
    var that = this;
    wx.login({
      success: (result) => {
        console.log('wx.login success', result)
        that.setData({
          code: result.code
        })
        app.globalData.code = result.code
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
    this.btnGroup = this.selectComponent("#btn-group")
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    //console.log('onShow: ',app.globalData.Cookie)
    if (this.data.islocal) {
      this.localPost();
      //本地上传的，先传cookie在获取打印费用
    }
  },
})