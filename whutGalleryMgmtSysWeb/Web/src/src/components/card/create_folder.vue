<template>
  <div class="add-collect" v-if="show_add">
    <div class="content-warp">
      <div class="content">
        <div class="head"><span class="head-title">新建收藏夹</span><span class="head-delete" @click="cancel">×</span></div>
        <div class="input-wrap">
          <input type="text" v-model="folder_name" placeholder="收藏夹名(3-10字)" class="input-name" ref="folder_name" @input="checkFolderName" @blur="checkFolderExist"/>
          <div class="hint">{{hint_folder_name}}</div>
        </div>
        <div class="add-bottom">
          <div class="confirm" @click="confirm">确定</div><div class="cancel" @click="cancel">返回</div>
          <div class="hint">{{hint_result}}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import {newFolder} from "../../api/user";

    export default {
        name: "create_folder",
      data(){
          return {
            folder_name:'',
            folder_desc:'',
            hint_result:'',
            hint_folder_name:'',
            show_add:false,
          }
      },
      created(){
          if(!this.$store.state.user.collect_list){
            this.$store.dispatch('SetCollection')
            if(this.$router.currentRoute.name==='person_collection')
              document.body.style.overflow='hidden'
          }
      },
      mounted(){
          this.$nextTick(()=>{
            // this.$refs['folder_name'].focus()
          })
      },
      methods:{
          changeShow(){
            this.show_add=!this.show_add
          },
          cancel(){
            this.changeShow()
            this.folder_name=''
            this.folder_desc=''
            if(this.$router.currentRoute.name==='person_collection')
            document.body.style.overflow='auto'
          },
        clean_hint(){
          this.hint_result=''
          this.folder_name=''
          this.folder_desc=''
        },
        confirm(){
            if(!this.folder_name){
              this.hint_folder_name='请填写收藏夹名'
              this.$refs.folder_name.style.border='0.0625rem #ff0000 solid'
            }
            else{
              let data =new FormData
              data.append('name',this.folder_name)
              data.append('desc',this.folder_desc)
              newFolder(data).then((res)=>{
                if(res.data.id){
                  this.hint_result='添加成功'
                  this.$store.dispatch('SetCollection')
                }
                else this.hint_result='添加失败'
                setTimeout(this.clean_hint,1800)
                if(this.$router.currentRoute.name!=='person_collection')
                this.$store.commit('SET_COLLECT_LIST',this.$store.state.imageGroup.image_id)
              }).catch(()=>{
                this.hint_result='添加失败'
                setTimeout(this.clean_hint,1800)
                })
            }
        },
        checkFolderName(){
            if(this.folder_name.length>10){
              this.hint_folder_name='收藏夹名称过长'
              this.$refs.folder_name.style.border='#ff0000 0.0625rem solid'
            }else{
              this.hint_folder_name=''
              this.$refs.folder_name.style.border='#9ad3e2 0.0625rem solid'
            }
        },
        checkFolderExist(){
          let exist=this.$store.state.user.collect_list.find((item)=>{
            if(item.name===this.folder_name)
              return true
          })
          if(exist){
            this.hint_folder_name='该收藏夹已存在'
            this.$refs.folder_name.style.border='#ff0000 0.0625rem solid'
          }else{
            this.hint_folder_name=''
            this.$refs.folder_name.style.border='#cecece 0.0625rem solid'
          }
        }
      }
    }
</script>

<style scoped>
  .add-collect{
    position: fixed;
    top: 0;
    left: 0;
    z-index: 102;
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
  .folder-desc{
    width: 100%;
    height: 6rem;
    resize: none;
    text-indent: 0.625rem;
    border: 1px solid #e3e3e3;
    outline: none;
    font-size: 1.1rem;
    padding-top: 0.3rem;
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
    background: #9AD3E2;
    color: #fff;
  }
  .confirm:hover{
    background:#2cbec6;
  }
</style>
