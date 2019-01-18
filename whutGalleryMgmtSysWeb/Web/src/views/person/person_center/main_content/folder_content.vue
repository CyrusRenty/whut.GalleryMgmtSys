<template>
  <div class="folder-content" v-if="photos"  ref="folder_content">
  <div class="folder-title">
    <div class="top-nav"><a @click="backTOCollectList" class="nav-back">返回收藏夹</a><span> - 收藏夹详情</span></div>
    <div class="collection-list-info">
      <div class="collection-list-text">
        <div class="collection-list-name">
          <label for="folder-name"> <img src="../../../../assets/Edit.png" class="icon-edit"/></label>
          <input type="text" v-model="photos.name" id="folder-name"  class="input-folder-name" @blur="sendFolderName"/>
        </div>
        <div class="collection-list-detail">
          <span>内容数量:{{photos.nums}}</span>
          |
          <span>创建时间:{{add_time}}前</span>
          |
          <span>更新时间:{{update_time}}前</span>
        </div>
      </div>
    </div>
  </div>
    <div class="folder-image clear width" >
      <div class="image-item" v-for="(photo,index) in photos.results" :key="index" >
          <div  class="item-content" :style="{'background-image':'url(' + photo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }">
            <div class="info" @click="showImageInfo(photo.id)" title="点击查看详情">
              <img src="../../../../assets/Delete_folder.png" class="delete_folder_icon" title="取消收藏" @click.stop="deleteImage(photo.ship_id,index)">
              <a class="download-warp"  :href="photo.image.split('.400×300')[0]" @click.stop="setDownload(photo.id)" :download="photo.name">下载</a>
            </div>
          </div>
          <div class="photo-info">
            <div class="works">
              <div class=" works-name">{{photo.name}}</div>
              <div class=" works-type">{{photo.cates}}</div>
            </div>
            <div class="bottom-data">
              <div class="img-warp">
                <img src="../../../../assets/_download.png"/><span class="r1rem">{{photo.download_nums}}</span>
                <img src="../../../../assets/_like.png"/><span class="r1rem">{{photo.like_nums}}</span>
                <img src="../../../../assets/_collect.png" /><span class="r1rem">{{photo.collection_nums}}</span>
              </div>
              <span class="time">{{photo.add_time}}</span>
            </div>
          </div>
      </div>
    </div>
    <router-view/>
  </div>
</template>

<script>
  import {changeFolderName} from "../../../../api/action";
  import {deleteImage} from "../../../../api/user";
  import {setDownload, setImageInfo} from "../../../../utils/user";
    export default {
        name: "folder_content",
      created(){
      },
      mounted(){

      },
      computed:{
          photos(){
            return this.$store.state.user.folder_images
          },
          add_time(){
            if(this.photos.add_time){
              return this.setTime(this.photos.add_time)
            }
          },
          update_time(){
            if(this.photos.update_time)
              return this.setTime(this.photos.update_time)
        },
      },
      methods:{
        sendFolderName(){
          let data=new FormData
          data.append('name',this.photos.name)
          changeFolderName(this.photos.id,data)
        },
        backTOCollectList(){
          this.$store.commit('SET_SHOW_FOLDER_CONTENT')
          this.$router.go(-1)
        },
        setTime(Time){
          let _time=Time.split('-')
          let date=new Date()
          let year=date.getFullYear()-parseInt(_time[0])
          let month=date.getMonth()+1-parseInt(_time[1])
          let day=date.getDate()-parseInt(_time[2])
          let time=[]
          if(year)
            time.push(year+'年')
          if(month)
            time.push(month+'个月')
          if(day)
            time.push(day+'天')
          else return '0天'
          return time.join("")
        },
        showImageInfo(id){
         setImageInfo(id)
        },
        deleteImage(id,index){
          deleteImage(id).then(()=>{
            this.photos.results.splice(index,1)
            this.photos.nums--
            this.$store.dispatch('SetCollection').then()
          })
        },
        setDownload(id){
          setDownload(id)
        }
      },
    }
</script>

<style scoped>
  .folder-content{
    background: #f7fafb;
    width: 100%;
  }
  .top-nav{
    margin-bottom: 0.5rem;
    font-size: 1.4rem;
  }
  .top-nav span{
    color: #9b9b9b;
  }
  .folder-title{
    margin:2rem 6rem;
    text-align: left;
    padding-top:1rem;
  }
  .nav-back{
    cursor: pointer;
  }
  .nav-back:hover{
    color: #9ad3e2;
  }

  .collection-list-info{
    background: #fff;
    width: calc( 100%);
    height: 8.625rem;
    padding: 2.0625rem 3rem 2.0625rem 1.5rem;
    display: flex;
    justify-content: space-between;
  }

  .collection-list-text{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }
  .icon-edit{
    position: absolute;
    width: 2rem;
    height: 2rem;
  }

  .collection-list-name img{

  }
  .input-folder-name{
    z-index:2;
    font-size: 1.875rem;
    line-height: 1.875rem;
    padding-left: 2.8rem;
  }
  .collection-list-detail{
    color: #cecece;
  }

  .collection-list-detail span{
    font-size: 1.125rem;
    line-height: 1.125rem;
  }

  .folder-image{
    width: 111rem;
    margin: 0 auto;
    height: auto;
    background: #f7fafb;
  }
  .delete_folder_icon{
    opacity: 0;
    height: 2rem;
    width: 2rem;
    z-index: 1;
    position:absolute;
    top: 1.5rem;
    left: 1.5rem;
  }
  .info:hover .delete_folder_icon{
    opacity: 1;
  }


</style>
