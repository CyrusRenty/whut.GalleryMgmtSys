import axios from 'axios'
import cookie from './cookie'
axios.interceptors.request.use(
  config=>{
      if(cookie.getCookie('token')){
        config.headers.Authorization=`JWT ${cookie.getCookie('token')}`
      }
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];


    return config
},
  err=>{
    return Promise.reject(err)
})

axios.interceptors.response.use(
  response=>{
    return response
  },
  error => {
    if(error.response){
      switch(error.response.status){

      }
    }
  }
)
export default axios
