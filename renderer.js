// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.

var data = new Object();
var csvfile = 'lorem.csv'

function newSearch(){
    var root= $("#root-search").val();

    var python = window.spawn('python', ['./regex.py', '-w', root, '-i', csvfile]);
    var data_string = "";

    python.stdout.on('data',function(regex_data){
        data_string += regex_data.toString();
    });

    python.stdout.on('end',function(){
        // console.log(data_string)
        data = JSON.parse(data_string);
        makeWordTree();
        getSentenceStats();
    });
}

document.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();

    for (const f of e.dataTransfer.files) {
      alert('Using file: ' + f.path)
      csvfile = f.path;
    }
  });

document.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
});