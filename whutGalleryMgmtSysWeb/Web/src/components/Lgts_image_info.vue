<template>
    <div class="image-info clear">
      <tslg_head/>
      <div class="warp clear">
        <div class="left">
          <img :src="imageInfo.image" class="image" >
          <div class="bot-btn">
            <div @click="setLike(imageInfo.id)" :class="{active_btn:imageInfo.if_like}"><img :src="imageInfo.if_like?liked:like"><span v-if="!imageInfo.if_like">点赞</span><span v-if="imageInfo.if_like">已点赞</span></div>
            <div @click="setCollect(imageInfo.id)" :class="{active_btn:imageInfo.if_collect}"><img :src="imageInfo.if_collect?collected:collect"><span v-if="!imageInfo.if_collect">收藏</span><span v-if="imageInfo.if_collect">已收藏</span></div>
          </div>
          <image_comment/>
        </div>
        <div class="right" ref="right">
          <div class="user-info">
            <i class="user-icon" :title="'进入'+userInfo.username+'的主页'" :style="{'background-image':'url(' + userInfo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }"  @click="getInOtherUser(userInfo.id)"></i>
            <div class="user-name">{{userInfo.username}}</div>
            <div  @click="setFollow(userInfo.id)">
              <div class="unFollow follow" v-if="!imageInfo.if_follow" title="关注">+关注</div>
              <div class="followed follow" v-if="imageInfo.if_follow" title="取消关注">已关注</div>
            </div>
          </div>
          <div class="data1">
            <div class="works-name-wrap">
              <div class="works-name">{{imageInfo.name}}</div>
              <div class="add-time">{{imageInfo.add_time}}</div></div>
            <div class="works-cate">{{imageInfo.cates}}</div>
          <div class="data1-">
            <img class="data1--" src="../assets/_download.png"><span>{{imageInfo.download_nums}}</span>
            <img src="../assets/_like.png"><span>{{imageInfo.like_nums}}</span>
            <img src="../assets/_collect.png"><span>{{imageInfo.collection_nums}}</span>
          </div>
          </div>
        <div class="data2">
          <div class="image-type-wrap"><img :src="cateImage" class="image-type-img"></div>
          <div class="ul-warp">
          <ul class="data2-">
            <li>格式</li>
            <li>尺寸</li>
            <li>体积</li>
            <li>版权</li>
          </ul>
          <ul class="data2-">
            <li>{{imageInfo.pattern}}</li>
            <li>{{imageInfo.width}}*{{imageInfo.height}}</li>
            <li>{{imageInfo.size}}</li>
            <li>@{{userInfo.username}}</li>
          </ul>
          </div>
          <div class="download-warp">
          <a :href="imageInfo.image" :download="imageInfo.name" class="download-a"><img src="../assets/white_download.svg"  @click="setDownload(imageInfo.id)"><span>下载</span></a>
          </div>
        </div>
          <div class="image-desc">
            <div>图片简介</div>
            <div>{{imageInfo.desc}}</div>
        </div>
        </div>
      </div>
      <tslg_footer/>
    </div>
</template>

<script>
  import {setFollow, setUnFollow, setLike, setUnLike, download} from "../api/action";
  import image_comment from '../components/image_comment'
  import tslg_head from './body/tslg_header'
  import tslg_footer from '../components/body/tslg_footer'
  import {getInOtherUser} from "../utils/user";
  import cookie from "../utils/cookie";
    export default {
        name: "lgts_image_info",
      components:{
          tslg_head,
        tslg_footer,
        image_comment
      },
      data(){
          return{
            like:require('../assets/image_unlike.png'),
            liked:require('../assets/9b_like.png'),
            collected:require('../assets/9b_collect.png'),
            collect:require('../assets/image_unCollect.png'),
            user_id:''
          }
      },
      created(){
        this.$store.commit('SET_AT_IMAGEINFO',true)
        console.log(this.$store.state.user.userInfo.id)
        this.$store.commit('SET_COMMENT_NEXT_PAGE',`image=${this.$store.state.imageGroup.image_id}&page=1`)
      },
      mounted(){
      },
      destroyed(){
        this.$store.commit('SET_AT_IMAGEINFO',false)
      },
      computed:{
        imageInfo(){
          return this.$store.state.imageGroup.imageInfo
        },
        userInfo(){
          return this.$store.state.imageGroup.image_userInfo
        },
        cateImage(){
          switch(this.imageInfo.pattern){
            case 'psd':
              return require('../assets/PS.png')
            case 'jpg':
              return require('../assets/JPG.png')
            case 'jpeg':
              return require('../assets/JPG.png')
            case 'png':
              return require('../assets/PNG.png')
          }
        },
      },
      methods:{
        setLike(id){
          let data=new FormData();
          data.append('image',id)
          data.append('user',this.$store.state.user.userInfo.id)
          if(!this.imageInfo.if_like){
            setLike(data).then((res)=>{
              this.imageInfo.if_like=res.data.id
            }).catch((error)=>{
              console.log(error)
            })
          }else{
            setUnLike(this.imageInfo.if_like).then(()=>{
              this.imageInfo.if_like=false
            }).catch((error)=>{
              console.log(error)
            })
          }
        },
        setCollect(id){
            this.$store.commit('SET_COLLECT_LIST',id);
            this.$store.commit('SET_COLLECT_SHOW');
            document.body.style.overflow='hidden';
        },
        setFollow(id){
          let data=new FormData();
          data.append('follow',id)
          data.append('fan',this.$store.state.user.userInfo.id)
          if(!this.imageInfo.if_follow){
            setFollow(data).then((res)=>{
              this.imageInfo.if_follow=res.data.id
              // this.$store.state.imageGroup.image.forEach((item)=>{
              //   if(item.user.id===id)
              //     item.if_follow=true
              // })
            })
          }else{
            setUnFollow(this.imageInfo.if_follow).then(()=>{
              this.imageInfo.if_follow=false
              // this.$store.state.imageGroup.image.forEach((item)=>{
              //   if(item.user.id===id)
              //     item.if_follow=false
              // })
            })
          }
        },
        getInOtherUser(id){
          getInOtherUser(id)
        },
        setDownload(id) {
          this.$store.commit('SET_IMAGE_ID',id);
          this.$store.commit('SET_IMAGE_INFO');
          let data=new FormData
          data.append('image',id)
          download(data).then((res)=>{})
        },
      },
    }
