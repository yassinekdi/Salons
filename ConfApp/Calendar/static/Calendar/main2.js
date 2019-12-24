Vue.component('tabs', {
  template: `
  <div class="has-padding-top-8-desktop">

    <div>
      <button v-for="(tab, index) in tabs" :key="index" :class="{'btn btn-dark': tab.isActive, 'btn btn-light': !tab.isActive}" @click="selectTab(tab)">{{tab.name}}</button>
    </div>

    <div class="tab-content"><slot></slot></div>
  </div> `,


  data() {
    return { tabs: [] };
  },

  created() {
    this.tabs = this.$children;
  },

  methods: {
    selectTab(selectedTab){
      this.tabs.forEach(tab=> {
        tab.isActive = (tab.name==selectedTab.name);
      })
    }
  }
});

Vue.component('tab', {
  template: `
    <div v-show="isActive"><slot></slot></div>
  `,
  props: {
    name: {required: true},
    selected: {default: false}
  },
  data() {
    return { isActive: false}
  },
  mounted() {
    this.isActive= this.selected
  }

})


new Vue({
  el: '#app'


});



// Scroll
const slider = document.querySelector('.center');
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
  isDown = true;
  slider.classList.add('active');
  startX = e.pageX - slider.offsetLeft;
  scrollLeft = slider.scrollLeft
  console.log(startX)
});

slider.addEventListener('mouseleave', () => {
  isDown = false;
  slider.classList.remove('active');
});

slider.addEventListener('mouseup', () => {
  isDown = false;
  slider.classList.remove('active');
});

slider.addEventListener('mousemove', (e) => {
  if (!isDown) return; // stop the function from running
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft
  const walk = (x - startX)*3;
  slider.scrollLeft = scrollLeft - walk;
});