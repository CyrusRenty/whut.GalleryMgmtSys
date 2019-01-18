<template>
  <div class="fan-follow">
    <div class="top">
      <a @click="showFan" :class="show_fan?'active-a-color':''">我的粉丝({{fan.length}})</a>
      <a @click="showFollow" :class="!show_fan?'active-a-color':''">我的关注({{my_follow.length}})</a>
    </div>
    <div v-if="show_fan">
      <person_card :person_list="fan" @newFollow="newFollow"/>
    </div>
    <div v-if="!show_fan">
      <person_card :person_list="my_follow"/>
    </div>
  </div>
</template>
<script>
  import person_card from '../../../../components/card/person_card'
  import {setImageInfo,setDownload} from "../../../../utils/user";
  import {getFans, getMyFollow} from "../../../../api/get";

  export default {
    name: "download",
    components:{person_card},
    data(){
        return {
          sw:true,
          no_result:false,
          fan:[],
          my_follow:[],
          show_fan:true
        }
    },
      computed:{

      },
      created(){

      },
      mounted(){
        this.getFans();
        this.getMyFollow()
      },
      methods:{
        showImageInfo(id){
         setImageInfo(id)
        },
        getFans(){
          getFans().then((res)=>{
            this.fan=res.data
          })
        },
        getMyFollow(){
          getMyFollow().then((res)=>{
              this.my_follow=res.data
            }
          )
        },
        showFan(){
          this.show_fan=true
        },
        showFollow(){
          this.show_fan=false;
        },
        newFollow(status){
          this.getMyFollow()
        }
      },

    }
</script>

<style lang="scss" scoped>
  @import "../../../../styles/variables";
  .fan-follow{
    height: 50rem;
    padding: 5rem 6rem;
    text-align: left;
  }
  .top a{
    font-size: 1.25rem;
    margin-right: 1.5rem;
  }
  .active-a-color{
    color:$normal
  }
</style>
