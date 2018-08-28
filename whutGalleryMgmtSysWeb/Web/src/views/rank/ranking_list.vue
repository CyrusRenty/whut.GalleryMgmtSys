<template>
  <div class="ranking-list">
    <Lgts_head/>
    <div class="billboard">
      <div class="person-card-item-wrap">
        <div class="billboard-item" v-for="(item,index) in list">
          <div class="card-left">
            <div class="person-downloads">
              <div class="rank">{{index+1}}</div>
              <div class="download-info">
                <span>关注量</span><br/>
                <span>{{item.fan_nums}}</span>
              </div>
            </div>
            <img class="profile-photo" :src="item.image" @click="getInPerson(item.id)">
            <div class="person-information">
              <div class="id-info">
                <span class="username">{{item.username}}</span><div class="identify" v-if="item.if_sign"><img src="../../assets/signed.png"></div></div>
              <span class="brief-introdution"></span>
              <div class="follow-button" @click="setFollow(index)">
                <input type="button" value="+关注"  v-if="!item.if_follow" class="person-card-follow"/>
                <input type="button" value="已关注" v-if="item.if_follow" class="person-card-follow"/>
              </div>
            </div>
          </div>
          <div class="person-works" v-for="img in item.images">
            <img :src="img.url"  class="person-card-image"/>
          </div>
        </div>
      </div>
     </div>
    <tslg_footer/>
  </div>
</template>

<script>
  import Lgts_head from '../../components/body/tslg_header'
  import tslg_footer from '../../components/body/tslg_footer'
  import {setFollow,setUnFollow} from "../../api/action";
  import {getInOtherUser} from "../../utils/user";
    export default {
        name: "rankingList",
        components: {tslg_footer,Lgts_head},
      data(){
          return {
            sw:true
          }
      },
      created(){
          if(!this.list.length)
        this.$store.dispatch('GetRankList')
      },
      mounted(){
        window.addEventListener('scroll',this.getMorePersonCard)
      },
      destroyed(){
        window.removeEventListener('scroll',this.getMorePersonCard)
      },
      computed:{
        list(){
          return this.$store.state.person_card.rank_list
        }
      },
      methods: {
        setFollow(index) {
          let data = new FormData();
          data.append('follow', this.list[index].id)
          data.append('fan', this.$store.state.user.userInfo.id)
          console.log(data)
          if (!this.list[index].if_follow) {
            console.log('get in')
            setFollow(data).then((res) => {
              this.list[index].if_follow = res.data.id
              this.$store.state.person_card.list.forEach((item) => {
                if (item.user.id === id)
                  item.if_follow = true
              })
            })
          } else {
            setUnFollow(this.list[index].if_follow).then(() => {
              this.list[index].if_follow = false
              this.$store.state.person_card.image.forEach((item) => {
                if (item.user.id === id)
                  item.if_follow = false
              })
            })
          }
        },
        getMorePersonCard(){
          if(this.sw&&document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight-80){
            this.sw=false
            if(this.$store.state.person_card.rank_next_page){
              this.$store.dispatch('GetRankList').then(()=>{
                this.sw=true
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

<style scoped>

</style>
