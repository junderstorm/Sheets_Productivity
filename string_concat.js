/**
 * Returns a single list of paren-enclosed, comma delimmited IDs 
 * Enter 1 as the second arg if you want to add single quotations to each element
 * Leave arg 2 blank if you want the elements unchanged, just concatenated as they are
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
