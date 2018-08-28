<template>
  <div class="main-image clear width" v-if="photos">
    <div v-if="search_context" class="search_context">{{search_context}}的搜索结果如下</div>
  <div class="image-item " v-for="(photo,index) in photos" :key="index" ref="image_item">
    <div  class="item-content" :style="{'background-image':'url(' + photo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
      <div class="info" @click="showImageInfo(photo.id)" title="点击查看详情" v-if="has_token">
        <div class="btn-warp clear">
          <div class="collect-btn clear" :class="{'btn-active':photo.if_collect}" @click.stop="showCollect(photo.id,index)" title="收藏">
            <img class="btn-img" :src="photo.if_collect?collect:unCollect">
            <span class="btn-span">{{photo.collection_nums}}</span>
          </div>
          <div class="like-btn" :class="{'btn-active':photo.if_like}" @click.stop="setLike(photo.id,index)" title="点赞">
            <img class="btn-img"  :src="photo.if_like?like:unlike">
          <span class="btn-span">{{photo.like_nums}}</span>
          </div>
        </div>
        <a class="download-warp"  :href="photo.image.split('.400x300')[0]" @click.stop="setDownload(photo.id)" :download="photo.name" title="点击下载">
          <img  class="download-img" src="../../assets/download.svg">
          <span class="download-span">下载</span>
        </a>
      </div>
    </div>
    <div class="photo-info">
    <div class="works">
      <div class="works-name">{{photo.name}}</div>
      <div class="works-type">{{photo.cates}}</div>
    </div>
    <div class="author">
      <i class="user-image" :style="{'background-image':'url(' + photo.user.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }" @click="getInOtherUser(photo.user.id)" @mouseenter="showPersonCard(index)" @mouseleave="showPersonCard" :title="'进入'+photo.user.username+'的主页'"></i>
      <div class="author-name floatL">{{photo.user.username}}</div>
      <div  @click="setFollow(photo.user.id,index)"><div class="unFollow follow" v-if="!photo.if_follow" title="关注">+关注</div><div class="followed follow" v-if="photo.if_follow" title="取消关注">已关注</div></div>
    </div>
    </div>
    <div class="author-detail" v-if="show_person_card===index">
      <div class="author-big-pic" :style="{'background-image':'url(' + photo.user.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
      </div>
      <span class="person-card-name">{{photo.user.username}}</span>
      <div class="products-and-fans">
        <div class="nums-info author-products">
          <span class="nums-info-title">作品</span>
          <span class="author-nums">{{photo.user.upload_nums}}</span>
        </div>
        <div class="nums-info author-fans">
          <span class="nums-info-title">粉丝</span>
          <span class="author-nums">{{photo.user.fan_nums}}</span>
        </div>
      </div>
    </div>
  </div>
    <div v-if="no_result">
      <img src="../../assets/noResult.png" class="no-result-img">
      <p class="no-result-word">没有找到符合条件的结果</p>
    </div>
  </div>
</template>

