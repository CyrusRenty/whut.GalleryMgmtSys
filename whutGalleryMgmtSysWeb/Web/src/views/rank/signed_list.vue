<template>
  <div class="signed-list">
    <Lgts_head/>
    <div class="ranking-list">
      <div class="p-card-wrap">
        <div class="p-card-item-wrap" v-if="list.length">
          <div class="p-card-item" v-for="(item,index) in list">
            <div class="card-left">
              <div class="p-fan">
              </div>
              <img class="profile-photo" :src="item.image" @click="getInPerson(item.id)">
              <div class="p-info">
                <div class="p-name"><span>{{item.username}}</span>
                  <img src="../../assets/person_role/signed.png" title="签约摄影师">
                </div>
                <div class="p-desc">{{item.desc}}</div>
                <div class="btn-warp" @click="setFollow(index)">
                  <input type="button" value="+关注"  v-if="!item.if_follow" class="follow unFollow"/>
                  <input type="button" value="已关注" v-if="item.if_follow" class="follow followed"/>
                </div>
              </div>
            </div>
            <div class="p-image-wrap">
              <i class="p-card-image" v-for="img in item.images" :style="{'background-image':`url(${img.url})`}"></i>
            </div>
          </div>
        </div>
        <page_choice @cur_page="Page" :page_nums="page_nums"/>
      </div>
    </div>
    <div class="no-result" v-if="show_no_result">
      暂无
    </div>
    <tslg_footer/>
  </div>
</template>

<script>
    import Lgts_head from '../../components/body/tslg_header'
    import tslg_footer from '../../components/body/tslg_footer'
    import page_choice from '../../components/page_choice'
    import {setFollow,setUnFollow} from "../../api/action";
    import {checkLogin, getInOtherUser} from "../../utils/user";

    export default {
        name: "cameraman",
        components: {tslg_footer,Lgts_head,page_choice},
      data(){
        return {
          sw:true,
          cur_page:1,
          show_no_result:false
        }
      },
      created(){
          if(!this.list.length)
          this.$store.dispatch('GetSignList',1)
      },
      mounted(){
        if(!this.list.length)
          this.show_no_result=true
      },
      computed:{
        list(){
          return this.$store.state.person_card.sign_list
        },
        page_nums(){
          return Math.ceil(this.$store.state.person_card.sign_counts/4)
        }
      },
      methods: {
        setFollow(index) {
          if(checkLogin()){
            let data = new FormData();
            data.append('follow', this.list[index].id)
            data.append('fan', this.$store.state.user.userInfo.id)
            console.log(data)
            if (!this.list[index].if_follow) {
              console.log('get in')
              setFollow(data).then((res) => {
                this.list[index].if_follow = res.data.id
              })
            } else {
              setUnFollow(this.list[index].if_follow).then(() => {
                this.list[index].if_follow = false
              })
            }
          }
        },
        getInPerson(id){
          getInOtherUser(id)
        },
        Page(cur_page){
          this.$store.commit('SET_SIGN_LIST_EMPTY')
          this.$store.dispatch('GetSignList',`${cur_page}`)
        }
      },
    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .signed-list{
    background: $bg;
    min-height:50rem;
  }
  .p-card-wrap{
    width: 108rem;
    padding-top: 3rem;
    margin: 0 auto;
  }
  .p-card-item-wrap{
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
  &:hover{
     box-shadow: 2px 2px 12px #e0e0e0;
   }
  }
  .card-left{
    width: 47%;
    display: flex;
    height: 100%;
  }
  /*
  different
   */
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
    margin: 2.5rem 0;
  }
  .p-info{
    display: -webkit-flex; /* Safari */
    display: flex;
    flex-direction:column;
    text-align: left;
    height: 100%;
    padding: 3.625rem 0 3.625rem 1.5rem;
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
    width: 20rem;
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
    padding: 1.5rem 0;
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
  .no-result{
    width: 100%;
    height: 40rem;
  }
</style>
