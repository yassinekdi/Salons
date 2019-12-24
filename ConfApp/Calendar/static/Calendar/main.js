Vue.component('tabs', {
  template: `
  <div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css">
    <div>
      <button v-for="(tab, index) in tabs" :key="index" :class="{'btn btn-dark': tab.isActive, 'button is-white': !tab.isActive }" @click="selectTab(tab)">{{tab.name}}</button>
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
  methods: {
/**
 * scrollTo - Horizontal Scrolling
 * @param {(HTMLElement ref)} element - Scroll Container
 * @param {number} scrollPixels - pixel to scroll
 * @param {number} duration -  Duration of scrolling animation in millisec
 */
    scrollTo(element, scrollPixels, duration) {
      const scrollPos = element.scrollLeft;
      // Condition to check if scrolling is required
      if ( !( (scrollPos === 0 || scrollPixels > 0) && (element.clientWidth + scrollPos === element.scrollWidth || scrollPixels < 0)))
      {
        // Get the start timestamp
        const startTime =
          "now" in window.performance
            ? performance.now()
            : new Date().getTime();

        function scroll(timestamp) {
          //Calculate the timeelapsed
          const timeElapsed = timestamp - startTime;
          //Calculate progress
          const progress = Math.min(timeElapsed / duration, 1);
          //Set the scrolleft
          element.scrollLeft = scrollPos + scrollPixels * progress;
          //Check if elapsed time is less then duration then call the requestAnimation, otherwise exit
          if (timeElapsed < duration) {
            //Request for animation
            window.requestAnimationFrame(scroll);
          } else {
            return;
          }
        }
        //Call requestAnimationFrame on scroll function first time
        window.requestAnimationFrame(scroll);
      }
    },
    swipeLeft() {
      const content = this.$refs.content;
      this.scrollTo(content, -300, 800);
    },
    swipeRight() {
      const content = this.$refs.content;
      this.scrollTo(content, 300, 800);
    }
  }
});