<script>
  import {setLike,setUnLike,setFollow,setUnFollow,download} from "../../api/action";
  import mock from '../../utils/mock'
  import {getInOtherUser, setDownload, setImageInfo} from "../../utils/user";

    export default {
      name: "image_card",
      data(){
        return {
          like:require('../../assets/image_like.png'),
          unlike:require('../../assets/image_unlike.png'),
          collect:require('../../assets/image_collect.png'),
          unCollect:require('../../assets/image_unCollect.png'),
          show_person_card:-1,
          sw:true,
          no_more:false,
        }
      },
      computed:{
        photos(){
          return this.$store.getters.image
        },
        if_continue(){
          return this.$store.state.imageGroup.continue_getImage
        },
        has_token(){
          return this.$store.state.user.token
        },
        search_context(){
          return this.$store.state.imageGroup.search_context
        },
        no_result(){
          return this.$store.state.imageGroup.no_result
        }
       },
      created(){
      },
      mounted(){
      },
      destroyed(){
        this.$store.commit('SET_MAIN_SEARCH',false)
        window.removeEventListener('scroll',this.get)
      },
      methods:{
        setLike(id,index){
          let data=new FormData();
          data.append('image',id)
          data.append('user',this.$store.state.user.userInfo.id)
          if(!this.photos[index].if_like){
            setLike(data).then((res)=>{
              this.photos[index].if_like=res.data.id
              this.photos[index].like_nums++
            }).catch((error)=>{
              console.log(error)
            })
          }else{
            setUnLike(this.photos[index].if_like).then(()=>{
              this.photos[index].if_like=false
              this.photos[index].like_nums--
            })
          }
        },
        showCollect(id,index){
            this.$store.commit('SET_IMAGE_ID',id);
            this.$store.commit('SET_INDEX',index)
            //this.photos[index].collect++;
            this.$store.commit('SET_COLLECT_LIST',id);
            this.$store.commit('SET_COLLECT_SHOW');
            document.body.style.overflow='hidden';
        },
        setFollow(id,index){
          let data=new FormData();
          data.append('follow',id)
          data.append('fan',this.$store.state.user.userInfo.id)
          if(!this.photos[index].if_follow){
            setFollow(data).then((res)=>{
              this.photos[index].if_follow=res.data.id
             this.photos.forEach((item)=>{
                if(item.user.id===id)
                  item.if_follow=res.data.id
              })
            })
          }else{
            setUnFollow(this.photos[index].if_follow).then(()=>{
              this.photos[index].if_follow=false
              this.photos.forEach((item)=>{
                if(item.user.id===id)
                  item.if_follow=false
              })
            })
          }
        },
        showImageInfo(id) {
          setImageInfo(id)
        },
        setDownload(id) {
         setDownload(id)
        },
        getInOtherUser(id){
          getInOtherUser(id)
        },
        get(){
          if (this.sw&&document.documentElement.scrollTop + document.documentElement.clientHeight >= document.documentElement.scrollHeight - 50) {
            this.sw = false;
              if(this.$store.state.imageGroup.continue_getImage&&this.$store.state.imageGroup.main_next_page.indexOf('page=1')===-1){
                if(this.$store.state.imageGroup.status==='normal'){
                  this.$store.dispatch('setImageGroupI').then(()=>{
                    this.no_more=false
                    this.sw=true
                  })
                }else{
                  this.$store.dispatch('setImageGroupT').then(()=>{
                    this.no_more=false
                    this.sw=true
                  })
                }
              }else {
                this.sw=true;
                this.no_more=true
              }
          }
        },
        showPersonCard(index){
          this.show_person_card=index
        },
        unshowPersonCard(){
          this.show_person_card=-1
        }
        },
    }
</script>

<style scoped>
  .main-image{
    padding: 3rem 0;
    margin: 0 auto;
    height: 76.6rem;
  }
  .floatL{
    float: left;
  }
  .search_context{
    width: 100%;
    text-align: left;
    font-size: 1.3rem;
    margin: 1rem 0;
    margin-left: 1.5rem;
    font-weight: bold;
  }


/*
person-card
 */
  .author-detail{
    position: absolute;
    top:0;
    width: 100%;
    height: 27.25rem;
    background: white;
    box-shadow:0.125rem 0.125rem 0.875rem #D6D6D6;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    line-height: 3rem;
    z-index: 2;
    font-size: 1.25rem;
    font-weight: bold;
  }

  .author-detail:before{
    content: "";
    display: block;
    position: absolute;
    border: 0.75rem solid transparent;
    border-top-color: white;
    left: 2.2rem;
    bottom: -1.5rem;
  }

  .author-big-pic{
    display: inline-block;
    width: 10rem;
    height: 10rem;
    border-radius: 10rem;
  }

  .person-card-name{
    font-size: 1.5rem;
  }

  .products-and-fans{
    display: flex;
  }

  .nums-info{
    display: flex;
    flex-direction: column;
    line-height: 2rem;
    padding: 0 3rem 0;
    margin-top: 2rem;
  }

  .author-products{
    border-right: 0.125rem solid #cecece;
  }

  .nums-info-title{
    color: #9b9b9b;
  }

  .author-nums{
    font-weight: bold;
  }

</style>
