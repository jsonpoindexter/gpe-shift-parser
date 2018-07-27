const csvFilePath = './2018 - I, Robot-2018-07-27.csv'; // TODO: Fetch this directly from babalooey
const csv = require('csvtojson');

const mainEventStart = new Date('2018-08-23 00:00'); // TODO: Set this to the actual prevent date

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

function filterForWap(shifts) {
    groupBy(shifts, "User ID").forEach((userShifts) => {
        const preEventShifts = userShifts.filter(shift =>
            new Date(shift['Shift Start']) <= mainEventStart &&
            shift['Full Name'].trim().length > 0 &&
            shift['Full Name'] === 'Jason Poindexter');
        if(preEventShifts.length > 0) { console.log(preEventShifts) }
    })
}



csv()
    .fromFile(csvFilePath)
    .then((shifts)=>{
       filterForWap(shifts)
    });
