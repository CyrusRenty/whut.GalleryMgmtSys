<template>
  <div class="comment-warp">
    <div class="comment-top">
      <h3>评论</h3>
      <div class="comment-input">
        <i :style="{'background-image':'url(' + this.$store.state.user.userInfo.image + ')','background-repeat':'no-repeat','background-size':'cover','background-position':'center' }"  ></i>
        <textarea v-model="comment_content" title="评论"></textarea>
      </div>
      <div class="sc-btn"><input type="button" class="submit" @click="sentComment" value="发表评论"></div>
    </div>
    <div class="comment-bottom" ref="comment" v-if="comment_list">
      <div v-for="(item,index) in comment_list" class="comment-item">
          <i class="comment-user-image" :style="{'background-image':`url(${item.user.image})`}"></i>
          <div class="comment-middle">
            <div class="up-context">
              <h3 class="username">{{item.user.username}}</h3>
              <span>{{item.add_time}}</span>
            </div>
            <div class="comment-context">{{item.content}}</div>
            <div class="under-context">
              <div class="comment-icon">
                <div @click="changeShowReply(index)" class="change-show-reply" title="展开所有评论" v-if="item.kids&&show_all_reply===-1">{{item.kids.length}}条回复</div>
                <div @click="changeShowReply(-1)" class="change-show-reply" title="收回评论" v-if="item.kids&&show_all_reply!==-1">{{item.kids.length}}条回复</div>
                <i class="icon1" title="举报评论" @click="badComment(item)"></i>
                <i class="icon2" title="回复评论" @click="showReply(index)"></i>
                <i v-if="item.if_like" class="icon3-" title="取消点赞" @click="setLikeComment(item)"></i>
                <i v-if="!item.if_like" class="icon3" title="点赞" @click="setLikeComment(item)"></i>
                <span :title="`点赞数${item.like}`">{{item.like}}</span>
            </div>
            </div>
            <div class="reply-wrap clear" v-if="show_reply===index">
              <div class="reply-input-wrap">
                <label for="reply-input"> 回复{{item.user.username}}：</label>
                <input id="reply-input" type="text" class="reply-input" v-model="reply_context" />
              </div>
              <div class="sc-reply">
                <input type="button" value="回复" class="submit" @click="replyComment(item,index)"/>
                <input type="button" value="取消" class="cancel" @click="replyCancel"/>
              </div>
            </div>
            <div class="reply-content-wrap" v-if="show_all_reply===index">
              <div v-for="(rpl_item,rIndex) in item.kids" class="reply-item">
                <div class="reply-top">
                  <div class="name-wrap"><span class="rpl-name">{{rpl_item.user.username}}</span><span> 回复 </span><span class="rpl-name">{{rpl_item.reply}}</span></div>
                  <span>{{rpl_item.add_time}}</span>
                </div>
                <div class="reply-context">{{rpl_item.content}}</div>
                <div class="under-context">
                  <span class="comment-icon ">
                    <i class="icon1" title="举报评论" @click="badComment(rpl_item)"></i>
                    <i class="icon2" title="回复评论" @click="showReplyReply(rIndex)"></i>
                    <i v-if="rpl_item.if_like" class="icon3-" title="取消点赞" @click="setLikeComment(rpl_item)"></i>
                    <i v-if="!rpl_item.if_like" class="icon3" title="点赞" @click="setLikeComment(rpl_item)"></i>
                    <span :title="`点赞数${rpl_item.like}`">{{rpl_item.like}}</span>
                  </span>
                </div>
                <div class="reply-wrap clear" v-if="show_reply_reply===rIndex">
                  <div class="reply-input-wrap">
                    <label for="reply-input1"> 回复{{rpl_item.user.username}}：</label>
                    <input id="reply-input1" type="text" class="reply-input" v-model="reply_reply_context" />
                  </div>
                  <div class="sc-reply">
                    <input type="button" value="回复" class="submit" @click="replyReply(rpl_item,index,rIndex)"/>
                    <input type="button" value="取消" class="cancel" @click="replyReplyCancel"/>
                  </div>
                </div>
              </div>
              <div class="show-all-reply" @click="changeShowReply(-1)" v-if="show_all_reply!==-1">收起评论</div>
            </div>
          </div>
      </div>
      <div class="no-result-word" v-if="no_more">没有更多评论了~</div>
    </div>
    <div v-if="!comment_list.length" class="no-result-word">暂无评论，快来发表首评吧！</div>
    <div class="report" v-if="show_report">
      <div class="content-wrap">
        <div>
          <h2>举报<span>(最多选择两项)</span></h2>
        <div class="checkbox-wrap">
          <div v-for="(item,index) in checkbox" class="check-item" @change="setCheck(index)" ref="report_check">
            <input :id="index" type="checkbox" :title="item" />
            <label :for="index">{{item}}</label>
          </div>
            <textarea v-model="report_context" title="举报原因" @focus="focusReportText"></textarea>
          <div class="hint" v-if="hint_reason_input">请填写举报原因</div>
        </div>
        </div>
        <div class="sc-wrap">
          <div class="hint">{{hint_result}}</div>
          <input type="button" value="确定" class="submit" @click="submitReport"/>
          <input type="button" value="返回" class="cancel" @click="deleteReport"/>
        </div>
          </div>
        </div>
      </div>
