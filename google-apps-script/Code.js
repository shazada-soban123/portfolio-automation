/**
 * Google Apps Script for Portfolio Automation
 *
 * SETUP INSTRUCTIONS:
 * 1. Open your Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Replace the default code with this code
 * 4. Save the project
 * 5. Run initializeSheet() once to set up columns
 * 6. Set up a trigger: Edit > Triggers > Add Trigger
 *    - Choose: "triggerOnNewRow"
 *    - Event source: "From spreadsheet"
 *    - Event type: "On change"
 */

// Configuration
const WEBHOOK_URL = 'YOUR_WEBHOOK_URL_HERE'; // Your deployed API endpoint (e.g., https://portfolio-automation.up.railway.app/webhook)
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

  // Find column indices
  const fullNameCol = headers.indexOf('Full Name') + 1;
  const emailCol = headers.indexOf('Email') + 1;
  const statusCol = headers.indexOf('Status') + 1 || findOrCreateColumn(sheet, headers, 'Status');
  const websiteCol = headers.indexOf('Website URL') + 1 || findOrCreateColumn(sheet, headers, 'Website URL');
  const timestampCol = headers.indexOf('Timestamp') + 1 || findOrCreateColumn(sheet, headers, 'Timestamp');

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

  // Check if this is a new entry (has email and no status yet)
  if (data['Email'] && !data['Status']) {
    Logger.log('New portfolio request: ' + data['Full Name']);

    // Update status to Processing
    sheet.getRange(lastRow, statusCol).setValue('Processing...');
    sheet.getRange(lastRow, timestampCol).setValue(new Date());

    // Send to webhook and get response
    const result = sendToWebhook(data, lastRow, emailCol, statusCol, websiteCol);
  }
}

/**
 * Find or create a column with the given name
 */
function findOrCreateColumn(sheet, headers, columnName) {
  const existingIndex = headers.indexOf(columnName);
  if (existingIndex !== -1) {
    return existingIndex + 1;
  }
  // Create new column
  const newCol = headers.length + 1;
  sheet.getRange(1, newCol).setValue(columnName);
  return newCol;
}

/**
 * Send data to the webhook endpoint and update sheet with result
 */
function sendToWebhook(data, rowNum, emailCol, statusCol, websiteCol) {
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
    'payload': JSON.stringify(payload),
    'muteHttpExceptions': true
  };

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);

  try {
    Logger.log('Sending request to webhook: ' + WEBHOOK_URL);
    const response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();

    Logger.log('Response code: ' + responseCode);
    Logger.log('Response: ' + responseText);

    if (responseCode === 200) {
      const result = JSON.parse(responseText);

      if (result.success) {
        // Update sheet with website URL
        const websiteUrl = result.website_url || result.repo_url;
        sheet.getRange(rowNum, websiteCol).setValue(websiteUrl);
        sheet.getRange(rowNum, websiteCol).setFormula('=HYPERLINK("' + websiteUrl + '", "View Website")');

        // Update status
        sheet.getRange(rowNum, statusCol).setValue('✓ Live');

        // Also add repo URL if different
        if (result.repo_url && result.repo_url !== websiteUrl) {
          sheet.getRange(rowNum, websiteCol + 1).setFormula('=HYPERLINK("' + result.repo_url + '", "GitHub Repo")');
        }

        Logger.log('SUCCESS! Website URL: ' + websiteUrl);
        return { success: true, website_url: websiteUrl };
      } else {
        sheet.getRange(rowNum, statusCol).setValue('✗ Error: ' + (result.error || 'Unknown error'));
        return { success: false, error: result.error };
      }
    } else {
      sheet.getRange(rowNum, statusCol).setValue('✗ HTTP Error: ' + responseCode);
      return { success: false, error: 'HTTP ' + responseCode };
    }
  } catch (error) {
    Logger.log('Error: ' + error.toString());
    sheet.getRange(rowNum, statusCol).setValue('✗ Error: ' + error.toString());
    return { success: false, error: error.toString() };
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

  const statusCol = headers.indexOf('Status') + 1;
  const websiteCol = headers.indexOf('Website URL') + 1;

  const result = sendToWebhook(data, lastRow, headers.indexOf('Email') + 1, statusCol, websiteCol);
  Logger.log('Test result: ' + JSON.stringify(result));
}

/**
 * DoGet - Required for web app deployment
 */
function doGet(e) {
  return HtmlService.createHtmlOutput(`
    <h1>Portfolio Automation API</h1>
    <p>Status: Active ✓</p>
    <p>Ready to receive portfolio requests!</p>
    <p>Webhook URL: ${WEBHOOK_URL}</p>
  `);
}

