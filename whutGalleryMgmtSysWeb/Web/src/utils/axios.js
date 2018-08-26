import axios from 'axios'
import cookie from './cookie'
axios.interceptors.request.use(
  config=>{
      if(cookie.getCookie('token')){
        config.headers.Authorization=`JWT ${cookie.getCookie('token')}`
      }
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
