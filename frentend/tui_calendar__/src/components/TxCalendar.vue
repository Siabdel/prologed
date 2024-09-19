
<template>

  <div id="calendar" style="height: 800px">

  <h1> {{msg}}</h1>
      {{ calendars.length }}
  </div>
</template>

<script>
import Calendar from "tui-calendar"; /* ES6 */
import "tui-calendar/dist/tui-calendar.css";

// If you use the default popups, use this.
import "tui-date-picker/dist/tui-date-picker.css";
import "tui-time-picker/dist/tui-time-picker.css";
export default {
  name: "tx-calendar",
  props: {
    msg : {
      type : String,
      default : ""
    },
    calendarView: {
      type: String,
      default: function () {
        return "month";
      },
    },
    calendars: {
      type: Array,
      default: function () {
        return [];
      },
    },
    hiddenCalendarsId: {
      type: Array,
      default: function () {
        return [];
      },
    },
    defaultTheme: {
      type: Object,
      default: function () {
        return {};
      },
    },
  },
  data: function () {
    return {
      calendar: null,
    };
  },
  watch: {
    calendars: {
      handler: function (newCalendars) {
        console.log(newCalendars);
      },
    },
    calendarView: {
      handler: function (view) {
        this.calendar.changeView(view, true);
      },
    },
    hiddenCalendarsId: {
      handler: function (val) {
        console.log(val);
        this.refreshCalendars();
        this.hideSchedules(val);
      },
    },
  },
  methods: {
    initCalendar: function () {
      return new Promise((resolve ) => {
        this.calendar = new Calendar("#calendar", {
          calendarView: this.calendarView,
          taskView: true,
          scheduleView: true,
          useDetailPopup: true,
          useCreationPopup: true,
          template: {
            popupDetailBody: (schedule) => {
              return "Body : " + schedule.body;
            },
          },
          calendars: this.calendars,
        });
        this.calendar.setTheme(this.defaultTheme);

        resolve();
      });
    },
    /**
     * @param {array} calendars.schedules
     */
    addSchedule: function (schedules) {
      // ADD SCHEDULEs
      console.log("addSchedule ...")
      this.calendar.createSchedules(schedules);
    },
    addCalendarsSchedules: function () {
      this.calendars.forEach((calendar) => {
        this.addSchedule(this.getSchedulesFromCalendar(calendar));
      });
    },
    handleUpdateSchedule: function () {
      // HANDLE SCHEDULE UPDATE
      this.calendar.on("beforeUpdateSchedule", (event) => {
        var schedule = event.schedule;
        var changes = event.changes;

        this.calendar.updateSchedule(schedule.id, schedule.calendarId, changes);
        let element = this.calendar.getSchedule(
          schedule.id,
          schedule.calendarId
        );
        this.$emit("updated-schedule", element);
      });
    },
    handleClickSchedule: function () {
      let lastClickSchedule = null;
      // HANDLE OPEN DETAIL ON CLICK SCHEDULE
      this.calendar.on("clickSchedule", (event) => {
        var schedule = event.schedule;

        // focus the schedule
        if (lastClickSchedule) {
          this.calendar.updateSchedule(
            lastClickSchedule.id,
            lastClickSchedule.calendarId,
            {
              isFocused: false,
            }
          );
        }
        this.calendar.updateSchedule(schedule.id, schedule.calendarId, {
          isFocused: false,
        });

        lastClickSchedule = schedule;
        let element = this.calendar.getSchedule(
          schedule.id,
          schedule.calendarId
        );
        this.$emit("clicked-schedule", element);
        // open detail view
      });
    },
    handleDeleteSchedule: function () {
      this.calendar.on("beforeDeleteSchedule", (event) => {
        var schedule = event.schedule;
        this.$emit("deleted-schedule", schedule);
      });
    },
    /**
     * @param {object} calendar
     */
    getSchedulesFromCalendar: function (calendar) {
      if (!calendar.schedules) return [];

      calendar.schedules.forEach((schedule) => {
        schedule.calendarId = calendar.id;
      });
      return calendar.schedules;
    },
    refreshCalendars: function () {
      this.calendar.clear();
      this.addCalendarsSchedules();
      this.calendar.render();
    },
    handleScreenResizing: function () {
      // Render a calendar when resizing a window.
      window.addEventListener("resize", () => {
        this.calendar.render();
      });
    },
    /**
     * @param {array} calendarsId
     */
    hideSchedules: function (calendarsId) {
      let toHide = true;
      let reRender = true;
      calendarsId.forEach((calendarId) => {
        this.calendar.toggleSchedules(calendarId, toHide, reRender);
      });
    },
  },
  mounted: function () {
    this.initCalendar().then(() => {
      this.addCalendarsSchedules();
      this.handleUpdateSchedule();
      this.handleClickSchedule();
      this.handleScreenResizing();
      this.handleDeleteSchedule();
      this.hideSchedules(this.hiddenCalendarsId);
      this.$emit("calendar-mounted", this.calendar);
    });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.scheduleTeste {
  background-color: red;
  color: white;
}
</style>
