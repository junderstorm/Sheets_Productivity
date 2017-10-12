// Replace the variables in this block with real values.
var address = '';
var user = '';
var userPwd = '';
var db = '';

var dbUrl = 'jdbc:mysql://' + address + '/' + db;

function downloadData() {
  
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('tab_updates');
  var i  = 2;
  var myQuery = '';
  var targetSheet = '';
  var startCol  =1;
  while (sheet.getRange(i,1).getValue()!='') {
    if(sheet.getRange(i,4).getValue()) {
      targetSheet = sheet.getRange(i,1).getValue();
      myQuery = sheet.getRange(i,2).getValue();
      startCol  = sheet.getRange(i,3).getValue();
      readFromTable(myQuery,targetSheet,startCol);
      sheet.getRange(i,5).setValue("Done!");
    }
    i++;
  }
  Browser.msgBox("Download complete");
}

function readFromTable(myQuery, mySheetName, colStart) {
  var conn = Jdbc.getConnection(dbUrl, user, userPwd);

  var start = new Date();
  var stmt = conn.createStatement();
  Logger.log("QUERY:" + myQuery);
  var results = stmt.executeQuery(myQuery);
  var numCols = results.getMetaData().getColumnCount();
  var headers = results.getMetaData();

  results.last();
  var recordCount = results.getRow();

  
  var myRows = new  Array(recordCount);
  myRows[0] = new Array(numCols);
  for (var col = 0; col< numCols; col++) {
    myRows[0][col]=headers.getColumnName(col+1);
  }
  
  //Get the sheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(mySheetName);
  
  if (recordCount>0) {
    currentRow = 1;
    results.first();
    do {
      myRows[currentRow] = new Array(numCols);
      for (var col = 0; col < numCols; col++) {
        myRows[currentRow][col] = results.getString(col + 1); 
      }
      currentRow++;
    } while (results.next());
  }
  
  sheet.getRange(1,colStart,sheet.getMaxRows(),numCols).clear();
  sheet.getRange(1, colStart, recordCount+1, numCols).setValues(myRows);
  results.close();
  stmt.close();
  
  var end = new Date();
  Logger.log('Time elapsed: %sms', end - start);
  conn.close();
}
