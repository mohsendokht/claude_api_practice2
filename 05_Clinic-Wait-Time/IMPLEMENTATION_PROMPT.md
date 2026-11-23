# Clinic Wait Time System - Implementation Prompt

## Executive Summary
Build a browser-based queue management system enabling patients to view clinic wait times and clinic staff to manage patient queues in real time.

---

## PRIMARY AI PROMPT FOR CODE GENERATION

```
You are building the Clinic Wait Time System, a healthcare web application with three components:
1. Patient Portal (read-only queue viewer)
2. Staff Portal (queue management interface)  
3. Queue Management Service (backend logic and data storage)

REQUIREMENTS:
- Patients view current queue length and estimated wait time within 5 seconds
- Display must work on smartphones, tablets, and desktop browsers
- Staff can add, remove, and prioritize patients in <2 minutes per transaction
- Queue updates visible to patients within 2 minutes of staff changes
- At least 80% of wait-time estimates must be accurate to ±10 minutes
- Interface must be accessible to users with limited technical skills
- Authentication required for staff; patients use clinic registration number or access link
- Estimated wait time calculated as: (average consultation duration × current queue length) + priority adjustments
- Average consultation duration: rolling average of last 20 completed visits, recalculated hourly
- Urgent patients: move to front of queue, subtract 15 minutes from estimated wait time
- Patient portal: completely anonymous access via static clinic URL (no authentication required)
- Clinic hours: admin-configurable by staff; when closed, display "Clinic Closed" and hide queue data

ACCEPTANCE CRITERIA:
1. Patients can view queue length and estimated waiting time
2. Estimated waiting time updates automatically when queue changes
3. Staff can add, remove, and update patients; changes reflected within 2 minutes
4. System adjusts wait times correctly with priority/urgent cases
5. Mobile/tablet/desktop devices supported without technical assistance
6. Clear, easy-to-understand format suitable for limited technical skills
7. At least 80% of wait-time estimates within ±10 minutes during testing

TECHNICAL ARCHITECTURE:
- Patient Portal: Simple HTML/CSS/JavaScript web page, read-only
- Staff Portal: Web page with queue management UI
- Queue Management Service: Backend API handling queue logic and persistence
- Database: Central database storing queue records, timestamps, and historical data (retain 90 days, then purge)
- APIs: Secure API for staff updates (staff authentication required), read-only API for patient portal (anonymous)
- Mobile-responsive design with large text and clear labels
- Load time target: <5 seconds for patient portal
- Patient identification: Anonymous access via static clinic-provided URL
- Staff roles: Single generic "Staff" role for MVP (all staff can add/remove/prioritize)
- Audit logging: Every staff action logged with staff ID, timestamp, and action type
- Concurrent updates: Database transaction locking prevents duplicate removes; queue entries immutable once removed
- Data privacy: Patient names visible only in staff portal, never in patient portal

TESTING REQUIREMENTS:
Test Cases (TC-01 to TC-08):
- TC-01: Patient views queue info (numeric length ≥0 within 5 sec)
- TC-02: Estimated wait time displays and updates automatically
- TC-03: Staff adds patient → queue +1, visible within 2 min
- TC-04: Staff removes patient → queue -1, visible within 2 min
- TC-05: Urgent priority recalculates order and wait times within 2 min
- TC-06: Smartphone access displays correctly, readable without horizontal scroll
- TC-07: Tablet/desktop access works fully
- TC-08: Wait-time accuracy validation (80% within ±10 minutes)

Edge Cases (EC-01 to EC-06):
- EC-01: Clinic closed → display "Clinic Closed", no queue estimates
- EC-02: Empty queue → display length=0, wait time=0 min
- EC-03: Zero wait time → display "No Waiting" or "0 Minutes"
- EC-04: Service unavailable → user-friendly error, log issue
- EC-05: Remove non-existent patient → reject, error message, preserve queue
- EC-06: Concurrent staff updates → maintain accuracy, no duplicates/loss

CONSTRAINTS:
- Simple, accessible design (no unnecessary technical complexity)
- Minimize implementation cost and maintenance burden
- Support future expansion (online queue joining, SMS notifications, appointment booking)
- Queue updates must be reliable and near-real-time
- Patient data privacy: no PII displayed in patient portal
- Staff authentication required; audit log staff changes
- System uptime: 99% during operating hours
- Staff should complete queue updates in <2 minutes per transaction
```

---

## TECHNOLOGY STACK FOR FIRST VERSION (SIMPLIFIED MVP)

