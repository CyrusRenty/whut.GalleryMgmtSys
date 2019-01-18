<template>
  <div class="sign-nav-btn sc-btn">
    <input type="button" :value="sign" class="submit contract" @click="showSign">
    <input type="button" :value="identify" class="cancel" @click="showIdentify">
    <person_identify ref="person_identify"/>
  </div>
</template>

<script>
  import person_identify from './person_identify'
    export default {
        name: "sign-nav",
      components:{
        person_identify
      },
      methods:{
        showSign(){
          this.$router.push('sign')
          // this.$store.commit('SET_SHOW_SIGN')
        },
        showIdentify(){
          this.$refs.person_identify.show()
        }
      },
      computed:{
          sign(){
            if(this.$store.state.user.userInfo.if_sign){
              return'已签约'
            }else return '签约'
          },
        identify(){
            if(this.$store.state.user.userInfo.if_cer){
              return '已认证'
            }else return '认证'
        }
      }

    }
</script>

<style scoped>
  .sign-nav-btn{
    margin-bottom: 2rem;
    height: 3rem;
    text-align: center;
    background: #fff;
  }
  .contract{
    margin-right: 1rem;
  }
</style>
