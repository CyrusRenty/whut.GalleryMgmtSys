<template>
    <div class="person-collection clear width">
      <div class="total-num">共{{collect_list.length}}个收藏夹</div>
      <add_folder_card/>
      <div class="image-item " v-for="(collect_item,index) in collect_list">
        <div class="item-content bg-pic">
          <div class="collection-pic-wrap">
            <img :src="image_item.url" v-for="image_item in collect_item.image" class="collection-pic-item"/>
          </div>
          <div class="info"></div>
          <img src="../../../assets/Delete_folder.png" class="delete_folder_icon" title="删除收藏夹" @click="deleteFolder(collect_item.id,index)">
          <div class="download" @click="showFolderContent(collect_item.id)">
            查看详情
          </div>
        </div>
        <div class="folder-info">
          <div class="works">
              <div class="folder-name">{{collect_item.name}}</div>
              <div class="collection-list-nums">
                <img src="../../../assets/collection-pic-nums.png" class="folder-item-nums"/>
                <span class="r1rem gray-span">{{collect_item.nums}}</span>
              </div>
            </div>
          <div class="about-worker">
            <div class=" cardTx">
              <span class="update-time">上次更新于{{collect_item.update_time}}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="collect_list.length===0">
        <img src="../../../assets/noResult.png" class="no-result-img">
        <p class="no-result-word">你还没有收藏夹，新建一个吧</p>
      </div>
      <confirm ref="set_comfirm" :title="confirm"/>
    </div>
</template>

<script>
  import mock from '../../../utils/mock'
  import add_folder_card from '../../../components/card/add_folder_card'
  import confirm from '../../../components/confirm_box'
  import {deleteFolder} from "../../../api/action";
    export default {
        name: "collection",
      components:{add_folder_card,confirm},
      data(){
          return {
            confirm:{title:'确定删除此收藏夹'}
          }
      },
      computed:{
        collect_list(){
          return this.$store.state.user.collect_his
        }
      },
      created(){
          if(!this.$store.state.user.collect_his.length)
        this.$store.dispatch('SetCollection').then(()=>{}
      )
      },
      methods:{
        showFolderContent(id){
          this.$store.commit('SET_SHOW_FOLDER_CONTENT')
          this.$store.dispatch('SetFolderImages',id)
          this.$router.push('/tslg/person/folder_content')
        },
        deleteFolder(id,index){
          this.confirm.id=id
          this.confirm.index=index
          this.$refs.set_comfirm.showConfirm()
        },
    }
  }
</script>

<style scoped>

.person-collection{
  margin: 0 auto;
}
.total-num{
  width: 100%;
  text-align: left;
  height: 3rem;
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  margin-left: 1.5rem;
}
.item-wrap{
  float: left;
}
.item {
  width:24.4rem;
  height: 32.3rem;
  margin: 0 1.5rem 3rem 1.5rem;
  display: flex;
  flex-direction: column;
}

.item-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 18.54rem;
  font-size: 1.25rem;
  color: #686868;
  overflow: hidden;
  position: relative;
}

.collection-pic-wrap{
  width: 100%;
  height: 100%;
  position: absolute;
  top:0;
  left: 0;
}

.collection-pic-item{
  width: 50%;
  height: 50%;
  float: left;
}

.bg-pic {
  width: 100%;
  height: 18.54rem;
  background:  #cecece no-repeat center;
  background-size: cover;
}

.item-content img {
  background-size: cover;
  background-position: center;
  overflow: hidden;
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

.download {
  opacity: 0;
  width: 12rem;
  height: 3rem;
  font-size: 1.4rem;
  line-height: 3rem;
  background: #fff;
  border-radius: 3rem;
  position: relative;
  z-index: 1;
  cursor: pointer;
}

.info-text {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 0 1rem ;
  background-color: white;
}

.item-content:hover .info {
  opacity: 1;
}

.item-content:hover .download{
 opacity: 1;
}

.item-content:hover .delete_folder_icon{
 opacity: 1;
}

.collection-list-nums{
  display: flex;
  align-items: center;
}
.folder-item-nums{
  width: 1.4rem;
  height: 1.2rem;
}
.r1rem {
  font-size: 1.3rem;
  margin-left: 0.25rem;
}

.gray-span{
  color: #9b9b9b;
}


.author {
  display: flex;
  flex-direction: column;
  text-align: left;
  height: 8.76rem;
  border-bottom: 0.125rem solid #f5f5f5;
}
.about-worker{
  width: 100%;
  height: 5rem;
  display: flex;
  align-items: center;
}
.update-time{
  color:#9b9b9b;
  font-size: 1.2rem;
}


</style>