### Frontend (Patient Portal & Staff Portal)
- **Language**: HTML5 + CSS3 + JavaScript (vanilla, no frameworks)
- **Styling**: Inline CSS or simple CSS file (mobile-responsive)
- **HTTP Client**: Fetch API
- **Package Manager**: None required (pure HTML/CSS/JS, no npm install)

### Backend (Queue Management Service)
- **Language**: Node.js with Express OR Python with Flask (pure, minimal dependencies)
- **API Format**: REST API endpoints only
- **Dependencies**: Minimal — Express/Flask only, no external libraries

### Data Storage
- **Option 1**: JSON files (simplest, no database setup needed)
  - `queue.json` — current queue state
  - `consultations.json` — history for calculating avg duration
  - `audit_log.json` — staff actions
  - `clinic_settings.json` — clinic hours, staff passwords
- **Option 2**: SQLite (included with Python/Node; no external DB required)
  - Single file: `clinic.db`
  - Same tables as above, but in a lightweight database
- **Data Retention**: Keep all data in first version (no purging yet)

### Real-Time Updates
- **Method**: Polling (Patient Portal refreshes every 15 seconds via setInterval)
- **Staff Portal**: Polling every 10 seconds for queue updates

### Deployment
- **Local Development**: Run backend on `localhost:3000` or `localhost:5000`
- **Production**: Deploy to free tier (Heroku, Replit, Vercel, or Railway)
- **No configuration files needed**: Use hardcoded defaults

### Authentication & Security
- **Staff Portal**: Simple username/password in JSON or hardcoded (not production-grade)
- **Patient Portal**: No authentication (open access)
- **Data Storage**: Plain JSON/SQLite (no encryption for MVP)
- **Input Validation**: Basic server-side validation only

---

## IMPLEMENTATION INSTRUCTIONS FOR AI BUILD

### Quick Start (Single Pass Build)
This prompt is designed for AI to build in one pass. Provide this prompt to an AI code generator with these instructions:

**"Build the Clinic Wait Time System using:**
- **Backend**: Node.js + Express (or Python + Flask)
- **Frontend**: HTML5 + vanilla JavaScript
- **Data Storage**: JSON files (or SQLite)
- **No dependencies beyond the framework**
- **No configuration required — hardcoded defaults**

---

### Phase 1: Backend Structure (AI Builds)
1. Create `server.js` or `app.py` with Express/Flask
2. Create data files/database:
   - `queue.json` or `clinic.db` (current queue entries)
   - `consultations.json` or database table (history for avg calculation)
   - `audit_log.json` or database table (staff actions)
   - `clinic_settings.json` or database table (clinic hours, staff credentials)
3. Implement Queue Management API:
   - `GET /api/queue` → returns queue length, estimated wait time, clinic status
   - `POST /api/queue/add` → add patient (staff auth required)
   - `DELETE /api/queue/:patient_id` → remove patient (immutable)
   - `PATCH /api/queue/:patient_id` → mark urgent (move to front, -15 min)
   - `POST /api/auth/login` → staff login (returns session token)
4. Implement wait-time calculation:
   - Load last 20 consultations
   - Calculate average duration
   - Formula: `Estimated Wait = (Avg Duration × Queue Length) + Priority Adjustment`
   - Urgent patients: subtract 15 minutes
5. Implement clinic hours checking (return open/closed status)
6. Add basic audit logging (action, staff, timestamp, patient)

### Phase 2: Patient Portal (AI Builds)
1. Create `patient.html`:
   - Clinic name header
   - Queue length (large, bold: 36px+)
   - Estimated wait time (large, highlighted)
   - Last updated time
   - Clinic closed message (if applicable)
   - Simple CSS (mobile-responsive, no framework)
2. Implement JavaScript:
   - Fetch `/api/queue` on page load
   - Polling: refresh every 15 seconds
   - Show "Connection Error" if API unavailable
   - Responsive layout (works on mobile/tablet/desktop without scrolling)
3. Accessibility:
   - Font size minimum 18px
   - High contrast (black text on white background)
   - No animations or flashing
   - Touch-friendly buttons

### Phase 3: Staff Portal (AI Builds)
1. Create `staff.html`:
   - Login form (username/password)
   - Queue display table (patient name, check-in time, wait time)
   - Buttons: "Add Patient", "Remove Patient", "Mark Urgent"
   - Clinic open/closed status indicator
   - Simple CSS (no framework)
2. Implement JavaScript:
   - Login flow (POST to `/api/auth/login`, store token in session)
   - Fetch `/api/queue` on load, polling every 10 seconds
   - Forms: add patient (name + registration), remove/urgent actions with confirm dialogs
   - Display audit log (last 10 actions visible)
   - Logout button
