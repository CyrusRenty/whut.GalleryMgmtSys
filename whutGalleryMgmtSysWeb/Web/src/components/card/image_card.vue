<template>
  <div class="main-image clear" v-if="image_list">
    <doUpload_card v-if="$router.currentRoute.meta.card"/>
    <div class="image-item " v-for="(photo,index) in image_list" :key="index" ref="image_item">
      <div v-if="$router.currentRoute.name==='ranking_list'" :class="{rank:true,first:index+1+(cur_page-1)*8===1,second:index+1+(cur_page-1)*8===2,third:index+1+(cur_page-1)*8===3}">{{index+1+(cur_page-1)*8}}</div>
      <div  class="item-content" :style="{'background-image':'url(' + photo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
        <div class="info" @click="showImageInfo(photo.id)" title="点击查看详情">
          <div class="btn-warp clear">
            <div class="collect-btn clear" :class="{'btn-active':photo.if_collect}" @click.stop="showCollect(photo)">
              <img class="btn-img" v-if="!photo.if_collect" src='../../assets/image_unCollect.png' title="收藏">
              <img class="btn-img" v-if="photo.if_collect" src='../../assets/image_collect.png' title="取消收藏">
              <span class="btn-span">{{photo.collection_nums}}</span>
            </div>
            <div class="like-btn" :class="{'btn-active':photo.if_like}" @click.stop="setLike(photo)" >
              <img class="btn-img" v-if="!photo.if_like" src='../../assets/image_unlike.png' title="点赞">
              <img class="btn-img" v-if="photo.if_like" src="../../assets/image_like.png" title="取消点赞">
              <span class="btn-span">{{photo.like_nums}}</span>
            </div>
          </div>
          <a class="download-warp" @click.stop="setDownload(photo)" title="点击下载">
            <img  class="download-img" src="../../assets/download.svg">
            <span class="download-span">下载</span>
          </a>
        </div>
      </div>
      <div  class="photo-info">
        <div class="works">
          <div class="works-name">{{photo.name}}</div>
          <div class="works-type">{{setCates(photo.cates)}}</div>
        </div>
        <div v-if="!show_data" class="author">
          <i class="user-image" :style="{'background-image':'url(' + photo.user.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }" @click="getInOtherUser(photo.user.id)" @mouseenter="showPersonCard(index)" @mouseleave="showPersonCard" :title="'进入'+photo.user.username+'的主页'"></i>
          <div class="author-name floatL">{{photo.user.username}}</div>
          <div @click="setFollow(photo)">
            <div class="unFollow follow" v-if="!photo.if_follow" title="关注">+关注</div>
            <div class="followed follow" v-if="photo.if_follow" title="取消关注">已关注</div>
          </div>
        </div>
        <div v-if="show_data" class="bottom-data">
        <div class="img-warp">
          <img src="../../assets/_download.png"/><span class="r1rem">{{photo.download_nums}}</span>
          <img src="../../assets/_like.png"/><span class="r1rem">{{photo.like_nums}}</span>
          <img src="../../assets/_collect.png" /><span class="r1rem">{{photo.collection_nums}}</span>
        </div>
        <span class="time">{{photo.add_time}}</span>
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
    <!--<div v-if="no_result">-->
      <!--<img src="../../assets/noResult.png" class="no-result-img">-->
      <!--<p class="no-result-word">没有找到符合条件的结果</p>-->
    <!--</div>-->
    <page_choice @cur_page="getCurPage" class="page" :page_nums="page_nums" v-if="show_page" />
    <collect ref="collect_list"/>
  </div>
</template>

<script>
  import {checkLogin, getInOtherUser, setDownload, setImageInfo, setLike, showCollect} from "../../utils/user";
  import {setFollow, setUnFollow} from "../../api/action";
  import collect from '../card/collect'
  import page_choice from '../page_choice'
  import doUpload_card from '../card/doUpload_card'

    export default {
        name: "image_card",
      components:{
          page_choice,
        collect,
        doUpload_card
      },
      props:['image_list','page_nums'],
      data(){
        return {
          show_person_card:-1,
          sw:true,
          no_more:false,
          cur_page:1,
          show_page:true,
          show_data:false,
        }
      },
      computed:{

      },
      created(){
        if(this.$router.currentRoute.name==='image'){
          this.show_data=true
          this.show_page=false
        }

      },
      methods:{
        setLike(item){
          setLike(item)
        },
        showCollect(item){
          if(checkLogin())
            this.$refs.collect_list.showCollect(item)
        },
        setFollow(item){
          if(checkLogin()) {
            let data = new FormData();
            data.append('follow', item.user.id)
            data.append('fan', this.$store.state.user.userInfo.id)
            let image_list=this.image_list
            if (!item.if_follow) {
              setFollow(data).then((res) => {
                for(let i=0;i<image_list.length;i++){
                  if(image_list[i].user.id===item.user.id)
                    image_list[i].if_follow=res.data.id
                }
              })
            } else {
              setUnFollow(item.if_follow).then(() => {
                for(let i=0;i<image_list.length;i++){
                  if(image_list[i].user.id===item.user.id)
                    image_list[i].if_follow=false
                }
              })
            }
          }
        },
        showImageInfo(id) {
          setImageInfo(id)
        },
        setDownload(item) {
            setDownload(item)
        },
        getInOtherUser(id){
          getInOtherUser(id)
        },
        showPersonCard(index){
          this.show_person_card=index
        },
        getCurPage(item){
          this.cur_page=item
          this.$emit('cur_page',item)
        },
        setCates(cates){
          let array=cates.split("、"),l_cate=[]
          for(let i=0;i<array.length;i++){
            let temp=array[i].split("/")
            l_cate.push(temp[temp.length-1])
          }
          cates=l_cate.join(" ")
          return cates
        }
      },
    }
</script >

<style lang="scss" scoped>
  .main-image{
    position: relative;
    margin: 0 auto 0;
    padding-bottom: 5rem;
    height: auto;
    min-height: 30rem;
  }
  .floatL{
    float: left;
  }

  .page{
    margin-bottom: 5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  .rank{
    position: absolute;
    left: 0.75rem;
    top: 0;
    width: 2rem;
    height: 2rem;
    background: #4a4a4a;
    color: #fff;
    line-height: 2rem;
    font-size: 1.1rem;
    z-index: 2;
  &:after{
     content: '';
     position: absolute;
     top: 2rem;
     left: 0;
     border: solid ;
     border-width: .5rem 1rem;
     border-color: #4a4a4a transparent transparent;
   }
  }
  .first{
    background-color: #fb2640;
  &:after{
     border-color: #fb2640 transparent transparent;
   }
  }
  .second{
    background: #f5a623;
  &:after{
     border-color: #f5a623 transparent transparent;
   }
  }
  .third{
    background-color: #ffd100;
  &:after{
     border-color: #ffd100 transparent transparent;
   }
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
