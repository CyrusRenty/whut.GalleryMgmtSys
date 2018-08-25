<template>
    <div class="collect" v-if="show_collect">
     <div class="content-warp">
       <div class="content">
        <div class="head"><span class="head-title">添加到收藏夹</span><span class="head-delete" @click="closeCollect">×</span></div>
         <div class="collect-list-warp">
           <ul class="collect-list">
             <li v-for="(item,index) in collect_list" class="list-item" :class="{collected:item.if_collect}">
               <div class="list-left"><span class="item-name">{{item.name}}</span><span class="item-num">{{item.nums}}个作品</span></div>
               <div class="list-right"><img :src="item.if_collect?delete_image:add_image" @click="action(item.if_collect,index,item.id)"></div>
             </li>
           </ul>
         </div>
         <div class="content-bottom"><div class="add-new" @click="showAdd">新建收藏夹</div></div>
       </div>
     </div>
      <create_folder_card ref="show_create_folder"/>
    </div>
</template>

<script>
  import {addImage,deleteImage} from "../../api/user";
  import create_folder_card from '../../components/card/create_folder'
  import cookie from "../../utils/cookie";

  export default {
        name: "collect",
    components:{
      create_folder_card
    },
      data(){
          return {
            show_add:false,
            add_image:require('../../assets/plus-circle.svg'),
            delete_image:require('../../assets/delete_image.png'),
          }
      },
    computed:{
      collect_list(){
        return this.$store.state.user.collect_list
      },
      image_id(){
        return this.$store.state.imageGroup.image_id
      },
      show_collect(){
        return this.$store.state.user.show_collect
      }
    },
      methods:{
        showAdd(){
          this.$refs.show_create_folder.changeShow()
        },
        closeCollect(){
          this.$store.commit('SET_COLLECT_SHOW')
          // if(this.$router.currentRoute.name!=='image'){
          //   var signal = false
          //   this.collect_list.forEach((item)=>{
          //     if(item.if_collect !== false){
          //       this.$store.state.imageGroup.imageInfo.if_collect=true
          //       this.$store.state.imageGroup.image[this.$store.state.imageGroup.index].if_collect=true
          //       signal = true
          //       return
          //     }
          //   })
          //   if (!signal) {
          //     this.$store.state.imageGroup.imageInfo.if_collect = false
          //     this.$store.state.imageGroup.image[this.$store.state.imageGroup.index].if_collect = false
          //   }
          // }

          document.body.style.overflow = 'auto';
        },
        //添加/删除图片 刷新收藏夹
        action(status,index,collect_id){
          let data=new FormData();
          data.append('image',this.image_id);
          data.append('folder',collect_id);
          data.append('user',cookie.getCookie('user_id'))
          if(status){
            deleteImage(this.collect_list[index].if_collect).then(()=>{
              this.$store.commit('SET_COLLECT_LIST',this.image_id)
              if(this.$router.currentRoute.name!=='image') {
                this.$store.state.imageGroup.image[this.$store.state.imageGroup.index].collection_nums--
                this.$store.state.imageGroup.image[this.$store.state.imageGroup.index].if_collect=false
              }else{
                this.$store.state.imageGroup.imageInfo.collection_nums--
                this.$store.state.imageGroup.imageInfo.if_collect = false
              }
            }).catch((error)=>{
              console.log(error)
            })
          }else{
            addImage(data).then((res)=>{
              this.collect_list[index].if_collect=res.data.id
              this.$store.commit('SET_COLLECT_LIST',this.image_id)
              if(this.$router.currentRoute.name!=='image'){
                this.$store.state.imageGroup.image[this.$store.state.imageGroup.index].collection_nums++
                this.$store.state.imageGroup.image[this.$store.state.imageGroup.index].if_collect=res.data.id
              }else{
                this.$store.state.imageGroup.imageInfo.collection_nums++
                this.$store.state.imageGroup.imageInfo.if_collect=res.data.id
              }
            }).catch((error)=>{
              console.log(error)
            })
          }
        },
      },
    }
</script>

<style scoped>
.collect{
  position: fixed;
  top: 0;
  left: 0;
  z-index: 101;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.6);
}
  .content-warp{
    display: flex;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
  }
  .content{
    position: relative;
    display: flex;
    flex-direction: column;
    width: 29.25rem;
    height: 37.5rem;
    background: #fff;
    padding:2.8rem 3rem 2.25rem;
  }
  .head{
    display: flex;
    align-items: center;
    flex-direction: row;
    justify-content: space-between;
  }
  .head-title{
    flex-direction: row;
    justify-content: space-between;
    font-size: 1.125rem;
    white-space: nowrap;
    font-weight: 600;
  }
  .head-delete{
    font-size: 2rem;
    cursor: pointer;
    color:#b3b3b3;
  }
  .collect-list-warp{
    height: 28.1rem;
    overflow: auto;
  }
  .collect-list-warp::-webkit-scrollbar{
    width: .5rem;
  }
  .collect-list-warp::-webkit-scrollbar-button{
    display: none;
  }
  .collect-list-warp::-webkit-scrollbar-thumb{
    background: #d9d9dd;
    border-radius: 0.7rem;
  }
  .collect-list{
    display: flex;
    align-items: center;
    flex-direction: column;

  }
  .list-item{
    -webkit-border-radius: 0.25rem;
    -moz-border-radius: 0.25rem;
    border-radius:0.25rem;
    display: flex;
    justify-content: space-between;
    width: 23.5rem;
    height: 5rem;
    margin-bottom: 0.625rem;
    background: #F0F1F2;
    background-size: cover;
  }
  .collected{
    background: #9AD3E2;
  }
  .list-left{
    display: flex;
    flex-direction: column;
    padding-left: 1.25rem;
    overflow: hidden;
    padding-top: .5rem;
  }
  .item-num{
    display:flex;
    justify-content: flex-start;
    padding-top: 0.625rem;
  }
  .item-name{
    display: flex;
    justify-content: flex-start;
    font-size:1.5625rem;
  }
  .list-right{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 5rem;
  }
  .list-right img{
    cursor: pointer;
    width: 2.5rem;
    height: 2.5rem;
  }
  .content-bottom{
    display: flex;
    justify-content: center;

  }
  .add-new{
    height: 2.5rem;
    width: 9.375rem;
    background: #9AD3E2;
    color: #fff;
    line-height:2.5rem ;
    border-radius: 1.5625rem;
    cursor: pointer;
    font-weight: 600;
    font-size: 1.1rem;
  }
  .add-new:hover{
    background: #2cbec6;
  }

</style>
