<script setup>
import {ref} from "vue";
import {Promotion, Expand, Close, Tools, HelpFilled} from "@element-plus/icons-vue";
import {useUserStore} from "@/stores/user";
import Login from '@/views/Login/index.vue'
import {ElMessage} from "element-plus";

const userStore = useUserStore()
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
}
const confirm = async () => {
  const res = await userStore.userLogout()
  ElMessage({type: 'success', message: res.info})
}
const show = ref(false)
const changeShow = () => {
  show.value = !show.value;
}
</script>

<template>
  <nav class="menu" :class="{ open: isMenuOpen }">
    <div class="logoSection">
      <RouterLink to="/">
        <img src="../assets/logo.png" alt="Logo" style="pointer-events:none;">
      </RouterLink>
    </div>

      <div class="actionsBar">
        <div>
          <button 
            id="menuBtn" 
            type="button" 
            @click="toggleMenu" 
            aria-label="Toggle menu">
            <i class="iconfont icon-hanbaocaidan"></i>
          </button>
          <h3 class="menuText" :class="{ open2: isMenuOpen }">
              {{ userStore.userInfo.username || 'Hashtopia' }}
          </h3>
        </div>
      </div>
    <ul class="optionsBar">
      <li class="menuItem">
          <RouterLink to="/" class="menuOption">
            <i class="iconfont icon-shouye"></i>
            <h5 class="menuText" :class="{ open2: isMenuOpen }">Home</h5>
          </RouterLink>
      </li>
      <li class="menuBreak">
        <hr>
      </li>
      <li class="menuItem">
          <RouterLink v-if="userStore.userInfo.id" to="/user/uploads" class="menuOption">
              <el-icon size="x-large">
                  <Promotion/>
              </el-icon>
              <h5 class="menuText" :class="{ open2: isMenuOpen }">Post</h5>
          </RouterLink>
          <a v-else class="menuOption" @click.prevent="changeShow" href="#">
              <el-icon size="x-large">
                  <Promotion/>
              </el-icon>
              <h5 class="menuText" :class="{ open2: isMenuOpen }">Post</h5>
          </a>
      </li>
      <li class="menuItem" v-if="userStore.userInfo.id">
          <RouterLink to="/user/control">
            <div class="menuOption">
              <el-icon size="x-large">
                <HelpFilled/>
              </el-icon>
              <h5 class="menuText" :class="{ open2: isMenuOpen }">Control</h5>
            </div>
          </RouterLink>
      </li>
    </ul>
    <div v-if="userStore.userInfo.id" class="menuBottom">
      <div class="menuUser">
        <RouterLink :to="`/user/index/${userStore.userInfo.id}`">
          <div>
            <img :src="userStore.userInfo.avatar" alt="">
          </div>
          <h5 class="Username menuText" :class="{ open2: isMenuOpen }" v-show="isMenuOpen">
            {{ userStore.userInfo.username }}</h5>
          <p class="menuText" :class="{ open2: isMenuOpen }"></p>
        </RouterLink>
      </div>
      <div class="themeBar">
          <div>
            <el-popconfirm @confirm="confirm" title="Are you sure you want to exit?" confirm-button-text="Yes"
                           cancel-button-text="No">
              <template #reference>
                <button type="button" @click="" aria-label="Exit" ><i class="iconfont icon-tuichu"></i></button>
              </template>
            </el-popconfirm>
          </div>
      </div>
    </div>
    <div v-else>
        <div class="themeBar">
          <div>
            <button title="Login" type="button" @click="changeShow">
              <el-icon size="x-large">
                <Expand/>
              </el-icon>
            </button>
          </div>
        </div>
    </div>
  </nav>
  <div class="overlay" v-if="show">
    <el-button class="close" @click="changeShow" plain round>
      <el-icon size="x-large">
        <Close/>
      </el-icon>
    </el-button>
    <login @changeShow="changeShow"/>
  </div>
</template>

<style scoped>
.fileUpload {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}


