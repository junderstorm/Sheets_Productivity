/**
 * Returns a single list of paren-enclosed, comma delimmited IDs 
 * Arg1 = list of elements to concatenate
 * Arg2 (optional) = 1 if you want to add single parans around each element, otherwise leave blank
 *
 * @Array {string} formatted like MM/DD/YYYY 
 * @customfunction
 */
function concatstringy(myArray,inty) {
  var stringy = ''
  if (inty == 1) {
  for (var i = 0; i<myArray.length; i++) {
       if (i !== myArray.length-1) {
      stringy += "'"+myArray[i]+"',"
    }
       else {
      stringy += "'"+myArray[i]+"'"
    }
  }
   return stringy;  
  }
    else {
     for (var i = 0; i<myArray.length; i++) {
        if (i !== myArray.length-1) {
            stringy += myArray[i]+','
    }
        else {
            stringy += myArray[i]
    }
  }
   return stringy;   
    }
}
