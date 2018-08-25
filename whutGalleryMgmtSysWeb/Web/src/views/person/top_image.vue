<template>
  <div id="userInfo">
    <div id="centerBg" class="pic-box"></div>
    <div  class="user-box">
      <div class="center-tx" :style="{'background-image':`url(${userInfo.image})`}">
        <div class="person-data person-fan" @click="goFanFollow"><span>粉丝</span><br/><span>{{userInfo.fan_nums}}</span></div>
        <div class="person-data person-follow" @click="goFanFollow"><span class="">关注</span><br/><span>{{userInfo.follow_nums}}</span></div>
      </div>
    </div>
    <div id="centerbtn">
      <span class="lh4r">{{userInfo.username}}</span><br/>
      <span class="person-desc" title="个人简介">{{userInfo.desc}}</span>
    </div>
  </div>
</template>

<script>

  export default {
        name: "Lgts_centerBg",
      computed:{
          userInfo(){
            return this.$store.state.user.userInfo
          },
      },
    created(){

    },
      mounted(){

    },
      methods:{
        goFanFollow(){
          this.$router.push({name:'person_download'})
        }
      }
    }
</script>

<style scoped>
  #userInfo{
    background: #fff;
  }
  .pic-box{
    width: 100%;
    height: 25rem;
    background:url(../../assets/personBg.jpg) #cecece no-repeat center;
    background-size: cover;
  }
  .user-box{
    width:100%;
    margin-top: -5rem ;
  }
  .center-tx{
    box-sizing: padding-box;
    width: 10rem;
    height: 10rem;
    border-radius: 10rem;
    background: transparent no-repeat center;
    background-size: cover;
    border: 0.5rem solid white;
    position: relative;
    margin: auto;
    color: white;
    font-size: 1.25rem;
  }
  #centerbtn{
    font-size: 1.5rem;
    padding-bottom: 0.6rem;
  }
  .lh4r{
    line-height: 4rem ;
  }
  .person-data{
    position: absolute;
    top:0;
    cursor: pointer;
  }
  .person-fan{
    left: -8.5rem;
  }
  .person-follow{
    right: -8.5rem;
  }
  .person-desc{
    display:inline-block;
    width: 20rem;
    font-size:1.25rem;
    color: #9e9e9e;
    text-align: center;
    word-break: break-all;
  }
</style>
