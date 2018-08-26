<template>
  <div class="other-user">
    <lgts_head/>
    <div class="userInfo" v-if="userInfo">
      <div class="pic-box"></div>
      <div  class="user-box">
        <div class="center-tx" :style="{'background-image':`url(${userInfo.image})`}">
          <div class="fan"><span>粉丝</span><br/><span>{{userInfo.fan_nums}}</span></div>
          <div class="follow"><span class="set-font">关注</span><br/><span>{{userInfo.follow_nums}}</span></div>
        </div>
      </div>
      <div class="center-btn">
        <span class="lh4r set-font">{{userInfo.username}}</span><br/>
        <span class="personInfo set-font f1-25r">{{userInfo.desc}}</span>
      </div>
      <div class="btn-follow-wrap sc-btn">
        <input type="button" value="返回" @click="getBack" class="cancel"/>
        <div @click="setFollow">
          <div class="unFollow follow" v-if="!userInfo.if_follow" title="关注">+关注</div>
          <div class="followed follow" v-if="userInfo.if_follow" title="取消关注">已关注</div>
        </div>
      </div>
    </div>
    <div class="other_user clear width" v-if="photos">
      <div class="total-num">共{{count}}作品</div>
      <div class="image-item " v-for="(photo,index) in photos" :key="index" >
        <div  class="item-content" :style="{'background-image':'url(' + photo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
          <div class="info" @click="showImageInfo(photo.id)" title="点击查看详情">
            <a class="download-warp"  :href="photo.image" @click.stop="setDownload(photo.id)" :download="photo.name">
              <img  class="download-img" src="../../../assets/download.svg">
              <span class="download-span">下载</span>
            </a>
          </div>
        </div>
        <div class="photo-info">
          <div class="works">
            <div class="works-name">{{photo.name}}</div>
            <div class="works-type">{{photo.cates}}</div>
          </div>
          <div class="bottom-data">
            <div class="img-warp">
              <img src="../../../assets/_download.png" /><span class="r1rem">{{photo.download_nums}}</span>
              <img src="../../../assets/_like.png" /><span class="r1rem">{{photo.like_nums}}</span>
              <img src="../../../assets/_collect.png"/><span class="r1rem">{{photo.collection_nums}}</span>
            </div>
            <span class="time">{{photo.add_time}}</span>
          </div>
        </div>
      </div>
      <div v-if="no_more">
        <img src="../../../assets/noResult.png" class="no-result-img">
        <p class="no-result-word">该用户暂无作品</p>
      </div>
    </div>
    <router-view/>
    <tslg_footer/>
  </div>

</template>

<script>
  import Lgts_head from '../../../components/body/Lgts_head'
  import tslg_footer from '../../../components/body/tslg_footer'
  import {setFollow, setUnFollow} from "../../../api/action";
  import {setImageInfo} from "../../../utils/user";

  export default {
        name: "other_user",
    components:{
      Lgts_head,
      tslg_footer
    },
    data(){
          return {
            sw:true,
            no_more:false,
          }
    },
    computed:{
      photos(){
        return this.$store.state.user.other_user_images
      },
      count(){
        return this.$store.state.user.other_count
      },
      userInfo(){
        return this.$store.state.user.other_userInfo
      },
      follow(){
        if(this.userInfo.if_follow)
          return '已关注'
        else return '关注'
      }
    },
    mounted(){
        document.documentElement.scrollTop = 0;
        window.addEventListener('scroll',this.getImage)
    },
    destroyed(){
      window.removeEventListener('scroll',this.getImage)
    },
    methods:{
      showImageInfo(id){
       setImageInfo(id)
      },
      setFollow(){
        let data=new FormData();
        data.append('follow',this.userInfo.id)
        data.append('fan',this.$store.state.user.userInfo.id)
        if(!this.userInfo.if_follow){
          setFollow(data).then((res)=>{
            this.userInfo.if_follow=res.data.id
            this.$store.state.imageGroup.image.forEach((item)=>{
              if(item.user.id===this.userInfo.id)
                item.if_follow=true
            })
          })
        }else{
          setUnFollow(this.userInfo.if_follow).then(()=>{
            this.userInfo.if_follow=false
            this.$store.state.imageGroup.image.forEach((item)=>{
              if(item.user.id===this.userInfo.id)
                item.if_follow=false
            })
          })
        }
      },
      getImage(){
        if (this.sw&&document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight-80){
          this.sw=false
          let page=this.$store.state.user.other_next_page
          if(page.indexOf('page=1')===-1&&page!==null){
              this.$store.dispatch('SetOtherUserImages').then(()=>{
                this.sw=true
              }) .catch((error)=>{
                console.log(error)
              })
          }
        }
      },
      getBack(){
        this.$router.go(-1)
      }
    },

  }
</script>

<style scoped>
  @media screen and (max-width: 300px) {
    .other_user{
      padding:0 1rem;
    }
  }
  .other_user{
    width: 100%;
    height: auto;
    padding: 2rem 4.5rem;
    background: #f7fafb;
  }

  .f1-25r{
    font-size:1.25rem;
  }
  .userInfo{
    background: #fff;
  }
  .pic-box{
    width: 100%;
    height: 400px;
    background:url(../../../assets/personBg.jpg) #cecece no-repeat center;
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
  .center-btn{
    height: auto;
    font-size: 1.5rem;
  }
  .lh4r{
    line-height: 4rem ;
  }
  .personInfo{
    color: #9e9e9e;
  }
  .btn-follow-wrap{
    height: 5rem;
    padding: 1rem 0;
  }
  .btn-follow-wrap div{
    display: inline-block;
  }
  .btn-follow-wrap .follow{
    height: 3rem;
    width: 7.5rem;
    line-height: 3rem;
    border-radius: 3rem;
  }
  .center-tx .fan{
    position: absolute;
    top:0;
    left: -8.5rem;
  }
  .center-tx .follow{
    position: absolute;
    top:0;
    right: -8.5rem;
  }


</style>
