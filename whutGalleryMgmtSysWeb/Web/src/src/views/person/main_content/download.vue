<template>
  <div class="person-download clear width" v-if="photos">
    <div class="fan-follow">
      <div class="top">
        <a @click="changeShow">我的粉丝({{fans.length}})</a>
        <a @click="changeShow">我的关注({{my_follow.length}})</a>
      </div>
      <div v-if="show_fan">
        <div v-for="item in fans">{{item.fan.username}}</div>
      </div>
      <div v-if="!show_fan">
        <div v-for="item in my_follow">{{item.follow.username}}</div>
      </div>
    </div>

      <div class="total-num">共{{count}}作品</div>
      <div class="image-item " v-for="(photo,index) in photos" :key="index" >
        <div  class="item-content" :style="{'background-image':'url(' + photo.image.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
          <div class="info" @click="showImageInfo(photo.image.id)" title="点击查看详情">
            <a class="download-warp"  :href="photo.image.image.split('.400x300')[0]" @click.stop="setDownload(photo.image.id)" :download="photo.image.name">
              <img  class="download-img" src="../../../assets/download.svg">
              <span class="download-span">下载</span>
            </a>
          </div>
        </div>
        <div class="photo-info">
          <div class="works">
            <div class="works-name">{{photo.image.name}}</div>
            <div class="works-type">{{photo.image.cates}}</div>
          </div>
          <div class="bottom-data">
            <div class="img-warp">
              <img src="../../../assets/_download.png"/><span class="r1rem">{{photo.image.download_nums}}</span>
              <img src="../../../assets/_like.png"/><span class="r1rem">{{photo.image.like_nums}}</span>
              <img src="../../../assets/_collect.png" /><span class="r1rem">{{photo.image.collection_nums}}</span>
            </div>
            <span class="time">{{photo.image.add_time}}</span>
          </div>
        </div>
      </div>
    <div v-if="count===0" >
      <img src="../../../assets/noResult.png" class="no-result-img">
      <p class="no-result-word">你还没有下载记录哦~</p>
    </div>
  </div>
</template>
<script>
  import {setImageInfo,setDownload} from "../../../utils/user";
  import {getFans, getMyFollow} from "../../../api/get";

  export default {
        name: "download",
      data(){
          return {
            sw:true,
            no_result:false,
            fans:[],
            my_follow:[],
            show_fan:true
          }
      },
      computed:{
        photos(){
          return this.$store.getters.download_his
        },
        count(){
          return this.$store.state.user.down_count
        }
      },
      created(){
        if(this.$store.state.user.download_next_page==='page=1')
        this.$store.dispatch('SetDownLoadHis').then(()=>{
        }).catch((res)=>{
          console.log(res)
        })
        window.addEventListener('scroll',this.getImage)
      },
      mounted(){
          this.getFans()
        this.getMyFollow()
      },
      destroyed(){
        window.removeEventListener('scroll',this.getImage)
      },
      methods:{
        showImageInfo(id){
         setImageInfo(id)
        },
        getImage(){
          if (this.sw&&document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight-80){
            this.sw=false
            if(this.$store.state.user.download_next_page&&this.$store.state.user.download_next_page.indexOf('page=1')===-1){
              this.$store.dispatch('SetDownLoadHis').then(()=>{
                this.sw=true
              }).catch((res)=>{
                console.log(res)
              });
            }
          }
        },
        setDownload(id){
          setDownload(id)
        },
        getFans(){
          getFans().then((res)=>{
            this.fans=res.data
          })
        },
        getMyFollow(){
          getMyFollow().then((res)=>{
              this.my_follow=res.data
            }
          )
        },
        changeShow(){
          this.show_fan=!this.show_fan
        }
      },

    }
</script>

<style scoped>
  .fan-follow{
    height: 50rem;
    padding: 5rem 6rem;
    text-align: left;
  }
</style>