3. Features:
   - Single "Staff" role (all permissions the same)
   - All actions logged to audit trail
   - Confirmation before remove/urgent actions
   - Polling updates queue display in real-time

### Phase 4: Testing (Manual, No Test Framework)
1. Test all acceptance criteria manually:
   - TC-01: Patient views queue length within 5 sec ✓
   - TC-02: Estimated wait time displays and updates ✓
   - TC-03: Staff adds patient, visible within 2 min ✓
   - TC-04: Staff removes patient, visible within 2 min ✓
   - TC-05: Urgent recalculates and updates within 2 min ✓
   - TC-06: Mobile access (iPhone/Android) displays correctly ✓
   - TC-07: Tablet/desktop works fully ✓
   - TC-08: Wait-time accuracy check (at least 80% within ±10 min) ✓
2. Test edge cases:
   - EC-01: Clinic closed → shows "Clinic Closed" ✓
   - EC-02: Empty queue → shows "0 Minutes" ✓
   - EC-03: Zero wait time → shows "No Waiting" ✓
   - EC-04: API unavailable → shows "Connection Error" ✓
   - EC-05: Remove non-existent patient → error message ✓
   - EC-06: Concurrent updates → no duplicates/data loss ✓
3. Browser testing: Chrome, Safari, Firefox (mobile + desktop)
4. Performance: Patient portal loads <5 sec, queue updates <2 min

### No Phase 5 or 6 for MVP
- Skip deployment complexity
- Skip documentation (code is self-explanatory)
- Run locally on `localhost:3000` or `localhost:5000` for testing

---

## TESTING STRATEGY FOR FIRST VERSION

### Manual Testing (No Test Framework)
Follow the acceptance criteria and edge cases exactly as written:

**Acceptance Tests (TC-01 to TC-08):**
1. Open patient portal in browser → queue length appears within 5 sec
2. Queue updates → estimated wait time refreshes automatically
3. Add patient via staff portal → queue length increases by 1, visible within 2 min
4. Remove patient via staff portal → queue length decreases by 1, visible within 2 min
5. Mark patient urgent → moves to front of queue, estimate reduced by 15 min, recalculated within 2 min
6. Open patient portal on smartphone → displays correctly, no horizontal scrolling
7. Open patient portal on tablet/desktop → full functionality works
8. Watch wait times → at least 80% of estimates are within ±10 minutes of actual wait

**Edge Case Tests (EC-01 to EC-06):**
1. Set clinic as "closed" → displays "Clinic Closed" message, no queue shown
2. Remove all patients → queue length shows 0, wait time shows "No Waiting"
3. Queue length is 1 patient → estimated wait time shows "0 Minutes" or "< 1 minute"
4. Disconnect backend server → patient portal shows "Connection Error", retry after 10 sec
5. Try to remove same patient twice → 2nd attempt shows error, queue data unchanged
6. Have two staff add/remove simultaneously → verify no duplicates or data corruption

### Browser & Device Testing
- Test on Chrome, Safari, Firefox (at least one mobile, one desktop per browser)
- Verify mobile layout (no horizontal scroll, readable text)
- Verify button clicks work on touch devices

### Performance Checks
- Patient portal load: measure <5 seconds
- Queue updates: measure <2 minutes visible to patient after staff action
- Concurrent staff: stress test with 5+ staff removing patients simultaneously

### Code Quality Check (Manual)
- No console errors or warnings
- API responses are valid JSON
- Staff authentication works (logout clears session)
- No hardcoded URLs with sensitive data

---

## DESIGN DECISIONS - CONFIRMED FOR TEST PROJECT

### 1. Wait-Time Calculation Accuracy ✅
- **Decision**: Include all queue members in calculation; adjust estimates for urgent patients separately
- **Formula**: `Estimated Wait = (Avg Consultation Duration × Current Queue Length) + Priority Adjustment`
- **Lookback Period**: Last 20 completed visits (rolling average, recalculated hourly)
- **Urgent Adjustment**: Subtract 15 minutes from urgent patient's estimate
- **Zero Queue**: Display "No Waiting" or "0 Minutes"

### 2. Patient Identification & Access ✅
- **Decision**: Completely anonymous—no authentication required
- **Access Method**: Static clinic-provided URL (e.g., `clinic.com/queue/ABC123`)
- **Patient Portal**: Shows only queue length and wait time, never patient names or positions
- **Future**: Clinic registration number support for queue position tracking (Phase 2+)