</template>

<script>
  import {report, setComment} from "../api/user";
  import {likeComment, unLikeComment} from "../api/action";

    export default {
        name: "image_comment",
      data(){
          return {
            comment_content:'',
            checkbox:['发布广告','低俗色情','虚假言论','恶意中伤','其他'],
            report_context:'原因：',
            reason:[],
            hint_reason_input:false,
            hint_result:'',
            report:{},
            show_report:false,
            show_reply:false,
            show_reply_reply:false,
            sw:true,
            no_more:false,
            reply_context:'',
            reply_reply_context:'',
            show_all_reply:-1,
          }
      },
      created(){
      },
      mounted(){
          this.$nextTick(()=>{
            this.$store.dispatch('setCommentList').then(()=>{
                console.log('图片评论获取成功')
              console.log(this.comment_list)
            })
          });
        this.$refs.comment.addEventListener('scroll',this.getComment)
      },
      methods:{
          //发送图片评论
        sentComment(){
            if(this.comment_content){
              let data=new FormData
              data.append('content',this.comment_content)
              data.append('user',this.$store.state.user.userInfo.id)
              //data.append('reply',this.$store.state.user.userInfo.id)
              data.append('image',this.$store.state.imageGroup.image_id)
              data.append('is_add_info','false')
              data.append('floor','0')
              setComment(data).then((res)=>{
                if(res.data){
                  this.comment_content=''
                  let item=res.data
                  item.add_time='刚刚'
                  item.like=0
                  this.comment_list.splice(0,0,item)
                }
              }).catch((res)=>{
                console.log(res)
              })
            }
          },
        //点赞评论
        setLikeComment(item){
          let data=new FormData
          data.append('comment',item.id)
          data.append('user',this.$store.state.user.userInfo.id)
          if(!item.if_like)
          likeComment(data).then((res)=>{
             if(res.data){
              item.if_like=res.data.id
              item.like++
             }
          }).catch((res)=>{
            console.log(res)
          })
          else unLikeComment(item.if_like).then(()=>{
              item.if_like=false
              item.like--
          })
        },
        //确定举报评论相关信息
        badComment(item){
          this.show_report=true
          this.report.content=item.content
          this.report.user=this.$store.state.user.userInfo.id
          this.report.comment=item.id
          document.body.style.overflow='hidden'
        },
        //举报复选框功能实现
        setCheck(index){
          this.hint_result=''
          let node=this.$refs.report_check[index].childNodes
          if(node[0].checked){
            this.reason.push(this.checkbox[index])
            node[2].style.color='#9ad3e2'
          }else{
              node[2].style.color='#4a4a4a'
              let nIndex=this.reason.indexOf(this.checkbox[index])
            this.reason.splice(nIndex,1)
          }
          if(this.reason.length===2){
            for(let i=0;i<5;i++){
              if(!this.$refs.report_check[i].childNodes[0].checked)
                this.$refs.report_check[i].childNodes[0].disabled='disabled'
            }
          }else if(this.reason.length>0){
            for(let i=0;i<5;i++){
              this.$refs.report_check[i].childNodes[0].disabled=false
            }
          }
          console.log(this.reason)
        },
        //发送举报
        submitReport(){
          let rea_length=this.report_context.length
          if(!this.reason.length){
            this.hint_result='请选择举报原因'
            return
          }
          if(this.reason.indexOf('其他')!==-1&&rea_length<=3){
            this.hint_reason_input=true
            return
          }
          if(rea_length>3){
            this.reason.push(this.report_context)
          }
          let reason=this.reason.join(" ")
          let data=new FormData
          data.append('reason',reason)
          data.append('user',this.report.user)
          data.append('comment',this.report.comment)
          data.append('content',this.report.content)
          report(data).then((res)=>{
            if(res.data){
              this.hint_result='举报成功'
              this.report_context='原因：'
            }else{
              this.hint_result='举报失败'
            }
            setTimeout(()=>{
              this.hint_result=''
            },2000)
          }).catch(()=>{
            this.hint_result='举报失败'
            setTimeout(()=>{
              this.hint_result=''
            },2000)
          })
        },
        //举报原因输入框聚焦消失hint
        focusReportText(){
          this.hint_reason_input=false
        },
        //退出举报评论弹窗
        deleteReport(){
          document.body.style.overflow='auto'
          this.report_context=''
          this.show_report=false
        },
        //滚动加载评论
        getComment(){
          //console.log(this.$refs.comment.scrollTop,this.$refs.comment.scrollHeight,this.$refs.comment.clientHeight)
          if(this.sw&&this.$refs.comment.scrollTop+this.$refs.comment.clientHeight>this.$refs.comment.scrollHeight-50){
            this.sw=false
            if(this.$store.state.imageGroup.comment_next_page){
              console.log('get')
              this.$store.dispatch('setCommentList').then(()=>{
                this.sw=true
              })
            }else this.no_more=true
          }
        },
        //展开回复评论的输入框
        showReply(index){
          this.show_reply=index;
          this.reply_context=''
        },
        //回复评论
        replyComment(item,index){
          if(this.reply_context){
            let data=new FormData
            data.append('content',this.reply_context)
            data.append('user',this.$store.state.user.userInfo.id)
            data.append('reply',item.user.id)
            data.append('image',this.$store.state.imageGroup.image_id)
            data.append('is_add_info','true')
            data.append('floor',`${item.floor}`)
            setComment(data).then((res)=>{
              if(res.data){
                let newItem=res.data
                newItem.add_time='刚刚'
                newItem.like=0
                newItem.reply=item.user.username
                if(!this.comment_list[index].kids)
                this.comment_list[index].kids=[]
                this.comment_list[index].kids.splice(0,0,newItem)
                this.replyCancel()
                this.changeShowReply(index)
              }
            }).catch((res)=>{
              console.log(res)
            })
          }
        },
        //收回评论的回复输入框
        replyCancel(){
          this.reply_context=''
          this.show_reply=false
        },
        //展开相应的评论的回复的回复的输入框
        showReplyReply(index){
          this.show_reply_reply=index
          this.reply_reply_context=''
        },
        //收回评论的回复的回复输入框
        replyReplyCancel(){
          this.show_reply_reply=false
          this.reply_reply_context=""
        },
        //回复评论的回复
        replyReply(item,index,rIndex){
          if(this.reply_reply_context){
            let data=new FormData
            data.append('content',this.reply_reply_context)
            data.append('user',this.$store.state.user.userInfo.id)
            data.append('reply',item.user.id)
            data.append('image',this.$store.state.imageGroup.image_id)
            data.append('is_add_info','true')
            data.append('floor',`${item.floor}`)
            setComment(data).then((res)=>{
              if(res.data){
                let newItem=res.data
                newItem.add_time='刚刚'
                newItem.like=0
                newItem.reply=item.user.username
                this.comment_list[index].kids.splice(rIndex+1,0,newItem)
                this.replyReplyCancel()
              }
            }).catch((res)=>{
              console.log(res)
            })
          }
        },
        //展开相应评论的回复
        changeShowReply(index){
          this.show_all_reply=index
        }
      },
      computed:{
          comment_list(){
            return this.$store.state.imageGroup.comment_list
          }
      }
    }
