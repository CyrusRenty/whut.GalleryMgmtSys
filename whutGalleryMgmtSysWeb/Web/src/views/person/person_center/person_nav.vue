<template>
  <div class="person-nav">
    <router-link :to="item.router" v-for="(item,index)  in person_nav" :key="index" class="user-choice" >{{item.text}}</router-link>
    </div>
</template>

<script>
    export default {
        name: "person_nav",
        data:function () {
          return {
            person_nav:[
              {text:"我的作品",router:'upload'},
              {text:"我的收藏",router:'collection'},
              {text:"我的关注",router:'follow'}],
          }
        },
    }
</script>

<style scoped>
  .person-nav{
    height: 5rem;
    width: 100%;
    background: #fff;
    padding:1rem 0;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .user-choice{
    width: 10rem;
    height: 100%;
    background: #fff;
    color: #4a4a4a;
    cursor:pointer;
    font-size: 1.5rem;
    line-height: 3rem;
  }
  .user-choice:hover{
    color:#ffd100;
  }
  .router-link-active{
    color:#e8be00;
  }
</style>
