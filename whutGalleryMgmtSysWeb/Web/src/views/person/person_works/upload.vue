<template>
    <div class="my-upload">
      <div class="top-nav">
        <div class="nav-item" v-for="(item,index) in nav_items" :class="{on:index===cur_index}" @click="changeStatus(index)">
          <span>{{item.title}}</span><span>({{item.count}})</span>
        </div>
      </div>
      <div class="declare" v-if="cur_index===0">请与上传之日起7天内完善图片信息并提交审核，否则素材将被删除</div>
      <div class="content-list">
        <div class="list-item" v-for="(item,index1) in list">
          <div class="left">
            <div class="image-bg" :style="{'background-image':`url(http://118.24.96.186${item.image})`}"></div>
            <div class="image-da">
              <div class="image-name">{{item.name}}</div>
              <div class="image-size">大小：{{setSize(item.size)}}</div>
              <div class="image-time">上传时间：{{item.add_time}}</div>
            </div>
          </div>
          <div class="right">
            <div class="btn del" @click="deleteItem(item,index1)">删除</div>
            <div class="btn edit" v-if="cur_index===0" @click="edit(item)">编辑</div>
          </div>
        </div>
      </div>
      <page_choice @cur_page="Page" :page_nums="page_nums"/>
    </div>
</template>

<script>
  import {getWorkNums, getWorkStatus} from "../../../api/get";
    import cookie from "../../../utils/cookie";
    import page_choice from '../../../components/page_choice'
    import {changeHis} from "../../../api/action";
    export default {
        name: "upload",
      components:{
          page_choice
      },
      data(){
          return{
            nav_items:[{title:'草稿箱',count:0},{title:'待审核',count:0},{title:'未通过',count:0},{title:'已通过',count:0}],
            list:[],
            nIndex:0,
            u_id:-1,
            page_nums:0,
            cur_index:0
          }
      },
      created(){
         this.u_id=cookie.getCookie('user_id');
        getWorkStatus(`user=${this.u_id}&if_active=4`).then((res)=>{
          this.list=res.data.results;
          this.nav_items[0].count=res.data.count;
          this.page_nums=Math.ceil(res.data.count/6)
        });
        getWorkNums().then((res)=>{
          this.nav_items[0].count=res.data.未上传;
          this.nav_items[1].count=res.data.等待审核;
          this.nav_items[2].count=res.data.未通过;
          this.nav_items[3].count=res.data.已通过
        })
      },
      methods:{
        changeStatus(index){
          this.cur_index=index;
          let nIndex;
          switch(index){
            case 0:{
              nIndex=4;
              break
            }
            case 1:{
              nIndex=2;
              break
            }
            case 2:{
              nIndex=3;
              break
            }
            case 3:{
              nIndex=1;
              break
            }
          }
          this.list=[];
          getWorkStatus(`user=${this.u_id}&if_active=${nIndex}&num=6`).then((res)=>{
            this.list=res.data.results
            this.nIndex=nIndex
            this.page_nums=Math.ceil(res.data.count/6)
          })
        },
        setSize(num){
          let size=num/1024;
          if(size>1024){
            size=size/1024;
            size=size.toFixed(2);
            size=size+'M'
          }else{
            size=size.toFixed(2);
            size=size+'K'
          }
          return size
        },
        deleteItem(item,index){
          let data=new FormData
          data.append('if_show','false')
          // data.append('user',this.$store.state.user.userInfo.id)
          changeHis(item.id,data).then((res)=>{
            console.log(res)
            if(res.data){
              this.list.splice(index,1)
              this.nav_items[index].count--
            }
          }).catch((error)=>{
            console.log(error)
          })
        },
        Page(page){
          getWorkStatus(`user=${this.u_id}&if_active=${this.nIndex}&page=${page}&num=6`).then((res)=>{
            this.list=res.data.results
          })
        },
        edit(item){
          console.log(item)
          let new_item=new Object();
          new_item.desc=item.desc;
          new_item.cates=item.cates;
          new_item.key_word_list=item.keywords.split(" ")||[];
          new_item.id=item.id;
          new_item.pre_file={};
          new_item.edit_status=true;
          new_item.name=item.name;
          new_item.pre_file.src='http://118.24.96.186'+item.image;
          this.$store.commit('SET_EDIT_ITEM',new_item);
          this.$router.push('/tslg/doUpload')
        }
      }

    }
</script>

<style lang="scss" scoped>
  @import "../../../styles/variables";
  .my-upload{
    float: left;
    width: 85rem;
    background: #fff;
  }
  .top-nav{
    height: 4rem;
    text-align: left;
    border-bottom: 0.0625rem solid #e9e9e9;
    font-size:$ms;
    line-height: 4rem;
  }
  .nav-item{
    display:inline-block;
    margin: 0 1.5rem;
    cursor: pointer;
    &:hover{
      color: $normal;
    }
  }
  .on{
    color: $normal;
  }
  .declare{
    font-size: $xsx;
    color:red;
    text-align: left;
    margin:1.125rem 0 0 1.5rem;
  }
  .content-list{
    padding: 0 1.5rem;
    margin-bottom: 2.5rem;
    min-height:40rem;
  }
  .list-item{
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 10.5rem;
    width: 100%;
    padding: 1.5rem 0;
    border-bottom: 0.0625rem solid #e9e9e9;
  }
  .left{
    height: 100%;
    display: flex;
    justify-content: flex-start;
    .image-bg{
      width: 10rem;
      height: 100%;
      margin-right: 3rem;
      background: center no-repeat;
      -webkit-background-size: cover;
      background-size: cover;
    }
    .image-da{
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: left;

      .image-name{
        font-size: 1.25rem;
        font-weight: 600;
      }
      .image-size{
        margin-top: 1.5rem;
        color: $f-light;
      }
      .image-time{
        margin-top: .25rem;
        color: $f-light;
      }
    }
  }
  .right{
    .btn{
      width: 7.5rem;
      height:2.5rem;
      -webkit-border-radius: 2.5rem;
      -moz-border-radius: 2.5rem;
      border-radius: 2.5rem;
      line-height: 2.5rem;
      font-weight: 600;
      font-size: 1.2rem;
      cursor: pointer;
    }
    .del{
      border: $normal solid 0.0625rem;
      color: $normal;
    }
    .edit{
      margin-top: .75rem;
      background: $normal;
      color: $f-deep;
    }
  }
</style>
