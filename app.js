const csvFilePath='./2018 - I, Robot-2018-07-27.csv'; //TODO Fetch this directly from babalooey
const csv=require('csvtojson');
csv()
    .fromFile(csvFilePath)
    .then((jsonObj)=>{
        console.log(jsonObj);
    });
