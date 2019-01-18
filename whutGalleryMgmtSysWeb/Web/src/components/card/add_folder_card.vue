<template>
  <div class="create-card width" >
    <div class="create-wrap">
      <i @click="showCreateFolder"></i>
      <span class="suggest-text" @click="showCreateFolder">新建收藏夹</span>
    </div>
    <create_folder_card ref="show_create_folder"/>
  </div>
</template>

<script>
  import create_folder_card from '../../components/card/create_folder'
    export default {
        name: "add_folder_card",
      data(){
          return {
            show_add:false
          }
      },
      components:{
        create_folder_card
      },
      methods:{
        showCreateFolder(){
          this.$refs.show_create_folder.changeShow()
          document.body.style.overflow='hidden'
        },
      }
    }
</script>

<style scoped>
  .create-card{
    float: left;
    width: 24.4rem;
    height: 32.3rem;
    margin: 0 1.5rem 3rem 1.5rem;
    background: #fff;
  }
  i{
    background: url(../../assets/big_icon/add.png);
    background-size: 100% 100%;
    height: 4.7rem;
    width: 4.7rem;
    cursor: pointer;
  }
  .suggest-text{
    font-size: 1.5rem;
    margin-top: 1rem;
  }
  .create-wrap{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    flex-direction: column;
  }

</style>
