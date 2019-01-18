<template>
  <div class="person_card">
    <div class="p-card-item" v-for="(item,index) in person_list">
      <div class="card-left">
        <div class="p-fan" v-if="$router.currentRoute.name==='ranking_list'">
          <div class="rank">{{index+1}}</div>
          <div class="fan-nums">
            <span>关注量</span><br/>
            <span>{{item.fan_nums}}</span>
          </div>
        </div>
        <img class="profile-photo" :src="item.image" @click="getInPerson(item.id)">
        <div class="p-info">
          <div class="p-name"><span>{{item.username}}</span>
            <img v-if="item.if_sign" src="../../assets/person_role/signed.png" title="签约摄影师">
            <img v-if="item.if_cer" src="../../assets/person_role/association.png" :title="item.org_name">
            <!--<img v-if="item.if_sign" src="../../assets/person_role/signed.png" title="">-->
          </div>
          <div class="p-desc">{{item.desc}}</div>
          <div class="btn-warp" @click="setFollow(item)">
            <input type="button" value="+关注"  v-if="!item.if_follow" class="follow unFollow"/>
            <input type="button" value="已关注" v-if="item.if_follow" class="follow followed"/>
          </div>
        </div>
      </div>
      <div class="p-image-wrap">
        <i class="p-card-image" v-for="img in item.images" :style="{'background-image':`url(${img.url})`}"></i>
        <!--http://118.24.96.186-->
      </div>
    </div>
  </div>
</template>

<script>
  import page_choice from '../page_choice'
  import {setFollow, setUnFollow} from "../../api/action";
  import {checkLogin, getInOtherUser} from "../../utils/user";
  export default {
    name: "person_card",
    components:{page_choice},
    props:{
      person_list:{},
      page_nums:{}
    },
    data(){
      return {
        show_fan:true
      }
    },
    methods:{
      setFollow(item) {
        if(checkLogin()){
          let data = new FormData();
          data.append('follow', item.id)
          data.append('fan', this.$store.state.user.userInfo.id);
          if (!item.if_follow) {
            setFollow(data).then((res) => {
              item.if_follow = res.data.id;
              this.$emit('newFollow',true)
            })
          } else {
            setUnFollow(item.if_follow).then(() => {
              item.if_follow = false;
              this.$emit('newFollow',false)
            })
          }
        }
      },
      getInPerson(id){
        getInOtherUser(id)
      },
    }
  }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .person_card{
    width: 108rem;
    margin: 0 auto;
    padding-bottom: 3rem;
    min-height: 60rem;
  }
  .p-card-item{
    height: 15rem;
    margin: 3rem 0;
    background: #fff;
    display: -webkit-flex; /* Safari */
    display: flex;
    justify-content: flex-start;
    align-items:center;
    transition: all 0.5s;
    padding: 1rem 3rem ;
  &:hover{
     box-shadow: 2px 2px 12px #e0e0e0;
   }
  }
  .card-left{
    width: 48%;
    display: flex;
    height: 100%;
  }
  .p-fan{
    width: 8rem;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  .fan-nums{
    margin-top: 1rem;
  }
  }
  .fan-nums :nth-child(1){
    font-size: $ms;
    color: $f-light;
  }
  .fan-nums :nth-child(3){
    display: inline-block;
    margin-top: .3125rem;
    font-weight: bold;
    font-size: $ls;
  }
  .profile-photo{
    width: 10rem;
    height: 10rem;
    border-radius: 10rem;
    margin: 1.5rem 0 1.5rem 2rem;
  }
  .p-info{
    display: -webkit-flex; /* Safari */
    display: flex;
    flex-direction:column;
    text-align: left;
    height: 100%;
    padding: 2.625rem 0 2.625rem 1.5rem;
  }
  .p-name{
    font-size: $ls;
    font-weight: bold;
    padding-bottom: .5rem;
  img{
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    margin-left: .5rem;
  }
  }
  .p-desc{
    width: 27rem;
    white-space: nowrap;
    overflow: hidden;
    height: 2*$ss;
    color: $f-light;
    font-size: $ss;
  }
  .btn-warp{
    padding-top: 2.125rem;
  }
  .rank{
    line-height: 4rem;
    font-size: 4rem;
  }
  .p-image-wrap{
    height: 100%;
    padding: .5rem 0;
  }
  .p-card-image{
    display: inline-block;
    width: 16rem;
    height: 100%;
    background: no-repeat center;
    -webkit-background-size: cover;
    background-size: cover;
    margin-right: 1.5rem;
  }
</style>
