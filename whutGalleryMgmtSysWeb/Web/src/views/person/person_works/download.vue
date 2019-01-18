<template>
  <div class="my-download clear">
      <div v-for="item in download_list" class="d-item">
        <div class="image-content" :style="{'background-image':`url(http://111.231.230.54${item.image.image})`}">
          <div class="image-up" @click="showImageInfo(item.image.id)">
            <a class="down-a"><img src="../../../assets/download.svg"><span>下载</span></a>
          </div>
        </div>
        <div class="bottom"><div class="image-name">{{item.image.name}}</div><div class="time">{{item.add_time}}</div></div>
      </div>
    <page_choice :page_nums="page_nums" @cur_page="Page" class="page"/>
  </div>
</template>

<script>
    import {getDownloadHistory} from "../../../api/get";
    import page_choice from '../../../components/page_choice'
    import {setImageInfo} from "../../../utils/user";
    export default {
        name: "download",
      components:{
          page_choice
      },
      data(){
        return {
          download_list:[],
          page_nums:0
        }
      },
      created() {
        getDownloadHistory('page=1&num=12').then((res)=>{
          this.download_list=res.data.results
          this.page_nums=Math.ceil(res.data.count/12)
        })
      },
      methods:{
        Page(page){
          getDownloadHistory(`page=${page}&num=12`).then((res)=>{
            this.download_list=res.data.results
          })
        },
        showImageInfo(id){
          setImageInfo(id)
        }
      }
    }
</script>

<style lang="scss" scoped>
  .my-download{
    float: left;
    height: 65.875rem;
    width: 85rem;
    padding: 0 1rem;
    background: #fff;
  }
  .d-item{
    height: 17.125rem;
    width: 19rem;
    float: left;
    margin: 1.5rem .875rem 0;
    box-shadow: 0 0 4px #9b9b9b;

  }
  .image-content{
    position: relative;
    width: 100%;
    height: 14.25rem;
    background: no-repeat center;
    -webkit-background-size: cover;
    background-size: cover;
    .image-up{
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,.6);
      opacity: 0;
      cursor: pointer;
      &:hover{
        opacity: 1;
      }
      .down-a{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 11.25rem;
        height: 3rem;
        border-radius:3rem;
        background: #fff;
        img{
          width: 1rem;
        }
      }
    }
  }
  .bottom{
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 2.625rem;
    padding:0 2rem;
  }
  .image-name{
    font-size: 1.125rem;
    font-weight: 600;
  }
  .time{
    color: #9b9b9b;
  }
  .page{
    padding-top: 2.5rem;
    width: 100%;
  }
</style>
