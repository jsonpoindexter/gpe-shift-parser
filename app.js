/* ----- outputs array of csv cells ---- */
// const fs = require('fs');
// const parse = require('csv-parse');

// function groupBy(collection, property) {
//     var i = 0, val, index,
//         values = [], result = [];
//     for (; i < collection.length; i++) {
//         val = collection[i][property];
//         index = values.indexOf(val);
//         if (index > -1)
//             result[index].push(collection[i]);
//         else {
//             values.push(val);
//             result.push([collection[i]]);
//         }
//     }
//     return result;
// }
//
// const parser = parse({relax_column_count: true}, function (err, shifts) {
//     if(err){
//         console.log(err);
//     }
//     console.log(shifts);
// });
//
// fs.createReadStream(__dirname+'/2018 - I, Robot-2018-07-27.csv').pipe(parser);


const csvFilePath='./2018 - I, Robot-2018-07-27.csv'; //TODO Fetch this directly from babalooey
const csv=require('csvtojson');
csv()
    .fromFile(csvFilePath)
    .then((jsonObj)=>{
        console.log(jsonObj);
    });
