const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(__dirname));

const dataDir = __dirname;
const queueFile = path.join(dataDir, 'queue.json');
const consultationsFile = path.join(dataDir, 'consultations.json');
const settingsFile = path.join(dataDir, 'clinic_settings.json');
const auditFile = path.join(dataDir, 'audit_log.json');

// Helper functions to read/write JSON files
function readQueue() {
  try {
    const data = fs.readFileSync(queueFile, 'utf8');
    return JSON.parse(data).queue;
  } catch {
    return [];
  }
}

function writeQueue(queue) {
  fs.writeFileSync(queueFile, JSON.stringify({ queue }, null, 2));
}

function readConsultations() {
  try {
    const data = fs.readFileSync(consultationsFile, 'utf8');
    return JSON.parse(data).consultations;
  } catch {
    return [];
  }
}

function writeConsultations(consultations) {
  fs.writeFileSync(consultationsFile, JSON.stringify({ consultations }, null, 2));
}

function readSettings() {
  try {
    const data = fs.readFileSync(settingsFile, 'utf8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

function readAuditLog() {
  try {
    const data = fs.readFileSync(auditFile, 'utf8');
    return JSON.parse(data).logs || [];
  } catch {
    return [];
  }
}

function writeAuditLog(logs) {
  fs.writeFileSync(auditFile, JSON.stringify({ logs }, null, 2));
}

function addAuditLog(staff, action, patientId, details = {}) {
  const logs = readAuditLog();
  logs.push({
    timestamp: new Date().toISOString(),
    staff: staff,
    action: action,
    patient_id: patientId,
    details: details
  });
  writeAuditLog(logs);
}

function calculateAverageConsultationDuration() {
  const consultations = readConsultations();
  if (consultations.length === 0) return 12;

  const last20 = consultations.slice(-20);
  const total = last20.reduce((sum, c) => sum + (c.duration_minutes || 0), 0);
  return Math.round(total / last20.length);
}

function calculateEstimatedWaitTime(queueLength, avgDuration, isUrgent = false) {
  const waitMinutes = avgDuration * queueLength;
  if (isUrgent) {
    return Math.max(0, waitMinutes - 15);
  }
  return waitMinutes;
}

function isClinicOpen() {
  const settings = readSettings();
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const currentTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

  const openTime = settings.open_time || '09:00';
  const closeTime = settings.close_time || '17:00';

  return currentTime >= openTime && currentTime < closeTime;
}

// API: Get queue information (Patient Portal)
app.get('/api/queue', (req, res) => {
  const queue = readQueue();
  const avgDuration = calculateAverageConsultationDuration();
  const clinicOpen = isClinicOpen();

  if (!clinicOpen) {
    return res.json({
      queue_length: 0,
      estimated_wait_time: 0,
      clinic_status: 'closed',
      message: 'Clinic is currently closed'
    });
  }

  // Count non-urgent patients for wait time calculation
  const normalPatients = queue.filter(p => p.priority !== 'urgent').length;
  const estimatedWait = calculateEstimatedWaitTime(normalPatients, avgDuration, false);

  res.json({
    queue_length: queue.length,
    estimated_wait_time: estimatedWait,
    clinic_status: 'open',
    timestamp: new Date().toISOString()
  });
});

// API: Staff login
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  const settings = readSettings();

  const staff = settings.staff.find(s => s.username === username && s.password === password);

  if (staff) {
    res.json({
      success: true,
      token: Buffer.from(username).toString('base64'),
      username: username
    });
  } else {
    res.status(401).json({ success: false, error: 'Invalid credentials' });
  }
});

// Middleware: Verify staff token
function verifyStaff(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const username = Buffer.from(token, 'base64').toString('utf8');
    const settings = readSettings();
    if (!settings.staff.find(s => s.username === username)) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    req.staff = username;
    next();
  } catch {
    res.status(401).json({ error: 'Unauthorized' });
  }
}

