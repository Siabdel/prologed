
let eventGuid = 0
let todayStr = new Date().toISOString().replace(/T.*$/, '') // YYYY-MM-DD of today

export const INITIAL_EVENTS_0 = [
  {
    id: createEventId(),
    title: 'All-day event',
    start: todayStr
  },
  {
    id: createEventId(),
    title: '###Timed event ####',
    start: todayStr + 'T12:00:00'
  }
];

export const INITIAL_EVENTS = [
   {
        "id": "3",
        "title": "Reservation for Hotel Mamounia ",
        "start": "2024-09-19T16:00:00",
        "end": "2024-09-19T11:00:00",
        "guest_name": "John Doe",
        "guest_email": "john.doe@example.com",
        "reservation_status": "confirmed",
        "number_of_guests": 4,
        "total_price": "1750.00",
        "bgColor": "#00a9ff",
        "color": "white"
    },
      {
          "id": "1",
          "title": "Reservation for Sunny Beach Villa",
          "start": "2024-09-19" + 'T12:00:00',
          "end": "2024-09-19" + 'T14:00:00',
          "category": "time",
          "bgColor": "#00a9ff",
          "color": "white"
      },
      {
          "id": "2",
          "title": "Reservation for Villa Provençale",
          "start": "2024-09-27" + 'T10:00:00',
          "end": "2024-09-27" + 'T14:00:00',
          "category": "time",
          "bgColor": "#00a9ff",
          "color": "white"
      }
  ];

export function createEventId() {
  return String(eventGuid++)
}