</script>

<style scoped>
  i{
    display: inline-block;
    background:no-repeat center;
    -webkit-background-size: cover;
    background-size: 100% 100%;
  }
  .comment-warp{
    padding: 3rem;
    border-right: 0.0625rem solid #e9e9e9;
  }
  .comment-top{
    display: flex;
    flex-direction: column;
    text-align: left;
    width: 100%;
  }
  .comment-input i{
    width: 3.75rem;
    height: 3.75rem;
    margin-right: 1rem;
    border-radius: 50%;
  }
  .comment-input textarea{
    height: 3.75rem;
    width: 50rem;
    border: 0.0625rem solid #cecece;
    font-size: 1.1rem;
    resize: none;
  }
  .sc-btn{
    border-bottom: 0.0625rem solid #e9e9e9;
  }
  .sc-btn .submit{
    float: right;
    margin-top:0.75rem ;
    width: 6rem;
    height: 2rem;
    font-size: 1rem;
    line-height: 2rem;
    margin-bottom: 2.5rem;
  }
  .comment-bottom{
    min-height: 5rem;
    max-height: 43rem;
    overflow-y: scroll;
  }
  .comment-bottom::-webkit-scrollbar-button{
    display: none;
    -moz-appearance: none;
  }
  .comment-bottom::-webkit-scrollbar{
    width: .5rem;
  }
  .comment-bottom::-webkit-scrollbar-thumb{
    background: #d9d9dd;
    border-radius: 0.7rem;
  }
  .comment-item{
    display: flex;
    padding: 1.5rem 0;
    border-bottom: 0.0625rem solid #e9e9e9;
  }
  .comment-item .top{
    display: flex;
  }
  .comment-user-image{
    width: 3.75rem;
    height: 3.75rem;
    background: no-repeat center;
    background-size:cover;
    border-radius: 50%;
    margin-right: 1rem;;
  }
  .comment-middle{
    text-align: left;
    width: 48rem;
    word-wrap: break-word;
    /*letter-spacing: 0.1rem;*/
  }
  .first-comment{
    margin-bottom: 1.5rem;
  }
  .up-context{
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.875rem;
  }
  .up-context span{
    color: #9e9e9e;
  }
  .username{
    margin: 0;
  }
  .comment-context{
    font-size: 1.1rem;
  }
  .under-context{
    color: #9b9b9b;
    padding: 0.75rem 0;
  }
  .comment-icon{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 1.2rem;
  }
  .comment-icon i{
    width: 1.2rem;
    height:1.2rem;
    cursor: pointer;
    margin-left: 0.5rem;
  }
  .comment-icon span{
    margin-left: 0.3rem;
    margin-top: 0.2rem;
  }
  .change-show-reply{
    cursor: pointer;
    margin-right: 1rem;
  }
  .icon1{
    background-image: url(../assets/report_normal.png);
  }
  .icon1:hover{
    background-image:url(../assets/report_hover.png);
  }
  .icon2{
    background-image: url(../assets/commet_normal.png);
  }
  .icon2:hover{
    background-image: url(../assets/commet_active.png);
  }
  .icon3{
    background-image: url(../assets/like_normal.png);
  }
  .icon3-{
    background-image: url(../assets/like_active.png);
  }

