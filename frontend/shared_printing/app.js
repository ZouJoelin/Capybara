// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    // wx.login({
    //   success: res => {
    //     // 发送 res.code 到后台换取 openId, sessionKey, unionId
    //   }
    // })
  },
  /*
  miniprogram分支使用网址：https://capybara.mynatapp.cc/
  dev分支使用网址：https://campusprinter.nat300.top/
  devDomain: 'http://campusprinter.nat300.top/',
  https://capybara-dev.mynatapp.cc/
  domain: 'https://capybara.mynatapp.cc/',
  */
  globalData: {
    userInfo: null,
    isLogin: false, //用户是否已注册
    openid: '',
    code: '',//登录凭证,在index.js中获取
    Cookie: null,
    curDomain: 'https://capybara-dev.mynatapp.cc/'
  }
})
