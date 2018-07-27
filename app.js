const csvFilePath = './2018 - I, Robot-2018-07-27.csv'; //TODO Fetch this directly from babalooey
const csv = require('csvtojson');

function groupBy(collection, property) {
    var i = 0, val, index,
        values = [], result = [];
    for (; i < collection.length; i++) {
        val = collection[i][property];
        index = values.indexOf(val);
        if (index > -1)
            result[index].push(collection[i]);
        else {
            values.push(val);
            result.push([collection[i]]);
        }
    }
    return result;
}

csv()
    .fromFile(csvFilePath)
    .then((shifts)=>{
        const shift = shifts[0]
        // console.log(shift[])
        console.log(groupBy(shifts, "User ID")[0]);
    });
