<template>
  <div id="app">
    <div
      id="#overlay"
      v-if="currentCalendar"
      style="display: flex; justify-content: space-between">
      <div style="display: flex">
        <a
          href="#"
          class="square_btn_tab"
          @click="currentCalendarView = 'month'"
          >Month</a>
        <a href="#" class="square_btn_tab" @click="currentCalendarView = 'day'"
          >Day</a>
        <a href="#" class="square_btn_tab" @click="currentCalendarView = 'week'" >Week</a>
      </div>

      <div style="display: flex">
        <a href="#" class="square_btn blue" @click="currentCalendar.prev()">
          <i class="fa fa-chevron-right"></i>  Previous
        </a>
        <a href="#" class="square_btn blue" @click="currentCalendar.today()">
          <i class="fa fa-chevron-right"></i> Today
        </a>
        <a href="#" class="square_btn blue" @click="currentCalendar.next()">
          <i class="fa fa-chevron-right"></i> Next >
        </a>
      </div>

      <!--h4>{{ currentCalendar.getDateRangeStart()["_date"] }}</h4>
      <h4>{{ currentCalendar.getDateRangeEnd()["_date"] }}</h4-->
    </div>
    <!--label for="cars">Hide calendars:</label>

    <select v-model="hiddenCalendarsId" name="cars" id="cars" multiple>
      <option value="maintenances">maintenances</option>
      <option value="verifications">Verifications</option>
    </select-->

    <tx-calendar
      :msg="message"
      :calendars="foo"
      :hiddenCalendarsId="hiddenCalendarsId"
      :theme="defaultTheme"
      :calendarView="currentCalendarView"
      @calendar-mounted="storeCalendar"
      @updated-schedule="handleScheduleUpdate"
      @clicked-schedule="handleScheduleClicked"
      @deleted-schedule="handleScheduleDeleted"
    />
  </div>
</template>

<script>
import TxCalendar from "./components/TxCalendar.vue";
var themeDefaultConfig = {
  "common.border": "1px solid #e5e5e5",
  "common.backgroundColor": "black",
  "common.holiday.color": "#ff4040",
  "common.saturday.color": "#333",
  "common.dayname.color": "#333",
  "common.today.color": "#333",

  // creation guide style
  "common.creationGuide.backgroundColor": "rgba(81, 92, 230, 0.05)",
  "common.creationGuide.border": "1px solid #515ce6",

  // month header 'dayname'
  "month.dayname.height": "31px",
  "month.dayname.borderLeft": "1px solid #e5e5e5",
  "month.dayname.paddingLeft": "10px",
  "month.dayname.paddingRight": "10px",
  "month.dayname.backgroundColor": "inherit",
  "month.dayname.fontSize": "12px",
  "month.dayname.fontWeight": "normal",
  "month.dayname.textAlign": "left",

  // month day grid cell 'day'
  "month.holidayExceptThisMonth.color": "rgba(255, 64, 64, 0.4)",
  "month.dayExceptThisMonth.color": "rgba(51, 51, 51, 0.4)",
  "month.weekend.backgroundColor": "inherit",
  "month.day.fontSize": "14px",

  // month schedule style
  "month.schedule.borderRadius": "2px",
  "month.schedule.height": "24px",
  "month.schedule.marginTop": "2px",
  "month.schedule.marginLeft": "8px",
  "month.schedule.marginRight": "8px",

  // month more view
  "month.moreView.border": "1px solid #d5d5d5",
  "month.moreView.boxShadow": "0 2px 6px 0 rgba(0, 0, 0, 0.1)",
  "month.moreView.backgroundColor": "white",
  "month.moreView.paddingBottom": "17px",
  "month.moreViewTitle.height": "44px",
  "month.moreViewTitle.marginBottom": "12px",
  "month.moreViewTitle.backgroundColor": "inherit",
  "month.moreViewTitle.borderBottom": "none",
  "month.moreViewTitle.padding": "12px 17px 0 17px",
  "month.moreViewList.padding": "0 17px",

  // week header 'dayname'
  "week.dayname.height": "42px",
  "week.dayname.borderTop": "1px solid #e5e5e5",
  "week.dayname.borderBottom": "1px solid #e5e5e5",
  "week.dayname.borderLeft": "inherit",
  "week.dayname.paddingLeft": "0",
  "week.dayname.backgroundColor": "inherit",
  "week.dayname.textAlign": "left",
  "week.today.color": "#333",
  "week.pastDay.color": "#bbb",

  // week vertical panel 'vpanel'
  "week.vpanelSplitter.border": "1px solid #e5e5e5",
  "week.vpanelSplitter.height": "3px",

  // week daygrid 'daygrid'
  "week.daygrid.borderRight": "1px solid #e5e5e5",
  "week.daygrid.backgroundColor": "inherit",

  "week.daygridLeft.width": "72px",
  "week.daygridLeft.backgroundColor": "inherit",
  "week.daygridLeft.paddingRight": "8px",
  "week.daygridLeft.borderRight": "1px solid #e5e5e5",

  "week.today.backgroundColor": "rgba(81, 92, 230, 0.05)",
  "week.weekend.backgroundColor": "inherit",

  // week timegrid 'timegrid'
  "week.timegridLeft.width": "72px",
  "week.timegridLeft.backgroundColor": "inherit",
  "week.timegridLeft.borderRight": "1px solid #e5e5e5",
  "week.timegridLeft.fontSize": "11px",
  "week.timegridLeftTimezoneLabel.height": "40px",
  "week.timegridLeftAdditionalTimezone.backgroundColor": "white",

  "week.timegridOneHour.height": "52px",
  "week.timegridHalfHour.height": "26px",
  "week.timegridHalfHour.borderBottom": "none",
  "week.timegridHorizontalLine.borderBottom": "1px solid #e5e5e5",

  "week.timegrid.paddingRight": "8px",
  "week.timegrid.borderRight": "1px solid #e5e5e5",
  "week.timegridSchedule.borderRadius": "2px",
  "week.timegridSchedule.paddingLeft": "2px",

  "week.currentTime.color": "#515ce6",
  "week.currentTime.fontSize": "11px",
  "week.currentTime.fontWeight": "normal",

  "week.pastTime.color": "#bbb",
  "week.pastTime.fontWeight": "normal",

  "week.futureTime.color": "#333",
  "week.futureTime.fontWeight": "normal",

  "week.currentTimeLinePast.border": "1px dashed #515ce6",
  "week.currentTimeLineBullet.backgroundColor": "#515ce6",
  "week.currentTimeLineToday.border": "1px solid #515ce6",
  "week.currentTimeLineFuture.border": "none",

  // week creation guide style
  "week.creationGuide.color": "#515ce6",
  "week.creationGuide.fontSize": "11px",
  "week.creationGuide.fontWeight": "bold",

  // week daygrid schedule style
  "week.dayGridSchedule.borderRadius": "2px",
  "week.dayGridSchedule.height": "24px",
  "week.dayGridSchedule.marginTop": "2px",
  "week.dayGridSchedule.marginLeft": "8px",
  "week.dayGridSchedule.marginRight": "8px",
};

