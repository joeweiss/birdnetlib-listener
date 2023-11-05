Vue.createApp({
  data() {
    return {
      message: "Loading ...",
      detectionsNow: [],
      detectionsToday: [],
      speciesImages: {},
      view: "detections",
      viewModes: ["detections", "daily", "weather"],
      rotationSeconds: 10,
      nowCheckSeconds: 5,
      weatherRefreshSeconds: 60 * 5,
      weatherCurrent: {},
      weatherForecast: {},
      weatherLoaded: false,
    };
  },
  mounted() {
    this.message = "Loading ...";

    this.getCurrentDetections();
    this.getDailyBirds();
    this.getWeatherCurrent();
    this.getWeatherForecast();

    // Refresh every second for clock.
    let _this = this;
    setInterval(() => {
      const currentDate = new Date();
      const formattedTime = currentDate.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
      });
      _this.message = formattedTime;
    }, 1000);

    // Refresh every 15 seconds for detections.
    setInterval(() => {
      _this.getCurrentDetections();
    }, 1000 * this.nowCheckSeconds);

    // Rotate the mode every 60 seconds.
    setInterval(() => {
      const currentIndex = _this.viewModes.indexOf(_this.view);
      const nextIndex = (currentIndex + 1) % _this.viewModes.length;
      _this.view = _this.viewModes[nextIndex];
    }, 1000 * this.rotationSeconds);

    // Refresh the weather.
    setInterval(() => {
      getWeatherCurrent();
    }, 1000 * this.weatherRefreshSeconds);
  },
  methods: {
    async getCurrentDetections() {
      let _this = this;
      try {
        const response = await fetch("/api/now-detections/"); // Replace with your API endpoint
        if (response.ok) {
          const data = await response.json();
          console.log("Current Detections:", data);
          // Further processing or state update with the fetched data
          _this.detectionsNow = data;
          _this.detectionsNow.forEach((item) => {
            _this.getNewImage(item.species.id);
          });
        } else {
          throw new Error("Failed to fetch data");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        // Handle error scenarios
      }
    },
    async getDailyBirds() {
      let _this = this;
      try {
        const response = await fetch("/api/daily-species/"); // Replace with your API endpoint
        if (response.ok) {
          const data = await response.json();
          console.log("Today Detections:", data);
          // Further processing or state update with the fetched data
          const numberToDisplay = 10;
          _this.detectionsToday = data.slice(0, numberToDisplay);
          // _this.detectionsNow.forEach((item) => {
          //   _this.getNewImage(item.species.id);
          // });
        } else {
          throw new Error("Failed to fetch data");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        // Handle error scenarios
      }
    },
    async getNewImage(speciesId) {
      let _this = this;
      try {
        const response = await fetch(`/api/species/${speciesId}/image/`); // Replace with your API endpoint
        if (response.ok) {
          const data = await response.json();
          console.log("Current Detections:", data);
          // Further processing or state update with the fetched data
          _this.speciesImages[speciesId] = data.url;
        } else {
          throw new Error("Failed to fetch data");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        // Handle error scenarios
        return "";
      }
    },
    async getWeatherCurrent() {
      let _this = this;
      try {
        const response = await fetch("/api/weather/current/");
        if (response.ok) {
          const data = await response.json();
          console.log("Current weather:", data);
          // Further processing or state update with the fetched data
          _this.weatherCurrent = data;
          _this.weatherLoaded = true;
        } else {
          throw new Error("Failed to fetch data");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        // Handle error scenarios
      }
    },
    async getWeatherForecast() {
      let _this = this;
      try {
        const response = await fetch("/api/weather/forecast/");
        if (response.ok) {
          const data = await response.json();
          console.log("Current forecast:", data);
          // Further processing or state update with the fetched data
          _this.weatherForecast = data;
        } else {
          throw new Error("Failed to fetch data");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        // Handle error scenarios
      }
    },
    pluralizeItem(count, itemName) {
      // Simple English pluralization example
      return count === 1 ? itemName : itemName + "s";
    },
    async callShutdown() {
      result = confirm("Shutdown?");
      if (result) {
        const response = await fetch("/api/shutdown/");
      }
    },
  },
}).mount("#app");
