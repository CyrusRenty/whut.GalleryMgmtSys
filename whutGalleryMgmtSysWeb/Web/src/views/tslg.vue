<template>
    <div class="tslg">
      <router-view/>
      <collect/>
    </div>
</template>

<script>
  import collect from '../components/card/collect'
    export default {
        name: "tslg",
      components:{
          collect
      }
    }
</script>

<style scoped>
 .tslg{
   width: 100%;
   height: 100%;
 }
</style>