var data_schedules = [
        {
          id: "maintenances",
          name: "My Calendar",
          theme: themeDefaultConfig,
          schedules_test: data_schedules,
          schedules : [
            {
              "id": "1",
              "title": "Test ok my schedule **App**",
              "category": "time",
              "start": "2024-09-18T12:30:00+09:00",
              "end": "2024-09-18T16:30:00+09:00",
              isPending: false,
              raw: { id: 111, whatisit: "raw option contains user datas" },
              customStyle: "scheduleTeste",
              bgColor: "red",
              color: "white",
              body: "body texte",
              location: "home/garden",
              attendees: ["User A", "User B"],
            },
            {
              "id": "2",
              "title": "my schedule 2 **APP**",
              "category": "time",
              "start": "2024-09-19T14:30:00+09:00",
              "end": "2024-09-19T15:30:00+09:00",
              bgColor: "green",
              dragBgColor: "red",
              borderColor: "black",
              color: "white",
            }, 
            {
              id: "verifications",
              name: "verifications",
              color: "#00a9ff",
              bgColor: "#00a9ff",
              dragBgColor: "#00a9ff",
              borderColor: "#00a9ff",
              schedules: [
                {
                  id: "3",
                  title: "my schedule 3",
                  category: "time",
                  dueDateClass: "",
                  start: "2024-09-20T22:30:00+09:00",
                  end: "2024-09-20T22:30:00+09:00",
                  bgColor: "#00a6e6",
                  dragBgColor: "red",
                  borderColor: "black",
                  color: "white",
                },
                {
                  id: "4",
                  title: "my schedule 4",
                  category: "time",
                  dueDateClass: "",
                  start: "2023-02-25T22:30:00+09:00",
                  end: "2023-02-30T22:30:00+09:00",
                  bgColor: "#6c3a9e",
                  dragBgColor: "red",
                  borderColor: "black",
                  color: "white",
                },
              ],
              }
          ] },

];
export default {
  name: "App",
  components: {
    TxCalendar,
  },
  data: function () {
    return {
      message : "",
      data : data_schedules,
      currentCalendar: null,
      currentCalendarView: "month",
      defaultTheme: themeDefaultConfig,
      hiddenCalendarsId: [], // calendars id can be string like 'todo'
      foo: [],
    };
  },
  created(){
      //let url = `http://localhost:8000/api/v1/prayer_time/`
      let url = `http://localhost:8000/api/v1/reservations/`

      //ajax load
      fetch(url)
          .then(response => response.json())
          .then(json => {
            setTimeout(() => {
              this.foo = json
              //console.log("created fetch =" + this.foo[0].schedules[0].title)
              console.log("add data_schedules in fetch =" + json)
              //alert("load data_schedules ...")
              this.message = "load data_schedules ..."
            }, 500);
          })  
          .catch(err => {
              console.error(err)
          });
    },
  methods: {
    handleScheduleUpdate: function (schedule) {
      console.log("handleScheduleUpdate", schedule);
    },
    handleScheduleClicked: function (schedule) {
      console.log("handleScheduleClicked", schedule);
    },
    handleScheduleDeleted: function (schedule) {
      console.log("handleScheduleDeleted", schedule);
    },
    storeCalendar: function (calendar) {
      this.currentCalendar = calendar;
    },
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
