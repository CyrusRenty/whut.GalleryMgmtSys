<template>
  <div class="canvas-user-image" ref="canvas_user_image">
    <canvas
      :width="canvasWidth"
      :height="canvasHeight"
      class="cursorPointer"
      id="avatarEditorCanvas"
      ref="avatarEditorCanvas"
      @dragover.prevent
      @drop="onDrop"
      @mousedown="onDragStart"
      @touchstart="onDragStart"
      @click="clicked">
    </canvas>
    <input
      type="file"
      ref="input"
      @change="fileSelected"
      style="display:none;"
      accept="image/*"
      />
    <img :src="this.$store.state.user.userInfo.image" ref="img_user" class="user-image">
    <img src="../assets/Camera.png" @click="clickInput" ref="img_camera" draggable="false" class="camera img">
  </div>
</template>

<style type="text/css">
  #avatarEditorCanvas {
  border-radius: 50%;
}

.cursorPointer{
    cursor: pointer;
  background: #4a4a4a;
}

.cursorGrab{
    cursor: -webkit-grab;
    cursor: -moz-grab;
}

.cursorGrabbing{
    cursor: grabbing;
    cursor: -webkit-grabbing;
    cursor: -moz-grabbing;
}
.canvas-user-image{
  margin-top: 5rem;

}
  .canvas-user-image .user-image{
  z-index: 19;
  position: absolute;
  height: 10rem;
  width: 10rem;
  border-radius: 50%;
  top: 5rem;
  left: 5.8rem;
}
.camera{
  z-index: 20;
}
  .img{
    position: absolute;
    top: 8.3rem;
    left: 8.95rem;
    height: 3.3125rem;
  }
</style>

<script>
import {changeUserInfo} from "../api/user";

