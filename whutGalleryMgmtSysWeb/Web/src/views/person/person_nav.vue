<template>
  <div class="person-nav">
    <router-link :to="item.router" v-for="(item,index)  in person_nav" :key="index" class="user-choice" >{{item.text}}</router-link>
    </div>
</template>

<script>
  import cookie from '../../utils/cookie'
    export default {
        name: "person_nav",
        data:function () {
          return {
            person_nav:[
              {text:"我的作品",router:'/tslg/person/upload',click:this.getUpload},
              {text:"我的收藏",router:'/tslg/person/collection',click:this.getCollection},
              {text:"下载历史",router:'/tslg/person/download',click:this.getDownload}],
          }
        },
      beforeRouteUpdate(to,from,next){
          document.documentElement.scrollTop=0
        next()
      },
      methods:{
          getUpload(){
            this.$store.dispatch('SetUploadHis',cookie.getCookie('user_id')).then();
          },
        getCollection(){
            this.$store.dispatch('SetCollection')
        },
        getDownload(){
          this.$store.dispatch('SetDownLoadHis')
        }
      }
    }
</script>

<style scoped>
  .person-nav{
    height: 5rem;
    width: 100%;
    background: #fff;
    padding:1rem 0;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .user-choice{
    width: 10rem;
    height: 100%;
    background: #fff;
    color: #4a4a4a;
    cursor:pointer;
    font-size: 1.5rem;
  }
  .router-link-active{
    color:#9ad3e2;
  }
</style>