// API: Get queue with details (Staff Portal)
app.get('/api/staff/queue', verifyStaff, (req, res) => {
  const queue = readQueue();
  const avgDuration = calculateAverageConsultationDuration();
  const clinicOpen = isClinicOpen();

  const queueWithWaitTimes = queue.map((patient, index) => {
    const patientsAhead = queue.slice(0, index).filter(p => p.priority !== 'urgent').length;
    const waitTime = calculateEstimatedWaitTime(patientsAhead, avgDuration, patient.priority === 'urgent');
    return {
      ...patient,
      position: index + 1,
      estimated_wait: waitTime
    };
  });

  res.json({
    queue: queueWithWaitTimes,
    clinic_open: clinicOpen,
    avg_consultation_duration: avgDuration,
    total_patients: queue.length
  });
});

// API: Add patient to queue
app.post('/api/queue/add', verifyStaff, (req, res) => {
  const { name, registration_number } = req.body;

  if (!name || !registration_number) {
    return res.status(400).json({ error: 'Name and registration number required' });
  }

  const queue = readQueue();
  const newPatient = {
    id: Date.now(),
    name: name,
    registration: registration_number,
    added_at: new Date().toISOString(),
    priority: 'normal'
  };

  queue.push(newPatient);
  writeQueue(queue);
  addAuditLog(req.staff, 'add', newPatient.id, { name, registration_number });

  res.json({ success: true, patient: newPatient });
});

// API: Remove patient from queue
app.delete('/api/queue/:patient_id', verifyStaff, (req, res) => {
  const patientId = parseInt(req.params.patient_id);
  const queue = readQueue();

  const patientIndex = queue.findIndex(p => p.id === patientId);
  if (patientIndex === -1) {
    return res.status(404).json({ error: 'Patient not found in queue' });
  }

  const removedPatient = queue[patientIndex];
  queue.splice(patientIndex, 1);
  writeQueue(queue);
  addAuditLog(req.staff, 'remove', patientId, { name: removedPatient.name });

  // Add to consultations history (simulate consultation completed)
  const consultations = readConsultations();
  consultations.push({
    patient_id: patientId,
    duration_minutes: calculateAverageConsultationDuration(),
    completed_at: new Date().toISOString()
  });
  writeConsultations(consultations);

  res.json({ success: true, message: 'Patient removed from queue' });
});

// API: Mark patient as urgent
app.patch('/api/queue/:patient_id', verifyStaff, (req, res) => {
  const patientId = parseInt(req.params.patient_id);
  const queue = readQueue();

  const patientIndex = queue.findIndex(p => p.id === patientId);
  if (patientIndex === -1) {
    return res.status(404).json({ error: 'Patient not found in queue' });
  }

  const patient = queue[patientIndex];
  queue.splice(patientIndex, 1);
  patient.priority = 'urgent';
  queue.unshift(patient); // Move to front
  writeQueue(queue);
  addAuditLog(req.staff, 'mark_urgent', patientId, { name: patient.name });

  res.json({ success: true, message: 'Patient marked as urgent and moved to front' });
});

// API: Get audit log (Staff Portal)
app.get('/api/staff/audit-log', verifyStaff, (req, res) => {
  const logs = readAuditLog();
  const recentLogs = logs.slice(-10).reverse();
  res.json({ logs: recentLogs });
});

// Serve patient portal
app.get('/patient', (req, res) => {
  res.sendFile(path.join(__dirname, 'patient.html'));
});

// Serve staff portal
app.get('/staff', (req, res) => {
  res.sendFile(path.join(__dirname, 'staff.html'));
});

app.listen(PORT, () => {
  console.log(`\n🏥 Clinic Wait Time System running on http://localhost:${PORT}`);
  console.log(`📋 Patient Portal: http://localhost:${PORT}/patient`);
  console.log(`👨‍⚕️ Staff Portal: http://localhost:${PORT}/staff`);
  console.log(`\n📝 Staff credentials:`);
  console.log(`   Username: staff1  Password: demo123`);
  console.log(`   Username: staff2  Password: demo123\n`);
});
