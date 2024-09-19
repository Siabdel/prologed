<template>
  <div id="app">
    <h1>  <div>{{ meeting.date }}</div></h1>
    <vue-meeting-selector
      class="simple-example__meeting-selector"
      v-model="meeting"
      :date="date"
      :loading="loading"
      :meetings-days="meetingsDays"
      @next-date="nextDate"
      @previous-date="previousDate"
      @change="getMeetings"
      @meeting-slot-selected="getMeetingDate"
    />
    <p>meeting Selected: {{ meeting ? meeting : "No Meeting selected" }}</p>
  </div>
</template>
 
<script>
import VueMeetingSelector from "vue-meeting-selector";
import data from "./data.json";

export default {
  name: "App",
  components: {
    VueMeetingSelector,
  },
  data() {
    return {
      date: new Date(),
      meetingsDays: [],
      meeting: { date: "2021-01-19T:09:00.000Z" },
      loading: true,
      nbDaysToDisplay: 5,
    };
  },
  methods: {
    getMeetingDate(){
        console.log("date selected = " + this.meeting.date)
    },
    getMeetings(rdv) {
        console.log("get meetings = " + rdv.date)
        return this.avaiable;
    },
    // @click on button-right
    async nextDate() {
      console.log("nextDate");
    },
    // @click on button-left
    async previousDate() {
      console.log("previousDate");
    },
  },
  created() {
    this.meetingsDays = data;
    this.loading = false;
  },
};
</script>