</script>

<style scoped>
  .image-info{
    background: #f7fafb;
  }
  .warp{
    margin: 3.75rem 15.25rem 5rem;
    background: #fff;
    width: 90.5rem;
  }
  .left{
    width:61.75rem;
    display: inline-block;
    float: left;
    background: #fff;
  }
  .right{
    display: inline-block;
    padding: 0 1.5rem;
    width: 27.75rem;
    float: left;
  }
  .left .image{
    width: 100%;
    display: block;
  }
  .bot-btn{
    padding: 2.25rem 0;
    border-right: 0.0625rem solid #e9e9e9;
    border-bottom:0.0625rem solid #e9e9e9;
    display: flex;
    justify-content: center;
  }
  .bot-btn div{
    width:7.5rem;
    height:3rem;
    background:#9ad3e2;
    border-radius:3rem;
    color:#fff;
    font-size:1.1rem;
    font-weight:600;
    display:flex;
    justify-content:center;
    align-items:center;
    cursor:pointer;
    margin-right: 1rem;
  }
  .bot-btn div:hover{
    background:#2cbec6;
  }
  .bot-btn div img{
    width:2rem;
  }
  .bot-btn div span{
    line-height:3rem;
  }
  .active_btn{
    background:#e4f2f5 !important;
    border:#9b9b9b 0.0625rem solid!important;
    color:#9b9b9b!important;
  }
  .data1{
    border-bottom: 0.0625rem solid #e9e9e9;
  }
  .user-info{
    border-bottom: 0.0625rem solid #e9e9e9;
    display: flex;
    align-items: center;
    flex-direction: column;
    height: 17rem;
  }
  .user-icon{
    margin-top: 3rem;
    width: 6rem;
    height: 6rem;
    cursor: pointer;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
  }
  .user-name{
    font-size:1.1rem;
    margin-top: 0.8rem;
    margin-bottom: 1.5rem;
  }
  .data1{
    text-align: left;
  }
  .works-name-wrap{
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.5rem;
  }
  .works-name{
    font-size: 1.5rem;
  }
  .add-time{
    color: #9c9c9c;
    font-size: 1rem;
    line-height: 2rem;
  }
  .works-cate{
   font-size: 1.1rem;
   margin-bottom: 1.5rem;
 }
  .data1-{
    display: flex;
    align-items: center;
    height: 1.5rem;
    font-size: 1.3rem;
    margin-bottom: 2rem;
  }
  .data1- img{
    width:1.5rem;
    height: 1.5rem;
  }
  .data1- span{
    margin-left: 0.3rem;
   margin-right: 0.6rem;
  }
  .data2{
    margin-bottom:2rem ;
    border-bottom: 1px solid #e9e9e9;
  }
  .image-type-wrap{
    display: flex;
    justify-content: center;
    margin-top: 3rem;
    margin-bottom:1.875rem ;
  }
  .image-type-img{
    width: 4.5rem;
    height: 4.5rem;
  }
  .ul-warp{
    display: flex;
    justify-content: space-around;
    padding:0 6rem;
  }
  .data2-{
    text-align: left;
    line-height: 1.4rem;
  }
  .download-warp{
    margin-bottom: 3rem;
    margin-top: 2rem;
    padding:0 1.5rem;
  }
  .download-a{
    display: flex;
    height: 3rem;
    width: 21.75rem;
    background: #9ad3e2;
    border-radius: 3rem;
    font-size: 1.1rem;
    color: #fff;
    justify-content: center;
    align-items: center;
    font-weight: 600;
  }
  .download-a img{
    height: 1.4rem;
    margin-right: 0.3rem;
  }
  .download-a:hover{
    background: #2cbec6;
  }
  .-btn{
    height: 3rem;
  }
  .share img{
    width: 14.5%;
  }
  .share-{
    margin: 0 20%;
  }
  .image-desc{
    margin-bottom: 2rem;
  }
  .image-desc div:nth-child(1){
    text-align: left;
    font-size: 1.2rem;
    margin-bottom: 0.7rem;
    font-weight: 600;
  }
  .image-desc div:nth-child(2){
    width: 100%;
    font-size: 1.1rem;
    line-height: 1.5rem;
    letter-spacing: 0.1rem;
    word-wrap: break-word;
    text-align: left;
  }
</style>
