Vue.createApp({
    data() {
        return {
            message: "Loading ..."
        }
    },
    mounted() {
        this.message = "Hello, World! I'm a bird computer. " + Date();
        // Refresh in 10 seconds
        setTimeout(() => {
            window.location.reload();
        }, 30 * 1000);

    }
}).mount("#app");