/**
 * DoPost - Handle POST requests if deployed as web app
 */
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  Logger.log('Received data: ' + JSON.stringify(data));
  return HtmlService.createHtmlOutput('OK');
}

/**
 * Create custom menu in spreadsheet
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🤖 Portfolio Automation')
    .addItem('⚡ Process Last Row', 'triggerOnNewRow')
    .addItem('🧪 Test Webhook', 'testWebhook')
    .addItem('📊 Initialize Sheet', 'initializeSheet')
    .addSeparator()
    .addItem('📝 View Logs', 'showLogs')
    .addToUi();
}

/**
 * Show recent logs
 */
function showLogs() {
  const logs = Logger.getLog();
  Logger.log('=== Recent Logs ===');
  Logger.log(logs);
  SpreadsheetApp.getUi().alert('Logs', logs.slice(-3000), SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Set up time-driven trigger to check for new rows periodically
 * Run this function once to enable periodic checking
 */
function setupTimeDrivenTrigger() {
  // Delete existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  for (let i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }

  // Create a trigger that runs every 5 minutes
  ScriptApp.newTrigger('checkForNewRows')
    .timeBased()
    .everyMinutes(5)
    .create();

  Logger.log('Time-driven trigger created successfully');
}

/**
 * Check for new rows using time-based trigger
 * This is an alternative to the on change trigger
 */
function checkForNewRows() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const lastRow = sheet.getLastRow();
  const lastProcessedRow = parseInt(PropertiesService.getScriptProperties().getProperty('lastProcessedRow') || '1');

  if (lastRow > lastProcessedRow) {
    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const statusCol = headers.indexOf('Status') + 1;
    const websiteCol = headers.indexOf('Website URL') + 1;
    const emailCol = headers.indexOf('Email') + 1;

    // Process new rows
    for (let i = lastProcessedRow + 1; i <= lastRow; i++) {
      const rowData = sheet.getRange(i, 1, 1, sheet.getLastColumn()).getValues()[0];

      const data = {};
      headers.forEach((header, index) => {
        data[header] = rowData[index];
      });

      if (data['Email'] && !data['Status']) {
        Logger.log('Processing row ' + i + ': ' + data['Full Name']);
        sheet.getRange(i, statusCol).setValue('Processing...');
        sendToWebhook(data, i, emailCol, statusCol, websiteCol);
      }
    }

    PropertiesService.getScriptProperties().setProperty('lastProcessedRow', lastRow.toString());
  }
}

/**
 * Initialize - Set up the sheet with status columns
 * Run this once to add all required columns
 */
function initializeSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);

  // Get existing headers
  let headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

  // Check and add columns if missing
  if (!headers.includes('Status')) {
    sheet.getRange(1, headers.length + 1).setValue('Status');
    headers.push('Status');
  }

  if (!headers.includes('Website URL')) {
    sheet.getRange(1, headers.length + 1).setValue('Website URL');
    headers.push('Website URL');
  }

  if (!headers.includes('Timestamp')) {
    sheet.getRange(1, headers.length + 1).setValue('Timestamp');
    headers.push('Timestamp');
  }

  // Format the headers
  const lastCol = headers.length;
  sheet.getRange(1, 1, 1, lastCol).setFontWeight('bold');
  sheet.getRange(1, 1, 1, lastCol).setBackground('#f3f4f6');

  // Set column widths
  sheet.setColumnWidth(headers.indexOf('Full Name') + 1, 150);
  sheet.setColumnWidth(headers.indexOf('Email') + 1, 200);
  sheet.setColumnWidth(headers.indexOf('Status') + 1, 120);
  sheet.setColumnWidth(headers.indexOf('Website URL') + 1, 200);

  Logger.log('Sheet initialized successfully!');
  Logger.log('Columns: ' + headers.join(', '));

  // Show confirmation
  SpreadsheetApp.getUi().alert('✅ Sheet Initialized!',
    'Your sheet now has:\n' +
    '• Status column\n' +
    '• Website URL column\n' +
    '• Timestamp column\n\n' +
    'Webhook URL: ' + WEBHOOK_URL,
    SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Update webhook URL
 */
function setWebhookUrl() {
  const ui = SpreadsheetApp.getUi();
  const result = ui.prompt(
    'Set Webhook URL',
    'Enter your deployed API endpoint URL:',
    ui.ButtonSet.OK_CANCEL
  );

  if (result.getSelectedButton() === ui.Button.OK) {
    const url = result.getResponseText().trim();
    if (url) {
      // This would need to be saved to ScriptProperties in production
      ui.alert('Webhook URL set to: ' + url + '\n\nPlease update the WEBHOOK_URL constant in the script code for this to persist.');
    }
  }
}
