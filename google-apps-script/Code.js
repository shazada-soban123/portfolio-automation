/**
 * Google Apps Script for Portfolio Automation
 *
 * SETUP INSTRUCTIONS:
 * 1. Open your Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Replace the default code with this code
 * 4. Save the project
 * 5. Set up a trigger: Edit > Triggers > Add Trigger
 *    - Choose: "triggerOnNewRow"
 *    - Event source: "From spreadsheet"
 *    - Event type: "On change"
 * 6. Deploy as web app if using URL fetch
 */

// Configuration
const WEBHOOK_URL = 'YOUR_WEBHOOK_URL_HERE'; // Your deployed API endpoint
const SHEET_NAME = 'Sheet1'; // Change if your sheet has a different name

/**
 * Main function called when spreadsheet changes
 * Detects new rows and sends data to webhook
 */
function triggerOnNewRow(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const lastRow = sheet.getLastRow();

  // Get the headers (row 1)
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

  // Get the latest row data (new entry)
  const rowData = sheet.getRange(lastRow, 1, 1, sheet.getLastColumn()).getValues()[0];

  // Convert to object
  const data = {};
  headers.forEach((header, index) => {
    data[header] = rowData[index];
  });

  // Validate required fields
  if (!data['Full Name'] || !data['Email']) {
    Logger.log('Missing required fields: Full Name or Email');
    return;
  }

  // Check if this is a new entry (has email)
  if (data['Email']) {
    Logger.log('New portfolio request: ' + data['Full Name']);

    // Send to webhook
    sendToWebhook(data);

    // Add timestamp
    sheet.getRange(lastRow, headers.length + 1).setValue(new Date());
    sheet.getRange(lastRow, headers.length + 2).setValue('Processing');
  }
}

/**
 * Send data to the webhook endpoint
 */
function sendToWebhook(data) {
  const payload = {
    'full_name': data['Full Name'] || '',
    'email': data['Email'] || '',
    'niche': data['Niche'] || '',
    'services': data['Services'] || '',
    'target_clients': data['Target Clients'] || '',
    'work_samples': data['Work Samples'] || '',
    'testimonials': data['Testimonials'] || '',
    'brand_colors': data['Brand Colors'] || '',
    'preferred_style': data['Preferred Style'] || '',
    'cta': data['CTA'] || 'Hire Me'
  };

  const options = {
    'method': 'POST',
    'contentType': 'application/json',
    'payload': JSON.stringify(payload)
  };

  try {
    const response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    const responseCode = response.getResponseCode();

    if (responseCode === 200) {
      Logger.log('Successfully sent to webhook');
      updateStatus(data['Email'], 'Website Generated');
    } else {
      Logger.log('Webhook returned status: ' + responseCode);
      updateStatus(data['Email'], 'Error: HTTP ' + responseCode);
    }
  } catch (error) {
    Logger.log('Error sending to webhook: ' + error.toString());
    updateStatus(data['Email'], 'Error: ' + error.toString());
  }
}

/**
 * Update status in the spreadsheet
 */
function updateStatus(email, status) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    if (data[i][1] === email) { // Email is column B (index 1)
      sheet.getRange(i + 1, 12).setValue(status); // Column L
      break;
    }
  }
}

/**
 * Manual trigger function - use this to test
 */
function testWebhook() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const lastRow = sheet.getLastRow();

  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const rowData = sheet.getRange(lastRow, 1, 1, sheet.getLastColumn()).getValues()[0];

  const data = {};
  headers.forEach((header, index) => {
    data[header] = rowData[index];
  });

  Logger.log('Testing with data: ' + JSON.stringify(data));
  sendToWebhook(data);
}

/**
 * DoGet - Required for web app deployment
 */
function doGet(e) {
  return HtmlService.createHtmlOutput('<h1>Portfolio Automation API</h1><p>Status: Active</p>');
}

/**
 * DoPost - Handle POST requests if deployed as web app
 */
function doPost(e) {
  const data = JSON.parse(e.postData.contents);

  // Process the incoming data
  Logger.log('Received data: ' + JSON.stringify(data));

  return HtmlService.createHtmlOutput('OK');
}

/**
 * Create custom menu in spreadsheet
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Portfolio Automation')
    .addItem('Test Webhook', 'testWebhook')
    .addItem('Process Last Row', 'triggerOnNewRow')
    .addSeparator()
    .addItem('View Logs', 'showLogs')
    .addToUi();
}

/**
 * Show recent logs
 */
function showLogs() {
  const logs = Logger.getLog();
  Logger.log('=== Recent Logs ===');
  Logger.log(logs);
  SpreadsheetApp.getUi().alert('Logs', logs.slice(-2000), SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Set up time-driven trigger to check for new rows periodically
 * Run this function once to enable periodic checking
 */
function setupTimeDrivenTrigger() {
  // Create a trigger that runs every 5 minutes
  ScriptApp.newTrigger('checkForNewRows')
    .timeBased()
    .everyMinutes(5)
    .create();
}

/**
 * Check for new rows using time-based trigger
 * This is an alternative to the on change trigger
 */
function checkForNewRows() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const lastRow = sheet.getLastRow();
  const lastProcessedRow = PropertiesService.getScriptProperties().getProperty('lastProcessedRow') || 1;

  if (lastRow > lastProcessedRow) {
    // Process new rows
    for (let i = parseInt(lastProcessedRow) + 1; i <= lastRow; i++) {
      const rowData = sheet.getRange(i, 1, 1, sheet.getLastColumn()).getValues()[0];
      const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

      const data = {};
      headers.forEach((header, index) => {
        data[header] = rowData[index];
      });

      if (data['Email']) {
        sendToWebhook(data);
      }
    }

    PropertiesService.getScriptProperties().setProperty('lastProcessedRow', lastRow.toString());
  }
}

/**
 * Initialize - Set up the sheet with status columns
 */
function initializeSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);

  // Add Status column header if not exists
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  if (!headers.includes('Status')) {
    sheet.getRange(1, headers.length + 1).setValue('Status');
    sheet.getRange(1, headers.length + 2).setValue('Website URL');
    sheet.getRange(1, headers.length + 3).setValue('Timestamp');
  }

  Logger.log('Sheet initialized successfully');
}