### 3. Clinic Hours & Closed Status ✅
- **Decision**: Admin-configurable schedule via staff settings panel
- **When Closed**: Display "Clinic Closed" message, hide queue data, show reopening time
- **Data Privacy**: Do not show historical wait times when closed
- **Emergency Override**: Not required for MVP

### 4. Urgent/Priority Cases ✅
- **Decision**: Any staff member can mark patient urgent; urgent patients move to queue front
- **Queue Position**: Urgent patients prioritized first (front of queue)
- **Wait-Time Impact**: Urgent patient sees -15 min reduced estimate; other patients recalculated
- **Implementation**: Flag `priority = 'urgent'` on queue_entry record

### 5. Staff Roles & Permissions ✅
- **Decision**: Single generic "Staff" role for MVP (all staff have identical permissions)
- **Future Roles**: Can add doctor/receptionist/admin roles in Phase 2+
- **Audit Trail**: Yes—every action logged with staff ID, timestamp, action type, affected patient
- **Permissions for MVP**: All staff can add, remove, prioritize patients

### 6. Data Retention & Privacy ✅
- **Decision**: Keep all data (no purging for MVP)
- **Privacy**: Patient names visible in staff portal only; never in patient portal
- **Encryption**: Not required for MVP (plain JSON/SQLite)
- **Future**: HTTPS and encryption added in production version

### 7. Concurrent Update Conflicts ✅
- **Decision**: Use database transaction locking to prevent duplicate removes
- **Queue Entry States**: Once removed, entry cannot be re-removed (immutable)
- **Rejoin Support**: Patient can be re-added as new queue entry if removed
- **Conflict Handling**: Database constraints prevent orphaned/duplicate records

### 8. Mobile & Offline Capability ✅
- **Decision**: Internet required for both patient and staff portals (MVP simplicity)
- **Graceful Degradation**: Show "Connection Error" message if API unavailable, retry after 10 sec
- **Offline Mode**: Not required for MVP; design APIs for future offline support

### 9. Monitoring & Alerting ✅
- **Decision**: Not required for MVP (run locally on localhost)
- **Error Logging**: Log errors to server console only
- **Future**: Monitoring/alerting added in production version
- **Status Check**: Manual check via browser (reload page)

### 10. Future Features Scope ✅
- **Decision**: Design API to support future features; don't implement them in MVP
- **API-Ready For**: SMS notifications, appointment booking, online queue joining
- **Implementation**: Add these features after core system tested and deployed
- **Data Structure**: Queue tables designed to store patient contact info (phone, email) for future use

---

## DELIVERABLES CHECKLIST FOR MVP

**Code:**
- [ ] Backend server (Express or Flask)
- [ ] Patient Portal (`patient.html` + JavaScript)
- [ ] Staff Portal (`staff.html` + JavaScript)
- [ ] Data files (`queue.json`, `consultations.json`, `clinic_settings.json`, `audit_log.json`) OR SQLite database
- [ ] API endpoints (all 5 endpoints working)

**Tests (Manual):**
- [ ] All acceptance criteria pass (TC-01 to TC-08)
- [ ] All edge cases pass (EC-01 to EC-06)
- [ ] Mobile responsiveness check
- [ ] Browser compatibility (Chrome, Safari, Firefox)
- [ ] Performance check (<5 sec patient load, <2 min updates)

**No Deliverables Needed:**
- ❌ Unit/integration/E2E test files
- ❌ Database migrations
- ❌ Configuration files (.env)
- ❌ Deployment setup
- ❌ Documentation
- ❌ CI/CD pipeline

---

## Success Criteria Summary (MVP)

✅ **Patients**: View queue length and wait time within 5 seconds  
✅ **Staff**: Add/remove/prioritize patients in <2 minutes per action  
✅ **System**: Updates visible within 2 minutes, 80%+ wait-time accuracy (±10 min)  
✅ **Accessibility**: Works on smartphone/tablet/desktop  
✅ **Data**: All actions logged to audit trail  
✅ **Privacy**: Patient names hidden from patient portal  
✅ **Simplicity**: No installation, configuration, or external dependencies (except Node/Python)  

---

## Ready to Build

This prompt is optimized for AI code generation in one pass. All requirements are:
- ✅ Clear and unambiguous
- ✅ Simplified for MVP
- ✅ No deployment complexity
- ✅ No configuration required
- ✅ JSON or SQLite only
- ✅ Manual testing only

**Next Step**: Provide this prompt to an AI code generator with the building instructions above. The AI should produce a working system in a single code generation pass.