.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.close {
  position: absolute;
  top: 40px;
  right: 40px;
  z-index: 1000;
  background: #ff4d4d;
  border: 2px solid #ff3333;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.close:hover {
  background: #ff3333;
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.iconfont {
  font-size: 20px;
}

.menu {
  max-width: 240px;
  position: absolute;
  width: 60px;
  height: 96vh;
  background-color: #eddddd;
  z-index: 2;
  top: 1vh;
  bottom: 0;
  left: 2vw;
  margin: auto;
  border-radius: 0.8rem;
  transition: 0.3s ease 0.15s;
  font-family: sans-serif;
}

.menu a {
  text-decoration: none;
}

.menu .actionsBar {
  width: 100%;
  height: 10%;
  padding: 0.5rem;
  overflow: hidden;
}

.menu .actionsBar div {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0.5rem;
  transition: 0.3s ease;
}

.menu .actionsBar div button {
  background-color: transparent;
  outline: none;
  border: none;
  border-radius: 0.5rem;
  color: #000;
  width: 45px;
  height: 45px;
  transition: 0.3s ease;
  font-size: 1rem;
}

.menu .actionsBar div button:hover {
  background-color: #d5d0d0;
  color: #F19FA3;

}

.menu .actionsBar div h3 {
  width: calc(100% - 45px);
  text-align: center;
}

/* Add new styles for logo section */
.logoSection {
  width: 100%;
  padding: 1rem 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.5rem;
}

.logoSection img {
  width: auto;
  height: 4vh;
  transition: 0.3s ease;
}

.menu.open .logoSection img {
  width: auto;
  height: 6vh;
}

.menu .optionsBar {
  overflow: hidden;
  display: flex;
  width: 100%;
  height: 55%;
  padding: 0 0.5rem;
  align-items: center;
  flex-direction: column;
}

.menu .optionsBar .menuItem {
  width: 100%;
  height: 5vh;
  margin: 0.3rem;
}

.menu .optionsBar .menuItem .menuOption {
  font-size: 1rem;
  outline: none;
  border: none;
  background-color: transparent;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0.5rem;
  transition: 0.3s ease;
}

.menu .optionsBar .menuItem .menuOption:hover {
  background-color: #d5d0d0;
  color: #f5131e;
}

.menu .optionsBar .menuItem .menuOption:hover i,
.menu .optionsBar .menuItem .menuOption:hover h5 {
  color: #f5131e;

}

.menu .optionsBar .menuItem .menuOption i {
  width: 45px;
  text-align: center;
  color: #000;
}

.menu .optionsBar .menuItem .menuOption h5 {
  width: calc(100% - 45px);
}

.menuText {
  color: black;
  transform: translateX(-250px);
  opacity: 0;
  transition: transform 0.3s ease 0.1s;
}


.menu.open {
  width: 20vw;
  opacity: 1;
}

@media screen and (max-width: 768px) {
  .menu.open {
    width: 50vw;
  }
}

.menuText.open2 {
  opacity: 1;
  transform: translateX(0);
  text-align: center;
}

.menu .menuBreak {
  width: 100%;
  height: 1vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu .menuBreak hr {
  width: 70%;
  height: 0.3vh;
  background-color: #000;
  border: none;
  border-radius: 5px;
}

.menu .themeBar {
  overflow: hidden;
  width: 100%;
  height: 10%;
  padding: 0.5rem;
}

.menu .themeBar div {
  width: 100%;
  max-width: 225px;

  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0.5rem;
  transition: 0.3s ease;
}

.menu .themeBar div button {
  background-color: transparent;
  outline: none;
  border: none;
  border-radius: 0.5rem;
  color: #000;
  width: 100%;
  height: 45px;
  transition: 0.3s ease;
  font-size: 1rem;
}

.menu .themeBar div button:hover {
  background-color: #d5d0d0;
  color: #f5131e;
}

.menu .menuUser {
  position: relative;
  width: 100%;
  max-width: 240px;
  height: 10%;
}

.menu .menuUser a {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
  padding: 0.5rem;
  position: relative;
}

.menu .menuUser a div {
  width: 45px;
  height: 45px;
  position: relative;
  border-radius: 0.5rem;
}

.menu .menuUser a div img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
}

.menu .menuUser a .Username {
  width: calc(70% - 45px);
}

.menu .menuUser a p {
  width: calc(30% - 45px);
}

.menu .menuUser a:hover p {
  animation: animArrow 0.3s ease 2;
  color: #F19FA3;

}


@keyframes animArrow {
  0% {
    transform: translateX(0);
  }

  50% {
    transform: translateX(5px);
  }

  100% {
    transform: translateX(0);
  }
}

.menu .menuUser:hover .userInfo {
  pointer-events: all;
  opacity: 1;
  transform: scale(1);
  color: #f0474f;
}

.el-button--text {
  margin-right: 15px;
}


.el-input {
  width: 300px;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}

.menuBottom {
 position: fixed;
 bottom: 4vh;
 width: inherit;
}
</style>