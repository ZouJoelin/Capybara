const app = getApp();
const curDomain = app.globalData.curDomain //配置当前页面使用域名

const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : `0${n}`
}

const handleErrorMessage = (data) => {
  let error_message = JSON.parse(data).error_message
  wx.showModal({
    title: '提示',
    content: error_message,
    showCancel: false,
    success: (res) => {
      if (res.confirm) {
        wx.reLaunch({
          url: '/pages/index/index',
        })
      }
    }
  })
}

const strLenOptiize = (len,str) => { //处理字符串长度过长
  let tmp = str
  let name
  if (tmp.length < len) {
    name = tmp
  }else{
    name = tmp.substring(0,len)+'...'
  }
  return name
}

const getTodayShareTimes = () => { //获取用户今日转发次数
  return new Promise((resolve, reject) => {
    wx.request({
      url: curDomain+'api/get_today_share_times?open_id='+app.globalData.openid,
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success (res){
        console.log('api/get_today_share_times GET >>>',res)
        if(res.statusCode == 200){
          resolve(res.data.share_times) //返回今日转发次数
        }else{
          //console.error('api/get_today_share_times GET >>>',res)
          reject(new Error('api/get_today_share_times GET >>>' + res))
        }
      }
    })
  })
}

const shareIncentiveUtil = () => {
  return new Promise((resolve, reject) =>{
    wx.request({
      url: curDomain+'api/share_incentive?open_id='+app.globalData.openid+'&incentive='+app.globalData.incentive,
      method: 'GET',
      header: {
        'content-type': 'application/json',
        'Cookie' : app.globalData.Cookie
      },
      success(res){
        console.log('api/share_incentive GET >>>',res)
        if(res.statusCode == 403){
          console.log('api/share_incentive GET 403 >>>',res.data.error_message)
          reject(res.data)
        }else{
          resolve(res)
        }
      },
      fail: (error) => {
        reject(error)
      }
    })
  })
}

const getUserInfoUtil = () => { //向后台获取用户信息
  return new Promise((resolve, reject) => {
    wx.request({
      url: curDomain+'api/get_user_info?open_id='+app.globalData.openid,
      method: 'GET',
      header : {
        'Cookie' : app.globalData.Cookie
      },
      success: (res) => {
        if(res.statusCode == 403){
          console.log('api/get_user_info GET 403 >>>',res.data.error_message)
          reject(res.data)
        }else if(res.statusCode == 200){
          console.log('api/get_user_info GET 200 >>>',res.data)
          app.globalData.isLogin = true
          app.globalData.userInfo = res.data
          resolve(res.data) // 返回userInfo给调用方
        }else{
          reject(new Error('Unexpected status code: ' + res.statusCode))
        }
      },
      fail: (error) => {
        console.error(error)
        reject(error)
      }
    });

  })

}



module.exports = {
  formatTime,
  strLenOptiize,
  handleErrorMessage,
  getUserInfoUtil,
  getTodayShareTimes,
  shareIncentiveUtil
}