/*
reply
*/
  .reply-wrap{
    margin-top: 1.5rem;
    position: relative;
  }
  .reply-input-wrap label{
    display: block;
    white-space: nowrap;
    padding-left:0.5rem;
    background: #fff;
    height: 100%;
    line-height: 2.5rem;
  }
  .reply-input-wrap{
    display: flex;
    align-items: center;
    height:2.5rem;
    border: 0.0625rem solid #979797;
    font-size: 1rem;
  }
  .reply-input{
    height: 100%;
    width: 100%;
    padding: 0.625rem 0;
    line-height: 2.5rem;
    font-size: 1rem;
  }
  .sc-reply{
    margin-top: 0.75rem;
  }
  .sc-reply input{
    width: 6rem;
    height:2rem;
    font-size: 1.2rem;
    border-radius: 2rem;
    font-weight: 600;
    line-height: 2rem;
    cursor: pointer;
    float: right;
  }

  /*
  reply content
  */

  .reply-content-wrap{
    margin-top: 1.5rem;
  }
  .reply-item{
    background: #f2f3f2;
    padding: .75rem 1rem;
    margin-bottom: .75rem;
  }
  .reply-top{
    display: flex;
    justify-content: space-between;
    color:#9c9c9c;
  }
  .name-wrap{
    font-size:1.2rem;
    margin-bottom: 0.875rem;
  }
  .rpl-name{
    color:#4a4a4a;
    font-weight:600;
  }
  .reply-context{
    font-size: 1.1rem;
  }
  .show-all-reply{
    color: #9ad3e2;
    cursor: pointer;
    font-size: 1rem;
  }

   /*
  report
   */

    .report{
      position: fixed;
      z-index: 100;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      background: rgba(0,0,0,.6);
      overflow: hidden;
    }
  .content-wrap{
    width: 29.25rem;
    height: 38rem;
    background: #f7fbfc;
    margin:10rem auto;
    display: flex;
    padding: 2.25rem 3rem;
    flex-direction: column;
    justify-content: space-between;
  }
  .content-wrap h2{
    text-align: left;
    margin: 0;
    padding-bottom:1rem ;
    border-bottom: 0.0625rem solid #e9e9e9;
  }
  .content-wrap h2 span{
    font-size: 1.2rem;
    color: #9b9b9b;
  }
  .checkbox-wrap{
    text-align: left;
    font-size: 1.2rem;
    position: relative;
    height: 20.875rem;
  }
  .checkbox-wrap label{
    margin-left: 1.5rem;
  }
  .check-item{
    position: relative;
    height: 3rem;
    padding: 0.875rem 0;
    line-height: 1.5rem;
    border-bottom: 0.0625rem solid #e9e9e9;
  }
  .checkbox-wrap textarea{
    display: block;
    height: 3.75rem;
    width: 100%;
    resize: none;
    border: 0.0625rem solid #979797;
    margin-top: 0.75rem;
    font-size: 1.1rem;
    background: #e9e9e9;
  }
  .sc-wrap{

  }
  .sc-wrap input{
    width: 7.5rem;
    height: 3rem;
    border-radius: 3rem;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
  }
  .sc-wrap .submit{
    margin-right: 1.5rem;
  }

  /*
  checkbox
   */

  input[type='checkbox']{
    opacity: 0;
    position: absolute;
    top: -33333px;
  }
  input[type='checkbox']:checked+label:before,
  input[type='checkbox']:not(:checked)+label:before{
    content: '';
    display: inline-block;
    width: 0.875rem;
    height: 0.875rem;
    border: 0.065rem solid #979797;
    border-radius: 50%;
    margin-right: 0.5rem;
    position: absolute;
    left: 0;
    top: .1rem;
    cursor: pointer;
  }
  input[type='checkbox']:checked+label:after{
    background: #9ad3e2;
  }
  input[type='checkbox']:not(:checked)+label:after,
  input[type='checkbox']:checked+label:after{
    content: '';
    display: inline-block;
    border-radius: 50%;
    width: 0.65rem;
    height: 0.65rem;
    position: absolute;
    left: 0.18rem;
    top: 0.26rem;
    cursor: pointer;
  }
</style>
