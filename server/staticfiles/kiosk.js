Vue.createApp({
    data() {
        return {
            message: "Loading ..."
        }
    },
    mounted() {
        this.message = "Hello, World! I'm a bird computer. " + Date();
        // Refresh every second.
        let _this = this;
        setInterval(() => {
            _this.message = "Hello, World! I'm a bird computer. " + Date();
        }, 1000);
    }
}).mount("#app");


