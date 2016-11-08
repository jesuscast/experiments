const express = require('express');
const http = require('http');
const fs = require('fs');
const formidable = require('formidable');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const server = http.createServer(app);
const port = 8080

function getExperimentID(req, res, next) {
  let experimentID = '';
  if(req.query.experimentID){
    experimentID = req.query.experimentID;
  } else if (req.body.experimentID) {
    experimentID = req.body.experimentID;
  } else {
    return res.status(400).json({result: 'ExperimentID not valid.'});
  }
  if(!experimentID || experimentID == '' || isNaN(experimentID)) {
    return res.status(400).json({result: 'ExperimentID not valid.'});
  }
  if (!fs.existsSync(experimentID)) {
    return res.status(400).json({result: 'ExperimentID has to be created first. Call /experiment/create'});
  }
  req.experimentID = experimentID;
  next();
}

app.use(bodyParser.json());

app.get('/experiment/create', getExperimentID, (req, res) => {
  fs.mkdirSync(req.experimentID);
});


app.post('/csv/upload', getExperimentID, (req, res, next) => {
  var form = new formidable.IncomingForm({uploadDir: path.resolve(__dirname, '../data/csv/'+req.experimentID), keepExtensions: true});
  form.parse(req, (err, fields, files) => {
    if (err) {
      console.log(err);
      return next(err);
    }

    try {
      // let filepath = path.resolve(__dirname, '../photo') + '/' + files.file.name;
      fs.rename(
          files.file.path, form.uploadDir + '/' +fields.fieldType+
              '-' + Date.now()+'.csv');
      console.log("Successful upload!");
      return res.status(200).json({result: 'success'});
    } catch (e) {
      console.log(e);
      return next(e);
    }
  });
});

app.get('/', (req, res) => {
  return res.status(200).json({result: 'Hi!'});
});

const onError = () => {
  console.log('Wrong');
}

const onListening = () => {
  console.log('Listening on port: ' + port);
}
/**
 * Listen on provided port.
 **/
app.set('port', port);
server.listen(port);
server.on('error', onError);
server.on('listening', onListening);