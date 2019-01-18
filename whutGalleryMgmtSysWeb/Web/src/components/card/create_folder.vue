<template>
  <div class="add-collect" v-if="show_add" :class="{bg:$router.currentRoute.name==='person_collection'}">
    <div class="content-warp">
      <div class="content">
        <div class="head"><span class="head-title">新建收藏夹</span><span class="head-delete" @click="cancel">×</span></div>
        <div class="input-wrap">
          <input type="text" v-focus v-model="folder_name" maxlength="10" placeholder="收藏夹名称(不超过10个字)" class="input-name" ref="folder_name"/>
          <div class="hint">{{hint_folder_name}}</div>
        </div>
        <div class="add-bottom">
          <div class="confirm" @click="confirm">确定</div>
          <div class="cancel" @click="cancel">返回</div>
          <div class="hint">{{hint_result}}</div>
        </div>
      </div>
    </div>
    <hint :title="hint_title" :duration="1000" ref="hint"/>
  </div>
</template>

<script>
    import {newFolder} from "../../api/user";
    import hint from '../../components/hint'
    export default {
        name: "create_folder",
      components:{
        hint
      },
      data(){
          return {
            folder_name:'',
            hint_result:'',
            hint_folder_name:'',
            hint_title:'',
            show_add:false,
          }
      },
      created(){
        this.$store.dispatch('SetFolderList')
      },
      methods:{
        changeShow(){
          this.show_add=!this.show_add
          document.documentElement.style.overflow='hidden'
        },
        cancel(){
          this.changeShow()
          this.folder_name=''
          if(this.$router.currentRoute.name==='person_collection')
          document.documentElement.style.overflow='auto'
        },
        confirm(){
            if(this.folder_name.length<3){
              this.$refs.hint.showHint('收藏夹名称3-10个字');
            }else if(this.checkFolderExist()){
              return
            }else{
              let data =new FormData
              data.append('name',this.folder_name);
              newFolder(data).then((res)=>{
                if(res.data.id){
                  this.$refs.hint.showHint('添加成功');
                  if(this.$router.currentRoute.name==='person_collection')
                  this.$store.dispatch('SetCollection')
                  this.$emit('reload')
                  this.changeShow()
                }
                else this.$refs.hint.showHint('添加失败');
              }).catch(()=>{
                this.$refs.hint.showHint('添加失败');
                })
            }
        },
        checkFolderExist(){
          let exist=this.$store.state.user.folder_list.find((item)=>{
            if(item.name===this.folder_name)
              return true
          });
          if(exist){
            this.$refs.hint.showHint('该收藏夹已存在');
            return true
          }else return false

        }
      },
      directives:{
        focus:{
          inserted:function (el) {
            el.focus()
          }
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .bg{
    background: rgba(0,0,0,0.6);
  }
  .add-collect{
    position: fixed;
    top: 0;
    left: 0;
    z-index: 102;
    width: 100%;
    height: 100%;
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
    height: 38rem;
    background: #fff;
  }
  .head{
    display: flex;
    align-items: center;
    flex-direction: row;
    justify-content: space-between;
    padding:0.625rem 2rem;
  }
  .head-title{
    flex-direction: row;
    justify-content: space-between;
    width: 7.5rem;
    font-size: 1.5rem;
  }
  .head-delete{
    font-size: 3rem;
    cursor: pointer;
    color:#b3b3b3;
  }
  .input-wrap{
    padding: 0 2.5rem;
  }
  .input-name{
    height: 3rem;
    border: 0.0625rem solid #e3e3e3;
    text-indent:0.625rem ;
    font-size: 1.1rem;
    width: 100%;
  }
  .add-bottom{
    position: absolute;
    bottom: 2.5rem;
    width: 100%;
    text-align: center;
    padding: 0 3rem;
  }
  .confirm,.cancel{
    display: inline-block;
    width: 7rem;
    height: 3rem;
    line-height: 3rem;
    border-radius: 3rem;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 600;
    margin:0 0.5rem;
  }
  .confirm{
    background: $normal;
    color: #4a4a4a;
  }
  .confirm:hover{
    background: $hover;
  }
</style>
