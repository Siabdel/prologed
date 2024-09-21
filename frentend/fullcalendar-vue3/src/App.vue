<script>
import { defineComponent } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import listPlugin from '@fullcalendar/list';
import axios from 'axios'

import { formatInTimeZone } from 'date-fns-tz'
import { fr } from 'date-fns/locale'

export default defineComponent({
  components: {
    FullCalendar,
  },
  data() {
    return {
      
      calendarOptions: {
        // ... autres options ...
        timeZone: 'Europe/Paris',
        events: this.fetchEvents,
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, listPlugin,],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          //right: 'dayGridMonth,timeGridWeek,timeGridDay',
          right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },
        eventTimeFormat: { // ajoutez cette option
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        },
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        },
        initialView: 'dayGridMonth',
        views: {
          dayGridMonth: { // Utilisez ceci au lieu de 'dayGridMonth' directement
            // Options spécifiques à la vue mois si nécessaire
          },
          timeGridWeek: {
            // Options spécifiques à la vue semaine si nécessaire
          },
        },
        //initialEvents: INITIAL_EVENTS, // alternatively, use the `events` setting to fetch from a feed
        events: [],
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        eventClick: this.handleEventClick,
        eventsSet: this.handleEvents,
        eventChange: this.handleEventChange, 
        eventRemove: this.handleEventRemove,
        eventDidMount: this.handleEventDidMount,
        events: this.fetchEvents,
      },
      currentEvents: [],
    } 
  },
  // A la creation
  created(){
      //let url = `http://localhost:8000/api/v1/prayer_time/`
      let url = `http://localhost:8000/api/v1/reservations/`
      
      //ajax load
      fetch(url)
          .then(response => response.json())
          .then(json => {
              this.calendarOptions['events'] = json
              console.log("load data_schedules in fetch =" + this.events[0].title + ' - ' + json[0].start)
              //alert("load data_schedules ...")
          })  
          .catch(err => {
              //console.error(err)
          });
    },
  methods: {
    handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends // update a property
    },

   handleDateSelect(selectInfo) {
      let title = prompt('Please enter a title for the new event:')
      // new add 
      if (title) {
        let newEvent = {
          title: title,
          start: selectInfo.startStr,
          end: selectInfo.endStr,
          //allDay: selectInfo.allDay
        }
        // pai add 
        this.addEvent(newEvent)
      }
      selectInfo.view.calendar.unselect()
    },

  handleEventClick(clickInfo) {
      if (confirm(`Are you sure you want to Update the event '${clickInfo.event.title}'`)) {
        this.openAdminEdit(clickInfo.event.id)
      }
    },
  
  openAdminEdit(eventId) {
    const adminUrl = `${process.env.VITE_API_BASE_URL}/admin/logyapp/reservation/${eventId}/change/`
    const link = document.createElement('a')
    link.href = adminUrl
    link.target = '_blank'
    link.rel = 'noopener noreferrer'
    document.body.appendChild(link)
    link.click()
    //document.location = adminUrl
    //document.body.removeChild(link)
    window.location.href = '/' + adminUrl
  },
 
  //
  fetchEvents(fetchInfo, successCallback, failureCallback) {
    // Votre logique de récupération d'événements...
  },
 
    handleEvents(events) {
      this.currentEvents = events
    },
    // ADD event in DB
    async addEvent(event) {
      try {
        const url = 'http://localhost:8000/api/v1/reservations/'
        const reservationData = {
          property: 1, // Remplacez par l'ID de la propriété appropriée
          start_date: event.start,
          end_date: event.end,
          guest_name: event.title, // Ou demandez le nom du guest séparément
          guest_email: "example@email.com", // Ajoutez un champ pour l'email
          number_of_guests: 1, // Ajoutez un champ pour le nombre de guests
          total_price: 0, // Calculez le prix total ou laissez le backend le faire
        };

        const response = await axios.post(url, reservationData)
        this.calendarOptions.events.push(response.data)
      } catch (error) {
        console.error('Error adding event:', error)
      }
    },
    // Update
    handleEventChange(changeInfo) {
      console.log('Event changed:', changeInfo);
      this.updateEvent(changeInfo.event)
    },
    async updateEvent(event) {
      try {
        const updatedEvent = {
          title: event.title,
          property: 1, // Remplacez par l'ID de la propriété appropriée
          guest_name: event.title, // Ou demandez le nom du guest séparément
          guest_email: "example@email.com", // Ajoutez un champ pour l'email
          number_of_guests: 1, // Ajoutez un champ pour le nombre de guests
          total_price: 0, // Calculez le prix total ou laissez le backend le faire

          //allDay: event.allDay,
          roperty: event.extendedProps.property, // Assurez-vous que cette propriété existe
          start_date: event.start.toISOString().split('T')[0],
          end_date: event.end ? event.end.toISOString().split('T')[0] : null,
          guest_name: event.title,
        }
        const url = `http://localhost:8000/api/v1/reservations/${event.id}/`
        console.log('Updating event:', updatedEvent);
        const response = await 
        // fetch
        await axios.put(url, updatedEvent);
        console.log('Update response:', response.data);
      } catch (error) {
        console.error('Error updating event:', error.response ? error.response.data : error);
      }
    },
    
    async deleteEvent(event) {
      try {
        const url = `http://localhost:8000/api/v1/reservations/${event.id}/`;
        await axios.delete(url);
        event.remove();
      } catch (error) {
        console.error('Error deleting event:', error.response ? error.response.data : error);
      }
    },
    handleEventRemove(removeInfo) {
      this.deleteEvent(removeInfo.event)
    }
  },
    // end
})

</script>

<template>
  <div class='demo-app'>
    <div class='demo-app-sidebar'>
      <div class='demo-app-sidebar-section'>
        <h2>HAPPY BEE</h2>
        <ul>
          <li>Fullcalendar</li>
        </ul>
      </div>
      <div class='demo-app-sidebar-section'>
        <label>
          <input
            type='checkbox'
            :checked='calendarOptions.weekends'
            @change='handleWeekendsToggle'
          />
          toggle weekends
        </label>
      </div>
      <div class='demo-app-sidebar-section'>
        <h2>All Events ({{ currentEvents.length }})</h2>
        <ul>
          <li v-for='event in currentEvents' :key='event.id'>
            <b>{{ event.startStr }}</b>
            <i>{{ event.title }}</i>
          </li>
        </ul>
      </div>
    </div>
    <div class='demo-app-main'>
      <FullCalendar
        class='demo-app-calendar'
        :options='calendarOptions'
      >
        <template v-slot:eventContent='arg'>
          <b>{{ arg.timeText }}</b>
          <i>{{ arg.event.title }}</i>
        </template>
      </FullCalendar>
    </div>
  </div>
</template>

<style lang='css'>

h2 {
  margin: 0;
  font-size: 16px;
}

ul {
  margin: 0;
  padding: 0 0 0 1.5em;
}

li {
  margin: 1.5em 0;
  padding: 0;
}

b { /* used for event dates/times */
  margin-right: 3px;
}

.demo-app {
  display: flex;
  min-height: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.demo-app-sidebar {
  width: 300px;
  line-height: 1.5;
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.demo-app-sidebar-section {
  padding: 2em;
}

.demo-app-main {
  flex-grow: 1;
  padding: 3em;
}

.fc { /* the calendar root */
  max-width: 1100px;
  margin: 0 auto;
}

</style>
