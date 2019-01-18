<template>
  <div class="person-upload clear width" id="person_upload" v-if="photos">
    <div class="total-num">共{{count}}作品</div>
    <image_box :image_list="photos"/>
      <!--<upload_card/>-->
      <!--<div class="image-item " v-for="(photo,index) in photos" :key="index" >-->
        <!--<div  class="item-content" :style="{'background-image':'url(' + photo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">-->
          <!--<div class="info" @click="showImageInfo(photo.id)" title="点击查看详情">-->
            <!--<a class="download-warp"  :href="photo.image.split('.400x300')[0]" @click.stop="setDownload(photo.id)" :download="photo.name">-->
              <!--<img  class="download-img" src="../../../../assets/download.svg">-->
              <!--<span class="download-span">下载</span>-->
            <!--</a>-->
          <!--</div>-->
        <!--</div>-->
        <!--<div class="photo-info">-->
          <!--<div class="works">-->
            <!--<div class=" works-name">{{photo.name}}</div>-->
            <!--<div class="blue-line"></div>-->
            <!--<div class=" works-type">{{photo.cates}}</div>-->
          <!--</div>-->
          <!--<div class="bottom-data">-->
            <!--<div class="img-warp">-->
              <!--<img src="../../../../assets/_download.png" /><span class="r1rem">{{photo.download_nums}}</span>-->
              <!--<img src="../../../../assets/_like.png" /><span class="r1rem">{{photo.like_nums}}</span>-->
              <!--<img src="../../../../assets/_collect.png" /><span class="r1rem">{{photo.collection_nums}}</span>-->
            <!--</div>-->
            <!--<span class="time">{{photo.add_time}}</span>-->
          <!--</div>-->
        <!--</div>-->
      <!--</div>-->
    <!--<div v-if="!count&&no_more">-->
      <!--<img src="../../../../assets/noResult.png" class="no-result-img">-->
      <!--<p class="no-result-word">你还没有上传作品哦~</p>-->
    <!--</div>-->
    <!--<div class="no-more-hint no-result-word" v-if="no_more&&count">没有更多了~</div>-->
    <!--<router-view/>-->
  </div>
</template>

<script>
  import upload_card from '../../../../components/card/doUpload_card'
  import cookie from '../../../../utils/cookie'
  import {setDownload, setImageInfo} from "../../../../utils/user";
  import image_box from '../../../../components/card/image_card'

    export default {
        name: "person_upload",
      components:{
        upload_card,
        image_box
      },
      data(){
          return {
            sw:true,
            no_more:false,
          }
      },
      computed:{
        photos(){
          return this.$store.state.user.upload_his
        },
        count(){
          return this.$store.state.user.up_count
        },
        page_nums(){

        }
      },
      created(){
          if(!this.photos.length){
            let id=cookie.getCookie('user_id')
            this.$store.commit('SET_UPLOAD_NEXT_PAGE',`user=${id}&page=1`)
            this.$store.dispatch('SetUploadHis');
          }
          window.addEventListener('scroll',this.getImage)
      },
      destroyed(){
        if(!this.$store.state.user.if_continue){
          this.$store.commit('SET_IF_CONTINUE',true)
        }
        window.removeEventListener('scroll',this.getImage)
      },
      methods:{
        showImageInfo(id){
         setImageInfo(id)
        },
        setDownload(id){
          setDownload(id)
        },
        getImage(){
          if (this.sw&&document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight-80){
            this.sw=false
            if(this.$store.state.user.upload_next_page&&this.$store.state.user.upload_next_page.indexOf('page=1')===-1){
              this.$store.dispatch('SetUploadHis').then(()=>{
                this.sw=true
              }).catch((res)=>{
                console.log(res)
              });
            }else{
              this.no_more=true
            }
          }
        }
      },
    }
</script>

<style scoped>
</style>
