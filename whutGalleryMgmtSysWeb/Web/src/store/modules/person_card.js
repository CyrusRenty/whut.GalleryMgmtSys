import {getFollowRankList,getSignedList} from "../../api/get";
import user from "./user";

const person_card={
  state:{
    baseurl:'http://10.138.207.222:8000',
    rank_list:{},
    sign_list:{},
    show_rank:true,
    rank_next_page:'',
    sign_next_page:''
  },
  mutations:{
    SET_RANK_LIST:(state,data)=>{
      state.rank_list=data
    },
    SET_SIGN_LIST:(state,data)=>{
      state.sign_list=data
    },
    SET_NEXT_RANK_PAGE:(state,data)=>{
      state.rank_next_page=data
    },
    SET_NEXT_SIGN_PAGE:(state,data)=>{
      state.sign_next_page=data
    }
  },
  actions:{
    GetRankList({commit}){
      return new Promise((resolve,reject)=>{
         getFollowRankList().then((res)=>{
           if(res.data.next===null){
             commit('SET_NEXT_RANK_PAGE',null)
           }
           else commit('SET_NEXT_RANK_PAGE',res.data.next.split("?")[1])
          commit('SET_RANK_LIST',res.data.results)
        }).catch((error)=>{
          reject(error)
        })
      })
    },
    GetSignList({commit}){
      return new Promise((resolve,reject)=>{
         getSignedList().then(res=>{
           if(res.data.next===null){
             commit('SET_NEXT_SIGN_PAGE',null)
           }
           else commit('SET_NEXT_SIGN_PAGE',res.data.next.split("?")[1])
          commit('SET_SIGN_LIST',res.data.results)
        }).catch((error)=>{
          reject(error)
        })
      })
    }
  }
}
export default person_card
function setUrl(data){
  data.forEach((item)=>{
    item.image=person_card.state.baseurl+item.image
    item.user_image=person_card.state.baseurl+item.user_image
  })
  return data
}
