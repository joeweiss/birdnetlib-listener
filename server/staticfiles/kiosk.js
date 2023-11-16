Vue.createApp({
  data() {
    return {
      message: "Loading ...",
      detectionsNow: [],
      detectionNowDisplaying: null,
      detectionsToday: [],
      detectionTodayDisplaying: null,
      speciesImages: {},
      view: "detections",
      viewModes: ["detections", "weather"],
      rotationSeconds: 30,
      nowCheckSeconds: 15,
      rotateDetectedBirdSeconds: 15,
      dailyCheckSeconds: 120,
      weatherRefreshSeconds: 60 * 5,
      weatherCurrent: {},
      weatherForecast: {},
      weatherLoaded: false,
      imageIds: {},
    };
  },
  mounted() {
    this.message = "Starting ...";

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
        // second: "2-digit",
      });
      _this.message = formattedTime;
    }, 1000);

    // Refresh for current detections.
    setInterval(() => {
      _this.getCurrentDetections();
    }, 1000 * this.nowCheckSeconds);

    // Refresh for daily birds.
    setInterval(() => {
      _this.getDailyBirds();
    }, 1000 * this.dailyCheckSeconds);

    // Rotate the mode every 60 seconds.
    setInterval(() => {
      if (!_this.detectionsNow) return;
      if (_this.detectionsNow.length > 0 && _this.view == "detections") {
        // Do not rotate off of detections if there are now detections.
        return;
      }

      const currentIndex = _this.viewModes.indexOf(_this.view);
      const nextIndex = (currentIndex + 1) % _this.viewModes.length;
      _this.view = _this.viewModes[nextIndex];
    }, 1000 * this.rotationSeconds);

    // Rotate detected now bird.
    setInterval(() => {
      console.log("Rotating now bird.");
      const birdArray = _this.detectionsNow;
      if (birdArray.length == 0) {
        _this.detectionNowDisplaying = null;
        return;
      }

      if (_this.detectionNowDisplaying == null) {
        _this.detectionNowDisplaying = birdArray[0];
      }
      const currentIndex = birdArray.indexOf(_this.detectionNowDisplaying);
      const nextIndex = (currentIndex + 1) % birdArray.length;
      _this.detectionNowDisplaying = birdArray[nextIndex];
    }, 1000 * _this.rotateDetectedBirdSeconds);

    // Rotate detected daily bird.
    setInterval(() => {
      console.log("Rotating daily bird.");
      const birdArray = _this.detectionsToday;
      if (birdArray.length == 0) {
        _this.detectionTodayDisplaying = null;
        return;
      }
      if (_this.detectionTodayDisplaying == null) {
        _this.detectionTodayDisplaying = birdArray[0];
      }
      const currentIndex = birdArray.indexOf(_this.detectionTodayDisplaying);
      console.log(currentIndex);
      const nextIndex = (currentIndex + 1) % birdArray.length;
      _this.detectionTodayDisplaying = birdArray[nextIndex];
      console.log(_this.detectionTodayDisplaying.common_name);
    }, 1000 * _this.rotateDetectedBirdSeconds);

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

          // Did birds change?
          let newNowNeeded = true;
          if (
            arraysAreEqual(
              _this.detectionsNow.map((i) => i.id),
              data.map((i) => i.id)
            )
          ) {
            console.log("No changes!");
            newNowNeeded = false;
          }

          _this.detectionsNow = data;
          _this.detectionsNow.forEach((item) => {
            _this.getNewImage(item.species.id);
          });

          if (_this.detectionsNow.length > 0 && newNowNeeded) {
            // Set the displaying item.
            _this.detectionNowDisplaying = _this.detectionsNow[0];
          }
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
          _this.detectionsToday = data;
          _this.detectionsToday.forEach((item) => {
            _this.getNewImage(item.id);
          });

          if (_this.detectionsToday.length > 0) {
            // Set the displaying item.
            _this.detectionTodayDisplaying = _this.detectionsToday[0];
          }
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
          console.log("getNewImage:", data);
          // Further processing or state update with the fetched data
          _this.speciesImages[speciesId] = data.url;
          _this.imageIds[data.url] = data.id; // So you can reverse this later.
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
    async hideCurrentImage() {
      let current_image_url;
      if (this.detectionNowDisplaying) {
        current_image_url =
          this.speciesImages[this.detectionNowDisplaying.species.id];
      } else {
        current_image_url =
          this.speciesImages[this.detectionTodayDisplaying.id];
      }
      if (!current_image_url) return;
      result = confirm("Hide this image?");
      if (result) {
        const response = await fetch(
          `/api/species-images/${this.imageIds[current_image_url]}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ is_active: false }),
          }
        );
      }
    },
    returnRelativeTime(fromDate) {
      const currentDate = new Date();
      const providedDate = new Date(fromDate);

      const elapsed = currentDate.getTime() - providedDate.getTime();

      const seconds = Math.floor(elapsed / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);

      if (days > 0) {
        return `${days} day${days > 1 ? "s" : ""} ago`;
      } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? "s" : ""} ago`;
      } else if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
      } else {
        return `${seconds} second${seconds !== 1 ? "s" : ""} ago`;
      }
    },
  },
}).mount("#app");

function arraysAreEqual(arr1, arr2) {
  // Check if the arrays are of the same length
  if (arr1.length !== arr2.length) {
    return false;
  }

  // Check each element in the arrays
  for (let i = 0; i < arr1.length; i++) {
    // If any elements differ, arrays are not equal
    if (arr1[i] !== arr2[i]) {
      return false;
    }
  }

  // If all elements are equal, arrays are equal
  return true;
}
