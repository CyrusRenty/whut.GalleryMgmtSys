import {setLike,setUnLike,download} from "../api/action";
import store from '../store'
import router from '../router'
const user= {
  setLike(id, index) {
    let data = new FormData();
    data.append('image', id)
    data.append('user', this.$store.state.user.userInfo.id)
    if (!this.$store.state.imageGroup.image[index].if_like) {
      setLike(data).then((res) => {
        this.$store.state.imageGroup.image[index].if_like = res.data.id
        this.$store.state.imageGroup.image[index].like_nums++
      }).catch((error) => {
        console.log(error)
      })
    } else {
      setUnLike(id).then(() => {
        this.$store.state.imageGroup.image[index].if_like = false
        this.$store.state.imageGroup.image[index].like_nums--
      })
    }
  },
  checkNumber(str){
    if(str.length>11){
      return '输入数字长度不合法'
    }else if(str.charAt(0)==="0"||parseFloat(str)!==parseInt(str)){
      return '输入格式错误'
    }else return ''
  },
}

export function setImageInfo(id) {
  const {href} = router.resolve({
    name: 'image',
    params: {
      id:id
    }
  })
  window.open(href, '_blank')
}
export function setDownload(id){
  let data=new FormData
  data.append('image',id)
  download(data).then((res)=>{})
}
export function getInOtherUser(id){
  if(id===store.state.user.userInfo.id)
    router.push('/tslg/person')
  else{
    store.commit('SET_OTHER_NEXT_PAGE',`user=${id}&page=1`)
    store.commit('SET_OTHER_IMAGES_ENPTY')
    router.push({name:'other_user',params:{Id:id}})
  }
}
export function goLogin() {
  store.commit('SET_DO_LOGIN',true)
  router.push('/tslg/login')
}
export function goRegister() {
  store.commit('SET_DO_LOGIN',false)
  router.push({name:'login'})
}
