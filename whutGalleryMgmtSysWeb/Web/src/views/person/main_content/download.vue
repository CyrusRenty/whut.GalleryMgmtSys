<template>
  <div class="person-download clear width" v-if="photos">
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

  export default {
        name: "download",
      data(){
          return {
            sw:true,
            no_result:false,
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
        }
      },

    }
</script>

<style scoped>
</style>
