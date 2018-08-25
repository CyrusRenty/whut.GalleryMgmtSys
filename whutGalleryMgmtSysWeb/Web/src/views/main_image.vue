<template>
    <div id="main-image">
      <div v-for="(item,index) in nav_items" class="main-item-box">
        <div class="title-wrap">
           <a>{{nav_items[index].first.name}}</a><a v-for="item_title in nav_items[index].second">{{item_title.name}}</a>
          <a class="more">更多</a>
        </div>
        <div class="image-wrap clear">
          <div v-for="(item_image,image_index) in nav_items[index].image" class="image-box">
            <div class="image-content" :style="{'background-image':`url(${item_image.image})`}">
              <div class="image-up" @click="showImageInfo(item_image.id)">
                <div class="btn-warp clear">
                  <div class="collect-btn" :class="{'btn-active':item_image.if_collect}" @click.stop="showCollect(item_image)" title="收藏">
                    <img class="btn-img" :src="item_image.if_collect?collect:unCollect">
                    <span class="btn-span">{{item_image.collection_nums}}</span>
                  </div>
                  <div class="like-btn" :class="{'btn-active':item_image.if_like}" @click.stop="setLike(item_image.id,index,image_index)" title="点赞">
                    <img class="btn-img"  :src="item_image.if_like?like:unlike">
                    <span class="btn-span">{{item_image.like_nums}}</span>
                  </div>
                </div>
                <a class="download-warp"  :href="item_image.image.split('.400x300')[0]" @click.stop="setDownload(item_image.id)" :download="item_image.name" title="点击下载">
                  <img  class="download-img" src="../assets/download.svg">
                  <span class="download-span">下载</span>
                </a>
              </div>
            </div>
            <div class="image-name">{{item_image.name}}</div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import {getTitle, getTypeImage} from "../api/get";
    import {setLike, setUnLike} from "../api/action";
    import {setDownload, setImageInfo} from "../utils/user";
  //https://i.pinimg.com/564x/89/f5/6f/89f56ff9fb2d02c2e3673d1513d93ad1.jpg
    export default {
        name: "main_image",
      data(){
          return {
            nav_items:[

            ],
            like:require('../assets/image_like.png'),
            unlike:require('../assets/image_unlike.png'),
            collect:require('../assets/image_collect.png'),
            unCollect:require('../assets/image_unCollect.png'),
          }
      },
      mounted(){
         this.get()
      },
      methods:{
        get(){
            getTitle().then((res)=>{
              for(let i=0;i<res.data.length;i++){
                let a={first:{},second:[],image:[]}
                a.first={name:res.data[i].name,id:res.data[i].id}
                a.second=res.data[i].kids
                getTypeImage(`group/${i+1}/?page=1&num=4`).then((res)=>{
                  a.image=res.data.results
                })
                this.nav_items.push(a)
              }
              //console.log(this.nav_items)
            })
          },
        setLike(id,index,image_index){
          let item=this.nav_items[index].image[image_index]
          let data=new FormData();
          data.append('image',id)
          data.append('user',this.$store.state.user.userInfo.id)
          if(!item.if_like){
            setLike(data).then((res)=>{
              item.if_like=res.data.id
              item.like_nums++
            }).catch((error)=>{
              console.log(error)
            })
          }else{
            setUnLike(item.if_like).then(()=>{
              item.if_like=false
              item.like_nums--
            })
          }
        },
        showCollect(item){
          //设置操作图片的id
          this.$store.commit('SET_IMAGE_ID',item.id);
          this.$store.commit('SET_COLLECT_ITEM',item)
          this.$store.commit('SET_COLLECT_LIST',item.id);
          this.$store.commit('SET_COLLECT_SHOW');
          document.body.style.overflow='hidden';
        },
        setDownload(id){
          setDownload(id)
        },
        showImageInfo(id){
          setImageInfo(id)
        }
      }
    }
</script>

<style scoped>
  #main-image{
    width: 111rem;
    margin: 3.75rem auto;
    background: #f7fafb;
  }
  .main-item-box{
    text-align: left;
    height: 35.32rem;
    margin-bottom: 3.75rem;
  }
  .title-wrap{
    margin-left: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .title-wrap a{
    margin-right: 3rem;
    font-size: 1.25rem;
    color: #9b9b9b;
    cursor: pointer;
  }
  .title-wrap a:hover{
    color: #9ad3e2;
  }
  .title-wrap a:nth-child(1){
    font-weight: 600;
    font-size: 1.5rem;
    color: #4a4a4a;
  }
  .title-wrap .more{
    float: right;
    margin-right: 1.5rem;
    display: flex;
    align-items: center;
  }
  .title-wrap .more:after{
    content: '';
    background: url(../assets/pull_down.png);
    background-size: 100% 100%;
    width: 1.2rem;
    height: .7rem;
    -webkit-transform: rotate(-90deg);
    transform: rotate(-90deg);
    display: inline-block;
    margin-left: .3rem;
  }
  .image-box{
    height: 32.32rem;
    width: 24.75rem;
    float: left ;
    margin: 0 1.5rem;
    box-shadow:0 0 4px #9B9B9B ;
  }
  .image-content{
    width: 100%;
    height: 28.75rem;
    background: no-repeat center;
    background-size: cover;
    position: relative;
  }
  .image-content .image-up{
    width: 100%;
    height: 100%;
    position: absolute;
    z-index: 1;
    background: rgba(0,0,0,.6);
    opacity: 0;
    cursor: pointer;
  }
  .image-content .image-up:hover{
      opacity: 1;
  }
  .image-name{
    font-size: 1.25rem;
    padding: .9rem 1.5rem;
  }
   .btn-warp{
    position:absolute;
    display: inline-block;
    z-index:3;
    top: 1.68rem;
    right: 1.375rem;
  }
   .collect-btn,.like-btn{
    display: inline-block;
    float: right;
    line-height: 1.375rem;
    height: 1.375rem;
    cursor: pointer;
    color: #fff;
    border: 0.0625rem solid #fff;
    border-radius: 1.375rem;
    padding: 0.3125rem 0.625rem;
    box-sizing: content-box;
  }
   .like-btn{
    margin-right: 0.625rem;
  }
   .btn-img{
    width: 1.375rem;
  }
   .btn-span{
    padding-left: 0.3215rem;
    float: right;
  }
   .btn-active{
    border:0.0625rem solid #9AD3E2;
    color:#9AD3E2;
  }
   .download-warp{
    width: 11.25rem;
    height: 3rem;
    background: #fff;
    border-radius: 3rem;
    position: absolute;
    z-index: 1;
    bottom: 3rem;
     right: 6.75rem;
    line-height:3rem ;
    cursor: pointer;
     display: flex;
     justify-content: center;
     align-items: center;
  }
   .download-img{
    width: 1.6rem;
     height: 1rem;
  }
   .download-span{
     font-size: 0.875rem;
     font-weight: 600;
  }
</style>
