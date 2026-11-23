# 🏥 Clinic Wait Time System

A simple, real-time queue management system for community health clinics. Patients can view wait times, and staff can manage the patient queue.

## 📋 Features

✅ **Patient Portal** - View current queue length and estimated wait time  
✅ **Staff Portal** - Add, remove, and prioritize patients in the queue  
✅ **Real-time Updates** - Queue changes visible within 2 minutes  
✅ **Audit Logging** - Track all staff actions  
✅ **Mobile Responsive** - Works on smartphones, tablets, and desktops  
✅ **No Installation Required** - JSON-based data storage, no database setup  

## 🚀 Quick Start

### Prerequisites
- **Node.js** (download from https://nodejs.org)

### Installation & Run

1. Navigate to the project directory:
```bash
cd C:\00_Dev_Hamid\claude\Clinic-Wait-Time
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

4. Open in your browser:
   - **Patient Portal**: http://localhost:3000/patient
   - **Staff Portal**: http://localhost:3000/staff

## 👥 Staff Login Credentials

| Username | Password |
|----------|----------|
| staff1   | demo123  |
| staff2   | demo123  |

## 📱 Portals

### Patient Portal
- Anonymous access (no login required)
- Displays current queue length
- Shows estimated wait time in minutes
- Updates every 15 seconds automatically
- Mobile-optimized interface

### Staff Portal
- Login with staff credentials
- View full queue with patient names and wait times
- Add new patients to the queue
- Remove patients when consultation completes
- Mark patients as urgent (move to front, reduce wait time by 15 minutes)
- View audit log of recent actions
- Display clinic open/closed status

## 📂 File Structure

```
clinic-wait-time/
├── server.js                 # Express backend server
├── patient.html              # Patient portal (read-only)
├── staff.html                # Staff portal (management UI)
├── package.json              # Node.js dependencies
├── queue.json                # Current queue data
├── consultations.json        # Historical consultation data
├── clinic_settings.json      # Clinic hours & staff credentials
├── audit_log.json            # Action audit trail
└── README.md                 # This file
```

## 🔄 How It Works

### Patient Flow
1. Patient visits http://localhost:3000/patient
2. Patient portal displays current queue length and wait time
3. Data refreshes automatically every 15 seconds
4. Patient decides whether to join the queue

### Staff Flow
1. Staff visits http://localhost:3000/staff and logs in
2. Dashboard shows current queue with all patient details
3. Staff adds patient: fills name + registration number
4. Staff removes patient when consultation completes
5. Staff can mark a patient as urgent (moves to front)
6. All actions logged to audit trail

## 📊 Wait Time Calculation

**Formula:**
```
Estimated Wait Time = (Average Consultation Duration × Number of Waiting Patients) - Urgent Adjustment
```

- **Average Consultation Duration**: Calculated from last 20 completed consultations
- **Urgent Adjustment**: Urgent patients have 15 minutes subtracted from their estimated wait time
- **Updates**: Recalculated whenever queue changes

## 🧪 Testing

### Manual Test Cases

**Patient Portal:**
- [ ] Load patient portal in browser → queue displays within 5 seconds
- [ ] Close staff portal and add patient → patient portal updates within 2 minutes
- [ ] Check on mobile device → no horizontal scrolling, readable text

**Staff Portal:**
- [ ] Login with staff1/demo123 → dashboard loads successfully
- [ ] Add patient → patient appears in queue within 2 seconds
- [ ] Remove patient → patient removed from queue, logged in audit trail
- [ ] Mark patient urgent → patient moves to top, wait time reduced by 15 minutes

**Edge Cases:**
- [ ] Empty queue → shows "0 patients waiting"
- [ ] Clinic closed (after 5 PM) → patient portal shows "Clinic Closed"
- [ ] Concurrent updates → both staff can add/remove without data loss
- [ ] Connection error → patient portal shows error message, retries automatically

## 📝 Data Files

### queue.json
Current queue entries with patient info and priority status

### consultations.json
Historical consultation records used to calculate average wait times

### clinic_settings.json
Clinic hours, staff credentials, and configuration

### audit_log.json
Audit trail of all staff actions (add, remove, mark urgent)

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## 🔧 Configuration

Edit `clinic_settings.json` to change:
- Clinic name
- Operating hours (open_time, close_time)
- Staff credentials
- Average consultation duration

## 📞 Support

For issues or questions, check:
1. Server is running (`npm start`)
2. Using correct URLs (http://localhost:3000/patient or /staff)
3. Correct staff credentials (staff1/demo123)
4. Browser console for error messages (F12)

---

**Version 1.0 - MVP** | Built for testing and demonstration
