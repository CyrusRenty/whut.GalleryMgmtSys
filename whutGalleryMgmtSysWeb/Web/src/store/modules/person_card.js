import {getFollowRankList,getSignedList} from "../../api/get";


const person_card={
  state:{
    rank_list:[],
    sign_list:[],
    rank_counts:0,
    sign_counts:0
  },
  mutations:{
    SET_RANK_LIST:(state,data)=>{
      state.rank_list=data.results
      state.rank_counts=data.count
    },
    SET_RANK_LIST_EMPTY:(state)=>{
      state.rank_list=[]
    },
    SET_SIGN_LIST:(state,data)=>{
      state.sign_list=data.results
      state.sign_counts=data.count
    },
    SET_SIGN_LIST_EMPTY:(state)=>{
      state.sign_list=[]
    },
  },
  actions:{
    GetRankList({commit},params){
      return new Promise((resolve,reject)=>{
         getFollowRankList(params).then((res)=>{
          commit('SET_RANK_LIST',res.data)
        }).catch((error)=>{
          reject(error)
        })
      })
    },
    GetSignList({commit},params){
      return new Promise((resolve,reject)=>{
         getSignedList(params).then(res=>{
          commit('SET_SIGN_LIST',res.data)
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