export default {
    props: {
        image: {
            type: String,
            default: ''
        },
        border: {
            type: Number,
            default: 0
        },
        borderRadius: {
            type: Number,
            default: 0
        },
        color: {
            type: Array,
            default: () => [0, 0, 0, 0]
        },
        scale: {
            default: 1
        },
        rotation: {
            default: 0
        }
    },
    data () {
        return {
            cursor: 'cursorPointer',
            canvas: null,
            context: null,
            dragged: false,
            imageLoaded: false,
            changed: false,
            width:100,
            height:100,
            state: {
                drag: false,
                my: null,
                mx: null,
                xxx: 'ab',
                image: {
                    x: 0,
                    y: 0,
                    resource: null
                }
            }
        };
    },
    computed: {
        canvasWidth () {
            return this.getDimensions().canvas.width;
        },
        canvasHeight () {
            return this.getDimensions().canvas.height;
        },
        rotationRadian () {
            return this.rotation * Math.PI / 180;
        }
    },
    mounted () {
        let self = this;
        this.canvas = this.$refs.avatarEditorCanvas;
        this.context = this.canvas.getContext('2d');
        this.paint();
        //
        // if (!this.image) {
        //    var placeHolder=new Image();
        //     placeHolder.src=this.$store.state.user.userInfo.image
        //     placeHolder.onload = function () {
        //      console.log(placeHolder)
        //       console.log(this.width,this.height,self.canvasWidth,self.canvasHeight)
        //         var x = self.canvasWidth / 2 - this.width / 2;
        //         var y = self.canvasHeight / 2 - this.height / 2;
        //         console.log(x,y)
        //         self.context.drawImage(placeHolder, x, y, this.width, this.height);
        //     };
        //
        // } else {
        //     this.loadImage(this.image);
        // }
    },
    methods: {
        clickInput(){
        this.$refs.input.click()
      },//1
        drawRoundedRect (context, x, y, width, height, borderRadius) {

            if (borderRadius === 0) {
                context.rect(x, y, width, height);
            } else {
                const widthMinusRad = width - borderRadius;
                const heightMinusRad = height - borderRadius;
                context.translate(x, y);
                context.arc(borderRadius, borderRadius, borderRadius, Math.PI, Math.PI * 1.5);
                context.lineTo(widthMinusRad, 0);
                context.arc(widthMinusRad, borderRadius, borderRadius, Math.PI * 1.5, Math.PI * 2);
                context.lineTo(width, heightMinusRad);
                context.arc(widthMinusRad, heightMinusRad, borderRadius, Math.PI * 2, Math.PI * 0.5);
                context.lineTo(borderRadius, height);
                context.arc(borderRadius, heightMinusRad, borderRadius, Math.PI * 0.5, Math.PI);
                context.translate(-x, -y);
            }
        },//2
        setState (state1) {

            var min = Math.ceil(1);
            var max = Math.floor(10000);

            this.state = state1;
            this.state.cnt = 'HELLO' + Math.floor(Math.random() * (max - min)) + min;
        },//3
        paint () {
            this.context.save();
            this.context.translate(0, 0);
           // this.context.fillStyle = 'rgba(' + this.color.slice(0, 4).join(',') + ')';

            let borderRadius = this.borderRadius;
            const dimensions = this.getDimensions();
            const borderSize = dimensions.border;
            const height = dimensions.canvas.height;
            const width = dimensions.canvas.width;

            // clamp border radius between zero (perfect rectangle) and half the size without borders (perfect circle or "pill")
            // borderRadius = Math.max(borderRadius, 0);
            // borderRadius = Math.min(borderRadius, width / 2 - borderSize, height / 2 - borderSize);

            this.context.beginPath();

            // inner rect, possibly rounded
            // this.drawRoundedRect(
            //     this.context,
            //     borderSize,
            //     borderSize,
            //     width - borderSize * 2,
            //     height - borderSize * 2,
            //     borderRadius);

            //this.context.rect(width, 0, -width, height); // outer rect, drawn "counterclockwise"
            this.context.arc(width/2,height/2,height/2,0,2*Math.PI)
            this.context.restore();
        },//4
        getDimensions () {
          let client_width=document.documentElement.clientWidth*160/1920
          this.width=client_width;
          this.height=client_width
            return {
                width: this.width,
                height: this.height,
                border: this.border,
                canvas: {
                    width: client_width,
                    height: client_width
                }
            };

        },//5
        onDrop (e) {

            e = e || window.event;
            e.stopPropagation();
            e.preventDefault();

            if (e.dataTransfer && e.dataTransfer.files.length) {
                // this.props.onDropFile(e)
                const reader = new FileReader();
                const file = e.dataTransfer.files[0];
                this.changed = true;
                reader.onload = (e) => this.loadImage(e.target.result);
                reader.readAsDataURL(file);
            }
        },//6
        onDragStart (e) {

            e = e || window.event;
            e.preventDefault();
            this.state.drag = true;
            this.state.mx = null;
            this.state.my = null;
            this.cursor = 'cursorGrabbing';
            let eventSubject = document;
            let hasMoved = false;
            let handleMouseUp = (event) => {
                this.onDragEnd(event);
                if (!hasMoved && event.targetTouches) {
                    e.target.click();
                }
                eventSubject.removeEventListener('mouseup', handleMouseUp);
                eventSubject.removeEventListener('mousemove', handleMouseMove);
                eventSubject.removeEventListener('touchend', handleMouseUp);
                eventSubject.removeEventListener('touchmove', handleMouseMove);
            };
            let handleMouseMove = (event) => {
                hasMoved = true;
                this.onMouseMove(event);
            };
            eventSubject.addEventListener('mouseup', handleMouseUp);
            eventSubject.addEventListener('mousemove', handleMouseMove);
            eventSubject.addEventListener('touchend', handleMouseUp);
            eventSubject.addEventListener('touchmove', handleMouseMove);
        },//7
        onDragEnd (e) {

            if (this.state.drag) {
                this.state.drag = false;
                this.cursor = 'cursorPointer';
            }
        },//8
        onMouseMove (e) {

            e = e || window.event;
            if (this.state.drag === false) {
                return;
            }

            this.dragged = true;
            this.changed = true;

            let imageState = this.state.image;
            const lastX = imageState.x;
            const lastY = imageState.y;

            const mousePositionX = e.targetTouches ? e.targetTouches[0].pageX : e.clientX;
            const mousePositionY = e.targetTouches ? e.targetTouches[0].pageY : e.clientY;

            const newState = {
                mx: mousePositionX,
                my: mousePositionY,
                image: imageState
            };

            if (this.state.mx && this.state.my) {
                const xDiff = (this.state.mx - mousePositionX) / this.scale;
                const yDiff = (this.state.my - mousePositionY) / this.scale;

                imageState.y = this.getBoundedY(lastY - yDiff, this.scale);
                imageState.x = this.getBoundedX(lastX - xDiff, this.scale);
            }

            this.state.mx = newState.mx;
            this.state.my = newState.my;
            this.state.image = imageState;
            // this.setState(newState)
        },//9
        replaceImageInBounds () {

            let imageState = this.state.image;
            imageState.y = this.getBoundedY(imageState.y, this.scale);
            imageState.x = this.getBoundedX(imageState.x, this.scale);
        },//10
        loadImage (imageURL) {
            let imageObj = new Image();
            let self = this;

            // imageObj.onload = () => this.handleImageReady(imageObj);
            imageObj.onload = () => {
                let imageState = self.getInitialSize(imageObj.width, imageObj.height);
                self.state.image.x = 0;
                self.state.image.y = 0;
                self.state.image.resource = imageObj;
                self.state.image.width = imageState.width;
                self.state.image.height = imageState.height;
                self.state.drag = false;
                self.$emit('image-ready', self.scale);
                self.imageLoaded = true;
                self.cursor = 'cursorGrab';
            };
            imageObj.onerror = (err) => console.log('error loading image: ', err);

            // imageObj.onerror = this.props.onLoadFailure
            if (!this.isDataURL(imageURL)) {
                imageObj.crossOrigin = 'anonymous';
            }

          imageObj.src = imageURL;
        },//11
        getInitialSize (width, height) {
            let newHeight;
            let newWidth;

            const dimensions = this.getDimensions();
            const canvasRatio = dimensions.height / dimensions.width;
            const imageRatio = height / width;

            if (canvasRatio > imageRatio) {
                newHeight = (this.getDimensions().height);
                newWidth = (width * (newHeight / height));
            } else {
                newWidth = (this.getDimensions().width);
                newHeight = (height * (newWidth / width));
            }
            return {
                height: newHeight,
                width: newWidth
            };
        },//12
        isDataURL (str) {
            if (str === null) {
                return false;
            }
            return !!str.match(/^\s*data:([a-z]+\/[a-z]+(;[a-z\-]+=[a-z\-]+)?)?(;base64)?,[a-z0-9!$&',()*+;=\-._~:@\/?%\s]*\s*$/i); // eslint-disable-line no-useless-escape
        },//13
        getBoundedX (x, scale) {

            var image = this.state.image;
            var dimensions = this.getDimensions();
            let width = Math.abs(image.width * Math.cos(this.rotationRadian)) + Math.abs(image.height * Math.sin(this.rotationRadian));
            let widthDiff = Math.floor((width - dimensions.width / scale) / 2);
            widthDiff = Math.max(0, widthDiff);
            return Math.max(-widthDiff, Math.min(x, widthDiff));
        },//14
        getBoundedY (y, scale) {

            var image = this.state.image;
            var dimensions = this.getDimensions();
            let height = Math.abs(image.width * Math.sin(this.rotationRadian)) + Math.abs(image.height * Math.cos(this.rotationRadian));
            let heightDiff = Math.floor((height - dimensions.height / scale) / 2);
            heightDiff = Math.max(0, heightDiff);
            return Math.max(-heightDiff, Math.min(y, heightDiff));
        },//15
        paintImage (context, image, border) {
            if (image.resource) {
                var position = this.calculatePosition(image, border);
                context.save();
                context.globalCompositeOperation = 'destination-over';
                let dimensions = this.getDimensions();
                context.translate(dimensions.canvas.width / 2, dimensions.canvas.height / 2);
                context.rotate(this.rotationRadian);
                context.translate(-dimensions.canvas.width / 2, -dimensions.canvas.height / 2);
                context.drawImage(
                    image.resource,
                    position.x,
                    position.y,
                    position.width,
                    position.height);
                context.restore();
            }
        },//16
        transformDataWithRotation (x, y) {
            let radian = -this.rotationRadian;
            let rx = x * Math.cos(radian) - y * Math.sin(radian);
            let ry = x * Math.sin(radian) + y * Math.cos(radian);
            return [rx, ry];
        },//17
        calculatePosition (image, border) {
            image = image || this.state.image;
            var dimensions = this.getDimensions();
            let width = image.width * this.scale;
            let height = image.height * this.scale;
            var widthDiff = (width - dimensions.width) / 2;
            var heightDiff = (height - dimensions.height) / 2;
            var x = image.x * this.scale;// - widthDiff;
            var y = image.y * this.scale;// - heightDiff;
            [x, y] = this.transformDataWithRotation(x, y);
            x += border - widthDiff;
            y += border - heightDiff;
            return {
                x,
                y,
                height,
                width
            };
        },//18
        redraw () {
            this.context.clearRect(0, 0, this.getDimensions().canvas.width, this.getDimensions().canvas.height);
            this.paint();
            this.paintImage(this.context, this.state.image, this.border);
        },//19
        getImage () {
            const cropRect = this.getCroppingRect();
            const image = this.state.image;

            // get actual pixel coordinates
            cropRect.x *= image.resource.width;
            cropRect.y *= image.resource.height;
            cropRect.width *= image.resource.width;
            cropRect.height *= image.resource.height;

            // create a canvas with the correct dimensions
            const canvas = document.createElement('canvas');
            canvas.width = cropRect.width;
            canvas.height = cropRect.height;

            // draw the full-size image at the correct position,
            // the image gets truncated to the size of the canvas.
            canvas.getContext('2d').drawImage(image.resource, -cropRect.x, -cropRect.y);
            return canvas;
        },//20
        getImageScaled () {
          let file=this.$refs.input.files[0]
          if(!file)
            return false
            const { width, height } = this.getDimensions();

            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            let newCtx=canvas.getContext('2d')

            // don't paint a border here, as it is the resulting image
            //this.paintImage(canvas.getContext('2d'), this.state.image, 0);
            let imgDataA = this.context.getImageData(0, 0, canvas.width, canvas.height);
            newCtx.putImageData(imgDataA,0,0,0,0,canvas.width,canvas.height)
          //   canvas.toBlob((blob)=>{
          //   let data=new FormData
          //     let reader=new FileReader()
          //     reader(blob)
          //   data.append('image',blob)
          //   changeUserInfo(this.$store.state.user.userInfo.id,data).then((res)=>{
          //     console.log(res.data)
          //   })
          // }, `${file.type}`,1)
            let newImg=canvas.toDataURL(`${file.type}`)
            let bytes=window.atob(newImg.split(',')[1]);        //去掉url的头，并转换为byte
            //处理异常,将ascii码小于0的转换为大于0
            let ab = new ArrayBuffer(bytes.length);
            let ia = new Uint8Array(ab);
            for (let i = 0; i < bytes.length; i++) {
              ia[i] = bytes.charCodeAt(i);
            }
          let newFile=new File([ab],file.name, {type : `${file.type}`})
          //   //let newFile=new Blob( [ab] , {type : `${file.type}`});
          //   // console.log(file.type)
          //  // newFile.filename=file.name
          //
          //    //console.log(newFile.filename)
           console.log(newFile)
            return newFile;
        },//21
        imageChanged () {
            return this.changed;
        },//22
        getCroppingRect () {
            const dim = this.getDimensions();
            const frameRect = {
                x: dim.border,
                y: dim.border,
                width: dim.width,
                height: dim.height
            };
            const imageRect = this.calculatePosition(this.state.image, dim.border);

            return {
                x: (frameRect.x - imageRect.x) / imageRect.width,
                y: (frameRect.y - imageRect.y) / imageRect.height,
                width: frameRect.width / imageRect.width,
                height: frameRect.height / imageRect.height
            };
        },//23
        clicked (e) {
            if (this.dragged === true) {
                this.dragged = false;
            } else {
                this.$refs.input.click();
            }
        },//24
        fileSelected (e) {
          this.$refs.img_camera.style.display='none'
          this.$refs.img_user.style.display='none'
            var files = e.target.files || e.dataTransfer.files;
            if (!files.length) {
                return;
            }
            // var image = new Image();
            var reader = new FileReader();
            this.changed = true;
            reader.onload = (e) => this.loadImage(e.target.result);
            reader.readAsDataURL(files[0]);

        },//25

    },
    watch: {
        state: {
            handler (val, oldval) {
                if (this.imageLoaded) {
                    this.redraw();
                }
            },
            deep: true
        },
        scale () {
            if (this.imageLoaded) {
                this.replaceImageInBounds();
                this.redraw();
            }
        },
        rotation () {
            if (this.imageLoaded) {
                this.replaceImageInBounds();
                this.redraw();
            }
        },
        borderRadius () {
            this.redraw();
        }
    }
};
</script>
